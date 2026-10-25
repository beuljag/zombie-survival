"""
===============================================
좀비 슈팅 게임 - LAN 멀티 버전 (최대 4명)
===============================================

- 1인 모드(ZZ1.py)의 좀비/무기/스킬/이펙트를 그대로 사용하고, 여기서는 여러 명이 함께하는 부분만 담당
- 같은 공유기(LAN) 안에서 한 명이 "방 만들기", 나머지는 호스트 IP를 입력해 "참가하기"
- 동기화 방식: 락스텝 - 모든 PC가 같은 입력으로 같은 게임을 동시에 계산하고, 매 프레임 입력만 주고받음
  (호스트가 모두의 입력을 모아서 다시 나눠줌)

【멀티 규칙】
- 좀비 수 = 1인 기준 × 인원수 × 1.1
- 경험치·점수는 공유, 레벨업 업그레이드는 각자 고름 (게임은 멈추지 않음: 화면 아래 카드 클릭 또는 1/2/3 키)
- 죽으면 관전하다가, 죽은 뒤 웨이브 3개가 지나면 살아 있는 팀원 옆에서 부활
- 전원이 죽으면 게임 오버
- 멀티에서는 일시정지/저장 없음 (ESC: 메뉴 - G 게임 포기 / Q 나가기)
===============================================
"""

import socket
import threading
import queue
import json
import time

import ZZ1 as g
from ZZ1 import *  # noqa: F401,F403 - 1인 모드의 클래스/함수/상수를 그대로 사용

PORT = 50007
DISCOVERY_PORT = 50008        # 같은 랜의 방 찾기 (방장이 1초마다 "방 있어요"를 UDP로 알림)
DISCOVERY_TAG = "zombie-survival-room"
MAX_PLAYERS = 4
INPUT_DELAY = 3          # 입력이 반영되기까지의 프레임 (네트워크 지연을 감추는 버퍼). 내 이동은 예측해서 바로 보여주므로 지연이 느껴지지 않음
MOB_FACTOR = 1.1         # 멀티 좀비 수 배율 (× 인원수 × 1.1)
REVIVE_WAVES = 3         # 죽은 뒤 이 웨이브 수가 지나면 부활
REVIVE_INVULN_FRAMES = 300   # 부활 직후 무적 시간 (5초)
HASH_INTERVAL = 300      # 동기화 확인 간격 (프레임)
PLAYER_COLORS = [(0, 255, 0), (80, 170, 255), (255, 170, 60), (230, 90, 255)]
REAL_GET_TICKS = pygame.time.get_ticks


# =====================================================================
# 네트워크
# =====================================================================
class Connection:
    """줄 단위 JSON 메시지를 주고받는 TCP 연결 (받기는 별도 스레드)"""

    def __init__(self, sock):
        self.sock = sock
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.inbox = queue.Queue()
        self.closed = False
        self.lock = threading.Lock()
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        buffer = b""
        try:
            while True:
                data = self.sock.recv(65536)
                if not data:
                    break
                buffer += data
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if line:
                        self.inbox.put(json.loads(line.decode("utf-8")))
        except (OSError, ValueError):
            pass
        self.closed = True

    def send(self, message):
        if self.closed:
            return
        data = (json.dumps(message, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
        try:
            with self.lock:
                self.sock.sendall(data)
        except OSError:
            self.closed = True

    def messages(self):
        while True:
            try:
                yield self.inbox.get_nowait()
            except queue.Empty:
                return

    def close(self):
        self.closed = True
        try:
            self.sock.close()
        except OSError:
            pass


def local_ip_addresses():
    """이 PC의 LAN IP 주소들 (호스트 화면에 표시)"""
    found = []
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(("8.8.8.8", 80))  # 실제로 보내지는 않음 - 기본 경로의 내 IP만 알아냄
        found.append(probe.getsockname()[0])
        probe.close()
    except OSError:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if not ip.startswith("127.") and ip not in found:
                found.append(ip)
    except OSError:
        pass
    return found or ["127.0.0.1"]


class Lockstep:
    """락스텝 입력 교환. 호스트는 모두의 입력을 모아 프레임별 묶음(tick)을 만들어 나눠줌"""

    def __init__(self, role, pid, host_conn=None, client_conns=None, pids=()):
        self.role = role                 # "host" / "client" / "solo"
        self.pid = pid
        self.host_conn = host_conn
        self.client_conns = client_conns or {}   # pid -> Connection (호스트만)
        self.ticks = {}                  # frame -> (inputs, dropped)
        self.pending = {}                # 호스트: frame -> {pid: input}
        self.active = set(pids)          # 호스트: 아직 연결된 플레이어
        self.dropped_queue = []          # 호스트: 다음 tick에 알릴 나간 플레이어
        self.next_tick = 0
        self.host_lost = False
        self.desync = False
        self.my_hashes = {}
        self.peer_hashes = {}
        self.rtt_ms = None               # 참가자: 호스트까지 왕복 시간 (입력 버퍼 자동 조절용)

    def ping(self):
        if self.role == "client":
            self.host_conn.send({"t": "ping", "s": time.time()})

    def input_delay(self):
        """입력 버퍼(프레임): 기본 INPUT_DELAY, 참가자는 핑이 크면 그만큼 늘림 (와이파이에서 멈칫 방지)"""
        if self.role != "client" or self.rtt_ms is None:
            return INPUT_DELAY
        return max(INPUT_DELAY, min(12, int(self.rtt_ms * 1.25 / (1000 / FPS)) + 2))

    def submit(self, frame, inp):
        if self.role == "client":
            self.host_conn.send({"t": "in", "f": frame, "i": inp})
        else:
            self.pending.setdefault(frame, {})[self.pid] = inp

    def report_hash(self, frame, value):
        if self.role == "client":
            self.host_conn.send({"t": "hash", "f": frame, "h": value})
        else:
            self.my_hashes[frame] = value
            self._check_hash(frame)

    def _check_hash(self, frame):
        mine = self.my_hashes.get(frame)
        for value in self.peer_hashes.get(frame, {}).values():
            if mine is not None and value != mine and not self.desync:
                self.desync = True
                for conn in self.client_conns.values():
                    conn.send({"t": "desync", "f": frame})

    def poll(self):
        if self.role == "client":
            for msg in self.host_conn.messages():
                if msg["t"] == "tick":
                    inputs = {int(k): v for k, v in msg["in"].items()}
                    self.ticks[msg["f"]] = (inputs, msg.get("drop", []))
                elif msg["t"] == "desync":
                    self.desync = True
                elif msg["t"] == "pong":
                    rtt = (time.time() - msg["s"]) * 1000
                    # 커질 때는 바로, 작아질 때는 천천히 따라감 (흔들리는 와이파이 대비)
                    self.rtt_ms = rtt if self.rtt_ms is None or rtt > self.rtt_ms else self.rtt_ms * 0.95 + rtt * 0.05
            if self.host_conn.closed:
                self.host_lost = True
            return
        # 호스트 (혼자 테스트 모드 포함)
        for pid, conn in list(self.client_conns.items()):
            for msg in conn.messages():
                if msg["t"] == "in":
                    self.pending.setdefault(msg["f"], {})[pid] = msg["i"]
                elif msg["t"] == "hash":
                    self.peer_hashes.setdefault(msg["f"], {})[pid] = msg["h"]
                    self._check_hash(msg["f"])
                elif msg["t"] == "ping":
                    conn.send({"t": "pong", "s": msg["s"]})
            if conn.closed and pid in self.active:
                self.active.discard(pid)
                self.dropped_queue.append(pid)
                del self.client_conns[pid]
        while True:
            have = self.pending.get(self.next_tick, {})
            if not self.active.issubset(have.keys()):
                break
            inputs = {pid: have[pid] for pid in sorted(have) if pid in self.active}
            dropped, self.dropped_queue = self.dropped_queue, []
            self.ticks[self.next_tick] = (inputs, dropped)
            message = {"t": "tick", "f": self.next_tick, "in": {str(k): v for k, v in inputs.items()}, "drop": dropped}
            for conn in self.client_conns.values():
                conn.send(message)
            self.pending.pop(self.next_tick, None)
            self.next_tick += 1

    def take(self, frame):
        return self.ticks.pop(frame, None)

    def close(self):
        for conn in list(self.client_conns.values()):
            conn.close()
        if self.host_conn is not None:
            self.host_conn.close()


# =====================================================================
# 입력
# =====================================================================
EMPTY_INPUT = {"k": 0, "x": 0, "y": 0, "l": 0, "h": 0, "r": 0, "e": 0, "u": -1, "s": 0, "g": 0}


class KeyState:
    """Player.update()가 읽는 키 상태를 입력 비트로 흉내냄"""
    def __init__(self, bits):
        self.bits = bits

    def __getitem__(self, key):
        # 입력 비트는 "위/왼쪽/아래/오른쪽" 뜻만 담고, 각 PC의 키 설정으로 해석 (키 설정이 달라도 동기화 유지)
        return bool((key in KEYS["up"] and self.bits & 1) or (key in KEYS["left"] and self.bits & 2) or
                    (key in KEYS["down"] and self.bits & 4) or (key in KEYS["right"] and self.bits & 8))

    def action_held(self, action):
        return bool(self.bits & {"up": 1, "left": 2, "down": 4, "right": 8}.get(action, 0))


_current_keys = [KeyState(0)]
REAL_GET_PRESSED = pygame.key.get_pressed


# Bullet에 쏜 사람 기록 (멀티에서 치명타/관통/속성탄을 쏜 사람 기준으로 적용)
_current_owner = DAMAGE_OWNER   # ZZ1과 같은 목록: 여기에 적힌 사람이 지금 주는 피해의 주인 (게임 오버 화면 기록)
_original_bullet_init = Bullet.__init__


def _bullet_init_with_owner(self, *args, **kwargs):
    _original_bullet_init(self, *args, **kwargs)
    self.owner = _current_owner[0]


# =====================================================================
# 멀티 게임 상태 / 시뮬레이션
# =====================================================================
class MatchState:
    def __init__(self, seed, roster, local_pid):
        random.seed(seed)
        fx.reset()
        self.local_pid = local_pid
        self.sim_frame = 0
        self.players = []
        for index, info in enumerate(roster):
            p = Player(index * 60, 0, info["ability"])
            p.weapon = Weapon(info["weapon"])
            if info["ability"] == "damage":
                p.weapon.damage *= 1.6
            p.pid = info["pid"]
            p.color = PLAYER_COLORS[index % len(PLAYER_COLORS)]
            p.image.fill(p.color)
            p.name = f"P{index + 1}"
            p.dead = False
            p.left = False
            p.death_wave = 0
            p.pending_choices = []   # 레벨업으로 고를 업그레이드 후보들
            p.aim = (p.rect.centerx + 100, p.rect.centery)
            p.last_health = p.health
            self.players.append(p)
        self.by_pid = {p.pid: p for p in self.players}
        self.n_players = len(self.players)

        self.all_sprites = pygame.sprite.Group()
        for p in self.players:
            self.all_sprites.add(p)
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        center = self.players[0]
        for _ in range(int(5 * self.n_players * MOB_FACTOR)):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(300, 800)
            zombie = Zombie(center.rect.centerx + math.cos(angle) * distance, center.rect.centery + math.sin(angle) * distance)
            self.zombies.add(zombie)
            self.all_sprites.add(zombie)

        self.score = 0
        self.wave = 1
        self.wave_timer_start = 0
        self.wave_interval = 60000
        self.zombie_spawn_counter = 0
        self.max_zombies = self.scaled(get_max_zombies(self.wave))
        self.game_over = False
        g.TEAM_PROVIDER = self.alive_players   # 앙코르: 팀 전체 버프

    # ----- 도우미 -----
    def scaled(self, count):
        return max(1, int(count * self.n_players * MOB_FACTOR))

    def alive_players(self):
        return [p for p in self.players if not p.dead and not p.left]

    def nearest_player(self, x, y):
        best, best_dist = None, 0
        for p in self.players:
            if p.dead or p.left:
                continue
            center = p.rect.center
            d = (center[0] - x) ** 2 + (center[1] - y) ** 2
            if best is None or d < best_dist:
                best, best_dist = p, d
        return best

    def state_hash(self):
        """동기화 확인용 요약값 (모든 PC가 같아야 함)"""
        total = self.score * 7 + self.wave * 131 + len(self.zombies) * 17
        for z in self.zombies:
            total += round(z.pos_x, 2) + round(z.pos_y, 2) * 3 + round(z.health, 2)
        for p in self.players:
            total += round(p.pos_x, 2) + round(p.pos_y, 2) * 5 + round(p.health, 2) * 11 + p.level
        return round(total, 2)

    # ----- 한 프레임 진행 -----
    def step(self, inputs, dropped):
        self.sim_frame += 1
        for pid in dropped:
            p = self.by_pid.get(pid)
            if p is not None:
                p.left = True
                p.dead = True
                fx.add_text(p.rect.centerx, p.rect.top - 30, f"{p.name} 나감", (200, 200, 200), big=True)
        if self.game_over:
            return
        zombies, bullets, items, explosions, all_sprites = self.zombies, self.bullets, self.items, self.explosions, self.all_sprites

        # 1) 각 플레이어 입력 처리 (업그레이드 선택 / 공격 / 스킬 / 순간이동 / 이동)
        for p in self.players:
            inp = inputs.get(p.pid, EMPTY_INPUT)
            p.aim = (inp["x"], inp["y"])
            if p.pending_choices and 0 <= inp["u"] < len(p.pending_choices[0]):
                apply_upgrade(p, p.pending_choices.pop(0)[inp["u"]])
            if inp.get("g") and not p.dead and not p.left:   # 포기: 바로 쓰러지고 부활하지 않음
                p.surrendered = True
                p.health = 0
            if p.dead or p.left:
                continue
            _current_owner[0] = p
            self.handle_actions(p, inp)
            _current_keys[0] = KeyState(inp["k"])
            p.update()
        _current_owner[0] = None

        # 2) 플레이어 상태 시간 처리 + 레벨업
        for p in self.players:
            if p.dead or p.left:
                continue
            self.tick_player(p)

        alive = self.alive_players()
        if not alive:
            self.game_over = True
            return

        # 3) 시간감속 스킬
        for p in alive:
            if p.skills.get("skill_slowdown", False):
                for zombie in zombies:
                    dx = zombie.rect.centerx - p.rect.centerx
                    dy = zombie.rect.centery - p.rect.centery
                    if dx * dx + dy * dy < 250 * 250:
                        zombie.slow_time = max(zombie.slow_time, 30)
                        zombie.slow_multiplier = min(zombie.slow_multiplier, 0.6)

        # 4) 좀비 이동 (가장 가까운 살아 있는 플레이어를 쫓음)
        for zombie in zombies:
            target = self.nearest_player(zombie.rect.centerx, zombie.rect.centery)
            zombie.chase_target = target   # 그리기(눈 방향)와 아래 거리 확인에서 다시 찾지 않도록 기억
            zombie.update(target, bullets, all_sprites, explosions)
        for p in alive:
            spear_charge(p, zombies)   # 창을 들고 달리면 정면 좀비에게 피해 + 넉백

        # 5) 오라 (벽/수호/질풍/회복)
        for zombie in zombies:
            zombie.guard_mult = 1.0
            zombie.hasted = False
        for source in zombies:
            role = source.angel_role
            aura = None
            if source.zombie_type == "wall":
                aura = ("guard", 160, 0.75)
            elif role == "guardian":
                aura = ("guard", 200, 0.7)
            elif role == "gale" or source.zombie_type == "howler":
                aura = ("haste", 220 if source.zombie_type == "howler" else 200, 0)
            if aura is not None:
                kind, radius, mult = aura
                for other in zombies:
                    if other is source:
                        continue
                    ddx = other.rect.centerx - source.rect.centerx
                    ddy = other.rect.centery - source.rect.centery
                    if ddx * ddx + ddy * ddy < radius * radius:
                        if kind == "guard":
                            other.guard_mult = min(other.guard_mult, mult)
                        else:
                            other.hasted = True
            if (source.zombie_type == "elder" or role == "healer") and source.ability_cooldown <= 0:
                heal_ratio, radius, cooldown = (0.08, 300, 240) if source.zombie_type == "elder" else (0.10, 250, 180)
                source.ability_cooldown = cooldown
                healed = False
                for other in zombies:
                    ddx = other.rect.centerx - source.rect.centerx
                    ddy = other.rect.centery - source.rect.centery
                    if ddx * ddx + ddy * ddy < radius * radius and 0 < other.health < other.max_health:
                        other.health = min(other.max_health, other.health + other.max_health * heal_ratio)
                        healed = True
                if healed:
                    fx.ring(source.rect.centerx, source.rect.centery, (120, 255, 150), radius, count=28)

        # 6) 지속형 스킬 (+ 100레벨 특수 업그레이드)
        for p in self.alive_players():
            if p.special_upgrades:
                _current_owner[0] = p
                tick_specials(p, zombies, bullets, all_sprites, explosions)
        for p in self.players:
            if not p.active_skills:
                continue
            _current_owner[0] = p
            for skill in list(p.active_skills):
                if not skill.update(p, zombies, bullets, all_sprites, explosions):
                    p.active_skills.remove(skill)
        _current_owner[0] = None

        # 7) 너무 멀어진 좀비는 가장 가까운 플레이어 근처로
        leash_sq = ZOMBIE_LEASH_DISTANCE * ZOMBIE_LEASH_DISTANCE
        for zombie in zombies:
            # 쫓던 플레이어가 충분히 가까우면 가장 가까운 플레이어도 그보다 가까우므로 다시 찾을 필요 없음 (결과는 같음)
            near = getattr(zombie, "chase_target", None)
            if near is not None and not near.dead and not near.left:
                dx = zombie.rect.centerx - near.rect.centerx
                dy = zombie.rect.centery - near.rect.centery
                if dx * dx + dy * dy <= leash_sq:
                    continue
            near = self.nearest_player(zombie.rect.centerx, zombie.rect.centery)
            dx = zombie.rect.centerx - near.rect.centerx
            dy = zombie.rect.centery - near.rect.centery
            if dx * dx + dy * dy > leash_sq:
                angle = random.uniform(0, 2 * math.pi)
                zombie.rect.center = (round(near.rect.centerx + math.cos(angle) * ZOMBIE_RESPAWN_DISTANCE),
                                      round(near.rect.centery + math.sin(angle) * ZOMBIE_RESPAWN_DISTANCE))

        # 8) 보스 소환
        self.boss_summons()

        # 9) 총알/아이템/이펙트 갱신
        for bullet in bullets.sprites():   # 총알마다 쏜 사람이 피해의 주인 (사거리 끝 폭발 등)
            _current_owner[0] = getattr(bullet, "owner", None)
            bullet.update()
        for melee_attack in [b for b in bullets if isinstance(b, Melee)]:
            _current_owner[0] = melee_attack.owner
            melee_sweep(melee_attack, zombies)   # 휘두르는 도중 들어온 좀비도 맞음
        _current_owner[0] = None
        items.update()
        explosions.update()
        handled = set(bullets.sprites())
        handled.update(items.sprites())
        handled.update(explosions.sprites())
        for sprite in all_sprites.sprites():
            if sprite in handled or isinstance(sprite, (Player, Zombie)):
                continue
            sprite.update()

        # 10) 총알-좀비 충돌
        self.bullet_hits()
        _current_owner[0] = None

        # 11) 플레이어 쪽 충돌 (아이템, 좀비 접촉, 적 투사체, 장판)
        for p in alive:
            self.player_collisions(p)

        # 12) 좀비 등장 / 웨이브
        self.spawning()

        # 13) 땅굴/결계 피해 무효, 피격 연출
        self.hit_effects()

        # 14) 좀비 죽음 처리
        self.zombie_deaths()

        # 15) 플레이어 사망 → 관전
        for p in alive:
            if p.health <= 0 or getattr(p, "surrendered", False):   # 포기는 재생/회복으로 버티지 않게 바로
                p.health = min(p.health, 0)
                p.dead = True
                p.death_wave = self.wave
                p.active_skills.clear()
                fx.death_burst(p.rect.centerx, p.rect.centery, p.color, 40)
                fx.add_text(p.rect.centerx, p.rect.top - 30, f"{p.name} 포기" if getattr(p, "surrendered", False)
                            else f"{p.name} 쓰러짐! ({REVIVE_WAVES}웨이브 뒤 부활)", (255, 120, 120), big=True, life=90)
        if not self.alive_players():
            self.game_over = True

    # ----- 플레이어 행동 -----
    def handle_actions(self, p, inp):
        zombies, bullets, explosions, all_sprites = self.zombies, self.bullets, self.explosions, self.all_sprites
        aim_x, aim_y = inp["x"], inp["y"]
        if p.skills.get("skill_auto_aim", False) and (inp["l"] or inp["r"] or inp["h"]):
            target = get_auto_aim_target(p, zombies, 600)
            if target:
                aim_x, aim_y = target

        if inp["l"] or (inp["h"] and p.weapon.weapon_type == "machinegun"):
            can_fire = p.shock_time <= 0 and p.weapon.fire()
            if p.skills.get("skill_infinity_ammo", False) and p.infinity_ammo_time > 0 and p.shock_time <= 0:
                can_fire = True
                p.weapon.last_shot_time = pygame.time.get_ticks()
            if can_fire:
                self.fire_weapon(p, aim_x, aim_y, inp.get("b"))

        if inp["r"] and p.weapon.weapon_type == "melee":   # 나무 방망이: 누르고 있으면 힘 모으기
            bat_charge_start(p)
        elif inp["r"]:
            execute_weapon_skill(p.weapon.weapon_type, p, aim_x, aim_y, zombies, bullets, all_sprites, explosions)
        if p.bat_charging:
            bat_charge_tick(p, inp.get("s", 0), aim_x, aim_y, zombies, bullets, all_sprites, explosions)

        if inp["e"] and p.skills.get("skill_teleport", False) and p.teleport_cooldown <= 0:
            p.rect.center = (inp["x"], inp["y"])
            p.teleport_cooldown = p.teleport_cooldown_max

    def fire_weapon(self, p, mouse_world_x, mouse_world_y, beat_frame=None):
        zombies, bullets, explosions, all_sprites = self.zombies, self.bullets, self.explosions, self.all_sprites
        if p.weapon.weapon_type in MELEE_WEAPONS:
            dx = mouse_world_x - p.rect.centerx
            dy = mouse_world_y - p.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                direction_x, direction_y = dx / distance, dy / distance
            else:
                direction_x, direction_y = p.last_direction_x, p.last_direction_y
            melee_damage = get_weapon_damage(p)
            if p.weapon.weapon_type == "hammer":   # 일렉 기타: 박자 판정 - 클릭한 순간(입력 지연 전) 기준
                # 클릭할 때 화면의 박자 = (지금까지 처리된 프레임 sim_frame-1) 중 클릭 프레임 → 몇 프레임 전인지
                frames_ago = 0 if beat_frame is None else max(0, self.sim_frame - 1 - beat_frame)
                melee_damage *= rhythm_judge(p, frames_ago)
            melee = Melee(p.rect.centerx, p.rect.centery, direction_x, direction_y, melee_damage, p.weapon.weapon_type, owner=p)
            bullets.add(melee)
            all_sprites.add(melee)
            melee_hit = False
            first_hit_zombie, first_hit_distance = None, 0
            knockback_mult = get_knockback_multiplier(p)
            for zombie in zombies:
                if zombie.health <= 0:
                    continue
                distance_to_zombie = math.sqrt((zombie.rect.centerx - p.rect.centerx) ** 2 + (zombie.rect.centery - p.rect.centery) ** 2)
                in_range = distance_to_zombie < Melee.CLOSE_HIT_RADIUS
                if not in_range and distance_to_zombie < melee.attack_range:
                    zombie_angle = math.degrees(math.atan2(-(zombie.rect.centery - p.rect.centery), zombie.rect.centerx - p.rect.centerx))
                    angle_diff = abs((zombie_angle - melee.base_angle + 180) % 360 - 180)
                    in_range = angle_diff <= melee.hit_half_arc
                if not in_range:
                    continue
                if not melee_hit or distance_to_zombie < first_hit_distance:
                    first_hit_zombie, first_hit_distance = zombie, distance_to_zombie
                melee_hit = True
                melee.has_hit.add(zombie)   # 휘두르는 동안 다시 맞지 않게
                zombie.health -= melee_strike_damage(p, melee_damage, zombie)
                fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, FX_WEAPON_COLORS.get(p.weapon.weapon_type, WHITE))
                self.apply_elements(p, zombie, melee_damage, 150)
                zombie_dx = zombie.rect.centerx - p.rect.centerx
                zombie_dy = zombie.rect.centery - p.rect.centery
                zombie_dist = math.sqrt(zombie_dx ** 2 + zombie_dy ** 2)
                if zombie_dist > 0:
                    zombie.knockback_vel_x = (zombie_dx / zombie_dist) * melee.knockback_power / 100 * knockback_mult
                    zombie.knockback_vel_y = (zombie_dy / zombie_dist) * melee.knockback_power / 100 * knockback_mult
            if melee_hit and p.weapon.weapon_type == "gloves":
                glove_combo_punch(p, zombies, all_sprites, explosions, first_hit_zombie, direction_x, direction_y)
            if melee_hit and p.skills.get("skill_explosion", False) and p.explosion_cooldown <= 0:
                p.explosion_cooldown = EXPLOSION_SKILL_COOLDOWN
                boom_x, boom_y = first_hit_zombie.rect.center
                explosion = Explosion(boom_x, boom_y, 80, "upgrade")
                explosions.add(explosion)
                all_sprites.add(explosion)
                for other in list(zombies):
                    if other is first_hit_zombie:
                        continue
                    if math.hypot(other.rect.centerx - boom_x, other.rect.centery - boom_y) < 80:
                        other.health -= melee_damage * EXPLOSION_SKILL_RATIO_MELEE * get_damage_multiplier(other)
        elif p.weapon.weapon_type == "shotgun":
            pellets = 3 + p.skill_upgrades["shotgun"]["pellets"]
            spread = 0.6 / (pellets - 1) if pellets > 1 else 0
            for i in range(pellets):
                offset = -0.3 + i * spread if pellets > 1 else 0
                angle = math.atan2(mouse_world_y - p.rect.centery, mouse_world_x - p.rect.centerx) + offset
                bullet = Bullet(p.rect.centerx, p.rect.centery, p.rect.centerx + math.cos(angle) * 500,
                                p.rect.centery + math.sin(angle) * 500, get_weapon_damage(p), "shotgun", "shotgun")
                bullet.speed = p.weapon.bullet_speed
                bullet.max_range = p.weapon.max_range
                bullets.add(bullet)
                all_sprites.add(bullet)
            fire_muzzle_flash(p, mouse_world_x, mouse_world_y, kick=2.5 if p.pid == self.local_pid else 0)
        elif p.weapon.weapon_type == "rocket":
            rocket = Bullet(p.rect.centerx, p.rect.centery, mouse_world_x, mouse_world_y, get_weapon_damage(p), "rocket", "rocket")
            rocket.lock_on(zombies, mouse_world_x, mouse_world_y)   # 유도 로켓
            bullets.add(rocket)
            all_sprites.add(rocket)
            fire_muzzle_flash(p, mouse_world_x, mouse_world_y, kick=3.0 if p.pid == self.local_pid else 0)
        else:
            bullet_type = "plasma" if p.weapon.weapon_type == "plasma" else "normal"
            bullet = Bullet(p.rect.centerx, p.rect.centery, mouse_world_x, mouse_world_y, get_weapon_damage(p), bullet_type, p.weapon.weapon_type)
            bullet.speed = p.weapon.bullet_speed
            bullet.pierce = p.weapon.pierce
            bullet.splash_radius = p.weapon.splash_radius
            bullet.splash_ratio = p.weapon.splash_ratio
            bullet.max_range = p.weapon.max_range
            bullets.add(bullet)
            all_sprites.add(bullet)
            fire_muzzle_flash(p, mouse_world_x, mouse_world_y,
                              kick=2.0 if (p.weapon.weapon_type == "sniper" and p.pid == self.local_pid) else 0)

    def apply_elements(self, p, zombie, base_damage, chain_range):
        """속성탄 (화염/얼음/전기) - 근접/총알 공용"""
        zombies = self.zombies
        if p.skills.get("skill_fire_bullets", False):
            ignite(zombie)   # 화염탄 (이미 불타면 중첩)
            fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "fire")
        if p.skills.get("skill_ice_bullets", False):
            zombie.slow_time = max(zombie.slow_time, 120)
            zombie.slow_multiplier = min(zombie.slow_multiplier, 0.6)
            fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "ice")
        if p.skills.get("skill_electric_bullets", False):
            zombie.electric_fx = 30
            chain = []
            for other in list(zombies):
                if other is zombie:
                    continue
                d = math.hypot(other.rect.centerx - zombie.rect.centerx, other.rect.centery - zombie.rect.centery)
                if d < chain_range:
                    chain.append((d, other))
            chain.sort(key=lambda entry: entry[0])
            for _, target in chain[:2]:
                target.health -= base_damage * 0.4 * get_damage_multiplier(target)
                fx.lightning(zombie.rect.centerx, zombie.rect.centery, target.rect.centerx, target.rect.centery)
                fx.element_hit(target.rect.centerx, target.rect.centery, "electric")
                target.electric_fx = 30

    def tick_player(self, p):
        if p.skills.get("skill_infinity_ammo", False) and p.infinity_ammo_time > 0:
            p.infinity_ammo_time -= 1
            if p.infinity_ammo_time <= 0:
                p.skills["skill_infinity_ammo"] = False
        for attr in ("teleport_cooldown", "explosion_cooldown", "corrode_time", "invuln_time", "damage_buff_time", "speed_buff_time"):
            if getattr(p, attr) > 0:
                setattr(p, attr, getattr(p, attr) - 1)
        if p.shock_time > 0:
            p.shock_time -= 1
        tick_katana_chain(p)   # 연참: 3초 안에 다시 안 쓰면 스택 초기화
        tick_overshield(p)     # 흡혈 보호막 3초
        tick_glove_combo(p)    # 글로브 콤보 (유지 시간 + 공격 속도 보너스)
        if p.regen > 0:
            p.health = min(p.health + p.regen / 60, p.max_health)
        # 독/둔화
        if p.poison_time > 0:
            p.poison_time -= 1
            p.poison_damage_cooldown -= 1
            if p.poison_damage_cooldown <= 0:
                apply_player_damage(p, 0.3)
                p.poison_damage_cooldown = 30
        if p.slow_time > 0:
            p.slow_time -= 1
        else:
            p.slow_multiplier = 1.0
        # 레벨업 → 업그레이드 후보를 미리 정해 둠 (모든 PC에서 같은 후보)
        gained = 0
        while p.exp >= p.exp_to_level:
            p.exp -= p.exp_to_level
            p.level += 1
            p.exp_to_level = int(100 * (1.1 ** p.level))
            gained += 1
        for gained_i in range(gained):   # 레벨마다 맞는 보상 (100레벨은 특수 업그레이드)
            p.pending_choices.append(build_upgrade_choices(p, p.level - gained + 1 + gained_i))
        if gained:
            fx.ring(p.rect.centerx, p.rect.centery, (255, 230, 90), 140, count=36, size=4)
            fx.add_text(p.rect.centerx, p.rect.top - 30, "LEVEL UP!", (255, 230, 90), big=True, life=70)
            if p.pid == self.local_pid:
                sfx("levelup")

    # ----- 보스 소환 -----
    def boss_summons(self):
        zombies, all_sprites, wave, max_zombies = self.zombies, self.all_sprites, self.wave, self.max_zombies

        def summon(kind, x, y, parent, color, life=300):
            minion = Zombie(x, y, zombie_type=kind, wave=wave, parent_zombie=parent)
            zombies.add(minion)
            all_sprites.add(minion)
            all_sprites.add(SpawnEffect(x, y, color, life))
            return minion

        for zombie in list(zombies):
            ztype = zombie.zombie_type
            if ztype == "demon" and len(zombies) < max_zombies + 3:
                zombie.imp_spawn_cooldown += 1
                if zombie.imp_spawn_cooldown >= zombie.imp_spawn_interval:
                    for _ in range(get_summon_count(1, wave, 4)):
                        a = random.uniform(0, 2 * math.pi)
                        summon("imp", zombie.rect.centerx + math.cos(a) * zombie.imp_spawn_radius,
                               zombie.rect.centery + math.sin(a) * zombie.imp_spawn_radius, zombie, (200, 50, 100))
                    zombie.imp_spawn_cooldown = 0
            elif ztype == "boss" and len(zombies) < max_zombies + 5:
                zombie.gangster_spawn_cooldown += 1
                if zombie.gangster_spawn_cooldown >= zombie.gangster_spawn_interval:
                    for _ in range(get_summon_count(zombie.gangster_spawn_count, wave, 4)):
                        a = random.uniform(0, 2 * math.pi)
                        summon("gangster", zombie.rect.centerx + math.cos(a) * zombie.gangster_spawn_radius,
                               zombie.rect.centery + math.sin(a) * zombie.gangster_spawn_radius, zombie, (100, 100, 100))
                    zombie.gangster_spawn_cooldown = 0
            elif ztype == "paladin" and len(zombies) < max_zombies + 5:
                zombie.knight_spawn_cooldown += 1
                if zombie.knight_spawn_cooldown >= zombie.knight_spawn_interval:
                    for _ in range(get_summon_count(1, wave, 6)):
                        a = random.uniform(0, 2 * math.pi)
                        summon("knight", zombie.rect.centerx + math.cos(a) * zombie.knight_spawn_radius,
                               zombie.rect.centery + math.sin(a) * zombie.knight_spawn_radius, zombie, (150, 150, 200))
                    zombie.knight_spawn_cooldown = 0
            elif ztype == "god" and len(zombies) < max_zombies + 10:
                zombie.apostle_spawn_cooldown += 1
                if zombie.apostle_spawn_cooldown >= zombie.apostle_spawn_interval:
                    names = ["베드로", "안드레아", "야고보", "요한", "빌립", "바르톨로메오", "도마", "마태오", "야고보", "다대오", "시몬", "맛디아"]
                    for i, name in enumerate(names):
                        a = (i / 12) * 2 * math.pi
                        apostle = summon("apostle", zombie.rect.centerx + math.cos(a) * 150, zombie.rect.centery + math.sin(a) * 150,
                                         zombie, (255, 255, 200), 200)
                        apostle.custom_name = name
                    for i in range(len(ANGEL_ROLES)):
                        a = (i + 0.5) / len(ANGEL_ROLES) * 2 * math.pi
                        ax, ay = zombie.rect.centerx + math.cos(a) * 260, zombie.rect.centery + math.sin(a) * 260
                        angel = make_role_angel(ax, ay, i, wave, zombie)
                        zombies.add(angel)
                        all_sprites.add(angel)
                        all_sprites.add(SpawnEffect(ax, ay, ANGEL_ROLES[i][2], 300))
                    zombie.apostle_spawn_cooldown = 0
            elif ztype == "king" and len(zombies) < max_zombies + 10:
                zombie.minion_spawn_cooldown += 1
                if zombie.minion_spawn_cooldown >= zombie.minion_spawn_interval:
                    for _ in range(get_summon_count(zombie.minion_spawn_count, wave, 3)):
                        a = random.uniform(0, 2 * math.pi)
                        summon("normal", zombie.rect.centerx + math.cos(a) * zombie.minion_spawn_radius,
                               zombie.rect.centery + math.sin(a) * zombie.minion_spawn_radius, zombie, (200, 0, 0))
                    zombie.minion_spawn_cooldown = 0

    # ----- 총알 충돌 -----
    def bullet_hits(self):
        zombies, bullets, explosions, all_sprites = self.zombies, self.bullets, self.explosions, self.all_sprites
        candidates = [b for b in bullets.sprites() if isinstance(b, Bullet) and not b.is_enemy]
        if not candidates:
            return
        rects = [b.rect for b in candidates]
        for zombie in list(zombies):
            if zombie not in zombies or zombie.health <= 0 or zombie.burrowed > 0:
                continue
            for index in zombie.rect.collidelistall(rects):
                bullet = candidates[index]
                if zombie.health <= 0:
                    break
                if not bullet.alive():
                    continue
                if zombie in bullet.hit_targets or zombie in bullet.dodged:
                    continue
                owner = bullet.owner if getattr(bullet, "owner", None) is not None else self.players[0]
                _current_owner[0] = owner
                if zombie.zombie_type == "shadow" and bullet.bullet_type != "rocket" and random.random() < 0.25:
                    bullet.dodged.add(zombie)
                    fx.add_text(zombie.rect.centerx, zombie.rect.top - 8, "회피", (180, 140, 255))
                    continue
                damage_multiplier = get_damage_multiplier(zombie)
                if bullet.bullet_type == "rocket":
                    zombie.health -= roll_crit_damage(owner, bullet.damage, zombie) * damage_multiplier
                    bullet.kill()
                    fx.hit_spark(bullet.rect.centerx, bullet.rect.centery, FX_WEAPON_COLORS["rocket"])
                    radius = WEAPON_STATS["rocket"]["splash_radius"] + owner.skill_upgrades["rocket"]["explosion"]
                    ratio = WEAPON_STATS["rocket"]["splash_ratio"]
                    knock = get_knockback_multiplier(owner)
                    explosion = Explosion(bullet.rect.centerx, bullet.rect.centery, radius, "rocket")
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                    for other in list(zombies):
                        dist = math.hypot(other.rect.centerx - bullet.rect.centerx, other.rect.centery - bullet.rect.centery)
                        if dist < radius:
                            if other is not zombie:
                                other.health -= bullet.damage * ratio * get_damage_multiplier(other)
                            if dist > 0:
                                other.knockback_vel_x = (other.rect.centerx - bullet.rect.centerx) / dist * 5 * knock
                                other.knockback_vel_y = (other.rect.centery - bullet.rect.centery) / dist * 5 * knock
                    continue
                zombie.health -= bullet_hit_damage(owner, bullet, zombie) * damage_multiplier   # 포탑 총알은 치명타 없음
                fx.hit_spark(bullet.rect.centerx, bullet.rect.centery, FX_WEAPON_COLORS.get(bullet.weapon_type, YELLOW))
                if bullet.splash_radius > 0:
                    splash = Explosion(bullet.rect.centerx, bullet.rect.centery, bullet.splash_radius, "plasma")
                    explosions.add(splash)
                    all_sprites.add(splash)
                    for other in list(zombies):
                        if other is zombie or other.health <= 0:
                            continue
                        if math.hypot(other.rect.centerx - bullet.rect.centerx, other.rect.centery - bullet.rect.centery) < bullet.splash_radius:
                            other.health -= bullet.damage * bullet.splash_ratio * get_damage_multiplier(other)
                self.apply_elements(owner, zombie, bullet.damage, 160)
                if owner.skills.get("skill_explosion", False) and owner.explosion_cooldown <= 0:
                    owner.explosion_cooldown = EXPLOSION_SKILL_COOLDOWN
                    explosion = Explosion(bullet.rect.centerx, bullet.rect.centery, 70, "upgrade")
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                    for other in list(zombies):
                        if other is zombie:
                            continue
                        if math.hypot(other.rect.centerx - bullet.rect.centerx, other.rect.centery - bullet.rect.centery) < 70:
                            other.health -= bullet.damage * EXPLOSION_SKILL_RATIO * get_damage_multiplier(other)
                bullet.hit_targets.add(zombie)
                if len(bullet.hit_targets) > bullet.pierce + owner.pierce_level:
                    bullet.kill()

    # ----- 플레이어 충돌 -----
    def player_collisions(self, p):
        zombies, bullets, items, explosions, all_sprites = self.zombies, self.bullets, self.items, self.explosions, self.all_sprites
        for item in pygame.sprite.spritecollide(p, items, True):
            if p.pid == self.local_pid:
                sfx("pickup")
            fx.ring(item.rect.centerx, item.rect.centery, ITEM_COLORS[item.item_type], 70, count=18)
            fx.add_text(p.rect.centerx, p.rect.top - 20, item.effect, ITEM_COLORS[item.item_type], life=50)
            if item.item_type == "health":
                p.health = min(p.health + ITEM_HEAL_AMOUNT, p.max_health)
                fx.anim("effects/heal.png", p.rect.centerx, p.rect.centery - 10, 2.0, 6)
            elif item.item_type == "damage":
                p.damage_buff_time = ITEM_BUFF_FRAMES
            else:
                p.speed_buff_time = ITEM_BUFF_FRAMES
            self.score += 5

        for zombie in pygame.sprite.spritecollide(p, zombies, False):
            if zombie.burrowed > 0:
                continue
            if zombie.zombie_type == "imp":
                if zombie.health > 0:
                    zombie.health = 0
                    zombie.no_reward = True
                    boom = Explosion(zombie.rect.centerx, zombie.rect.centery, 50, "imp")
                    explosions.add(boom)
                    all_sprites.add(boom)
                    apply_player_damage(p, 6, explosion=True)
                continue
            if zombie.zombie_type == "spark":
                p.shock_time = max(p.shock_time, 36)
            if zombie.zombie_type == "acid":
                p.corrode_time = max(p.corrode_time, 240)
            damage = 0.5
            if zombie.zombie_type == "spike":
                damage += zombie.spike_damage
            if zombie.zombie_type == "poison":
                p.poison_time = 300
            if zombie.zombie_type == "ice":
                if p.slow_time <= 0:
                    p.slow_time = 60
                p.slow_multiplier = min(p.slow_multiplier, zombie.slow_effect)
            apply_player_damage(p, damage)

        for bullet in list(bullets):
            if not bullet.rect.colliderect(p.rect):
                continue
            if isinstance(bullet, (SpikeProjectile, NinjaProjectile)):
                apply_player_damage(p, bullet.damage)
                bullet.kill()
            elif isinstance(bullet, IceProjectile):
                if p.slow_time <= 0:
                    p.slow_time = 300
                p.slow_multiplier = min(p.slow_multiplier, bullet.slow_effect)
                bullet.kill()
            elif isinstance(bullet, Bullet) and bullet.is_enemy:
                apply_player_damage(p, bullet.damage)
                bullet.kill()

        in_pool = False
        for pool in list(explosions):
            if isinstance(pool, PoisonPool):
                if (pool.rect.centerx - p.rect.centerx) ** 2 + (pool.rect.centery - p.rect.centery) ** 2 < pool.radius ** 2:
                    in_pool = True
            elif isinstance(pool, TsunamiEffect):
                hit_set = pool.__dict__.setdefault("hit_players", set())
                if p.pid not in hit_set and pool.rect.colliderect(p.rect):
                    apply_player_damage(p, pool.damage)
                    hit_set.add(p.pid)
        if in_pool:
            if p.poison_time <= 0:
                p.poison_time = 300
            p.pool_damage_cooldown -= 1
            if p.pool_damage_cooldown <= 0:
                apply_player_damage(p, 0.6)
                p.pool_damage_cooldown = 15

    # ----- 등장 / 웨이브 / 부활 -----
    def spawning(self):
        zombies, all_sprites = self.zombies, self.all_sprites
        alive = self.alive_players()
        self.zombie_spawn_counter += 1
        self.max_zombies = self.scaled(get_max_zombies(self.wave))
        if len(zombies) < self.max_zombies and self.zombie_spawn_counter > get_spawn_interval(self.wave):
            anchor = alive[0] if len(alive) == 1 else random.choice(alive)
            angle = random.uniform(0, 2 * math.pi)
            zombie = Zombie(anchor.rect.centerx + math.cos(angle) * 600, anchor.rect.centery + math.sin(angle) * 600,
                            zombie_type=get_zombie_type_by_wave(self.wave), wave=self.wave)
            zombies.add(zombie)
            all_sprites.add(zombie)
            self.zombie_spawn_counter = 0

        if pygame.time.get_ticks() - self.wave_timer_start >= self.wave_interval:
            self.wave += 1
            sfx("wave")
            self.wave_timer_start = pygame.time.get_ticks()
            boss_spawned = False
            for _ in range(self.scaled(3 + self.wave * 2)):
                anchor = alive[0] if len(alive) == 1 else random.choice(alive)
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(300, 800)
                if self.wave >= 3 and not boss_spawned:
                    zombie_type = random.choice(["boss", "paladin", "demon", "angel", "dragon", "king", "god"])
                    boss_spawned = True
                else:
                    zombie_type = get_zombie_type_by_wave(self.wave)
                zombie = Zombie(anchor.rect.centerx + math.cos(angle) * distance, anchor.rect.centery + math.sin(angle) * distance,
                                zombie_type=zombie_type, wave=self.wave)
                zombies.add(zombie)
                all_sprites.add(zombie)
            # 죽은 뒤 웨이브 3개가 지난 팀원 부활
            for p in self.players:
                if p.dead and not p.left and not getattr(p, "surrendered", False) and self.wave - p.death_wave >= REVIVE_WAVES:
                    buddy = random.choice(self.alive_players())
                    p.dead = False
                    p.health = p.max_health * 0.5
                    p.pos_x, p.pos_y = buddy.pos_x + 40, buddy.pos_y
                    p.rect.center = (round(p.pos_x), round(p.pos_y))
                    p._synced_center = p.rect.center
                    p.invuln_time = REVIVE_INVULN_FRAMES
                    p.poison_time = p.slow_time = p.shock_time = p.corrode_time = 0
                    p.slow_multiplier = 1.0
                    fx.ring(p.rect.centerx, p.rect.centery, (120, 255, 160), 120, count=32, size=4)
                    fx.add_text(p.rect.centerx, p.rect.top - 30, f"{p.name} 부활!", (120, 255, 160), big=True, life=90)

    # ----- 피격 연출 -----
    def hit_effects(self):
        for zombie in self.zombies:
            if zombie.burrowed > 0 and zombie.health < zombie.last_health:
                zombie.health = zombie.last_health
        for zombie in self.zombies:
            if zombie.block_hits > 0 and zombie.health < zombie.last_health:
                zombie.health = zombie.last_health
                zombie.block_hits -= 1
                zombie.custom_name = f"{zombie.base_name} [{zombie.block_hits}]"
                fx.add_text(zombie.rect.centerx, zombie.rect.top - 8, "막음", (190, 160, 255))
        for zombie in self.zombies:
            commit_damage(zombie)   # 총 피해 / 가장 강한 한 방 기록
            lost = zombie.last_health - zombie.health
            zombie.last_health = zombie.health
            if zombie.hit_flash > 0:
                zombie.hit_flash -= 1
            if lost > 0.01:
                zombie.damage_accum += lost
                if lost >= 1:
                    zombie.hit_flash = 5
            zombie.damage_text_cooldown -= 1
            if zombie.damage_accum >= 1 and (zombie.damage_text_cooldown <= 0 or zombie.health <= 0):
                fx.add_damage_text(zombie.rect.centerx, zombie.rect.top - 8, zombie.damage_accum, zombie.crit_marked)
                zombie.damage_accum = 0.0
                zombie.crit_marked = False
                zombie.damage_text_cooldown = 6
        for p in self.players:
            lost = p.last_health - p.health
            p.last_health = p.health
            if lost > 0.01 and not p.dead:
                p.hurt_flash = max(p.hurt_flash, 8)
                if p.pid == self.local_pid:
                    fx.add_hurt(min(0.6, lost / 12))
                    if lost >= 6:
                        fx.add_shake(min(10, lost / 3))

    # ----- 좀비 죽음 -----
    def zombie_deaths(self):
        zombies, bullets, items, explosions, all_sprites = self.zombies, self.bullets, self.items, self.explosions, self.all_sprites
        members = [p for p in self.players if not p.left]
        for zombie in list(zombies):
            if zombie not in zombies or zombie.health > 0:
                continue
            if not zombie.no_reward:
                self.score += 10
                for p in members:   # 경험치 공유
                    gain = get_exp_reward(p, self.wave)
                    if getattr(zombie, "dash_kill", False):
                        gain = int(gain * KATANA_DASH_EXP_RATIO)
                    p.exp += gain
                zombie.dash_kill = False
            death_type = zombie.zombie_type
            dx_, dy_ = zombie.rect.center
            zombie.kill()
            if zombie.alive():
                all_sprites.add(ResurrectionEffect(dx_, dy_, (100, 150, 200)))
                zombie.last_health = zombie.health
                continue
            fx.death_burst(dx_, dy_, zombie.image.get_at((zombie.image.get_width() // 2, zombie.image.get_height() // 2))[:3], zombie.size)
            all_sprites.add(DeathFade(zombie))
            if death_type in GUARANTEED_DROP_TYPES:
                fx.add_shake(9)
            if not zombie.no_reward:
                maybe_drop_item(death_type, dx_, dy_, items, all_sprites, summoned=zombie.parent_zombie is not None)
            alive = self.alive_players()

            def damage_players(radius, amount):
                for p in alive:
                    if math.hypot(p.rect.centerx - dx_, p.rect.centery - dy_) < radius:
                        apply_player_damage(p, amount, explosion=True)

            if death_type == "ice":
                target = self.nearest_player(dx_, dy_)
                if target is not None and target.rect.center != (dx_, dy_):
                    projectile = IceProjectile(dx_, dy_, target.rect.centerx, target.rect.centery)
                    bullets.add(projectile)
                    all_sprites.add(projectile)
            elif death_type == "wind":
                all_sprites.add(WindBlastEffect(dx_, dy_, 200, 0.5, 15))
                for other in list(zombies):
                    dist = math.hypot(other.rect.centerx - dx_, other.rect.centery - dy_)
                    if dist < 200:
                        if dist > 0:
                            other.knockback_vel_x += (other.rect.centerx - dx_) / dist * 15
                            other.knockback_vel_y += (other.rect.centery - dy_) / dist * 15
                        other.health -= 0.5
            elif death_type in ("bomber", "mine", "flame", "acid", "toxic", "nuclear"):
                radius = {"bomber": 140, "mine": 170, "flame": 180, "acid": 160, "toxic": 175, "nuclear": 220}[death_type]
                damage = {"bomber": 30.0, "mine": 40.0, "flame": 35.0, "acid": 32.0, "toxic": 38.0, "nuclear": 50.0}[death_type]
                boom = Explosion(dx_, dy_, radius, death_type)
                all_sprites.add(boom)
                explosions.add(boom)
                damage_players(radius, damage * 0.5)
                for other in list(zombies):
                    if math.hypot(other.rect.centerx - dx_, other.rect.centery - dy_) < radius:
                        other.health -= damage * get_damage_multiplier(other)
                if death_type == "flame":
                    all_sprites.add(FlameExplosionEffect(dx_, dy_, radius, 2.0))
                if death_type == "acid":
                    for p in alive:
                        if math.hypot(p.rect.centerx - dx_, p.rect.centery - dy_) < radius:
                            p.corrode_time = max(p.corrode_time, 240)
                if death_type == "toxic":
                    pool = PoisonPool(dx_, dy_, radius=120, duration=6000)
                    explosions.add(pool)
                    all_sprites.add(pool)
                if death_type == "nuclear":
                    for bomb_type in ("bomber", "mine", "flame", "acid", "toxic"):
                        for _ in range(random.randint(0, 3)):
                            a = random.uniform(0, 2 * math.pi)
                            bx = dx_ + math.cos(a) * random.uniform(50, 200)
                            by = dy_ + math.sin(a) * random.uniform(50, 200)
                            child = Zombie(bx, by, zombie_type=bomb_type, wave=zombie.wave, parent_zombie=zombie)
                            zombies.add(child)
                            all_sprites.add(child)
            elif death_type == "slime" and zombie.slime_gen < 2:
                for side in (-1, 1):
                    child = Zombie(dx_ + side * 25, dy_, zombie_type="slime", wave=zombie.wave, parent_zombie=zombie)
                    child.slime_gen = zombie.slime_gen + 1
                    scale = 0.72 ** child.slime_gen
                    size = max(12, int(30 * scale))
                    center = child.rect.center
                    child.image = pygame.Surface((size, size))
                    child.image.fill((90, 220, 90))
                    child.rect = child.image.get_rect(center=center)
                    child._synced_center = child.rect.center
                    child.size = max(14, int(32 * scale))
                    child.health = child.max_health = zombie.max_health * 0.5
                    child.last_health = child.health
                    child.speed *= 1.2
                    zombies.add(child)
                    all_sprites.add(child)
            elif zombie.angel_role == "split":
                for i in range(3):
                    a = i / 3 * math.pi * 2
                    imp = Zombie(dx_ + math.cos(a) * 40, dy_ + math.sin(a) * 40, zombie_type="imp", wave=zombie.wave, parent_zombie=zombie)
                    zombies.add(imp)
                    all_sprites.add(imp)
            elif death_type == "angel" and zombie.angel_role is None:
                all_sprites.add(HolyExplosionEffect(dx_, dy_, 180, 3.0))
                damage_players(180, 3.0)
                for other in list(zombies):
                    if math.hypot(other.rect.centerx - dx_, other.rect.centery - dy_) < 180:
                        other.health -= 3.0
            elif death_type == "god":
                all_sprites.add(HolyExplosionEffect(dx_, dy_, 250, 5.0))
                damage_players(250, 5.0)
                for other in list(zombies):
                    if math.hypot(other.rect.centerx - dx_, other.rect.centery - dy_) < 250:
                        other.health -= 5.0
            elif death_type == "titan" and getattr(zombie, "titan_respawn_as_giants", False):
                for _ in range(2):
                    a = random.uniform(0, 2 * math.pi)
                    giant = Zombie(dx_ + math.cos(a) * 80, dy_ + math.sin(a) * 80, zombie_type="giant", wave=zombie.wave, parent_zombie=zombie)
                    zombies.add(giant)
                    all_sprites.add(giant)


# =====================================================================
# 화면
# =====================================================================
MINIMAP_SIZE = 200           # 미니맵 크기 (px)
MINIMAP_SCALE = 1 / 22       # 월드 1px → 미니맵 크기 (반경 약 2200px가 보임)


def draw_teammate_markers(state, camera, local):
    """화면 밖 팀원: 화면 가장자리에 팀원 색 화살표 + 이름 + 거리 (쓰러진 팀원은 회색 + 부활 대기)"""
    w, h = SCREEN_WIDTH, SCREEN_HEIGHT
    # 표시 영역: 위쪽 HUD와 아래 안내줄을 피해서 (화면 가장자리에서 이만큼 안쪽)
    left_m, right_m, top_m, bottom_m = 60, 60, 120, 110
    cx, cy = (left_m + w - right_m) / 2, (top_m + h - bottom_m) / 2
    half_w, half_h = (w - left_m - right_m) / 2, (h - top_m - bottom_m) / 2
    for p in state.players:
        if p is local or p.left:
            continue
        sx, sy = camera.apply(p.rect.centerx, p.rect.centery)
        if 40 < sx < w - 40 and 40 < sy < h - 40 and not p.dead:
            continue   # 화면 안에 보이면 이름표로 충분
        dx, dy = sx - cx, sy - cy
        if abs(dx) < 1 and abs(dy) < 1:
            continue
        t = min(half_w / abs(dx) if dx else 1e9, half_h / abs(dy) if dy else 1e9, 1.0)
        mx, my = cx + dx * t, cy + dy * t
        angle = math.atan2(dy, dx)
        color = (130, 130, 130) if p.dead else p.color
        pulse = 2 * math.sin(state.sim_frame * 0.15)
        tip = (mx + math.cos(angle) * (34 + pulse), my + math.sin(angle) * (34 + pulse))
        left = (mx + math.cos(angle + 2.6) * 22, my + math.sin(angle + 2.6) * 22)
        right = (mx + math.cos(angle - 2.6) * 22, my + math.sin(angle - 2.6) * 22)
        pygame.draw.polygon(screen, (0, 0, 0), [(tip[0] + 2, tip[1] + 2), (left[0] + 2, left[1] + 2), (right[0] + 2, right[1] + 2)])
        pygame.draw.polygon(screen, color, [tip, left, right])
        pygame.draw.circle(screen, (20, 20, 24), (int(mx), int(my)), 18)
        pygame.draw.circle(screen, color, (int(mx), int(my)), 18, 3)
        ui_text(screen, p.name, font_tiny, color, (mx, my), "center", shadow=False)
        dist = math.hypot(p.rect.centerx - local.rect.centerx, p.rect.centery - local.rect.centery) / 50
        label = "부활 대기" if p.dead else f"{dist:.0f}m"
        ui_text(screen, label, font_hud, color, (mx - math.cos(angle) * 44, my - math.sin(angle) * 40), "center")


def draw_minimap(state, camera, local):
    """오른쪽 아래 미니맵: 팀원 / 내 시야 / 보스 / 주변 좀비"""
    size = MINIMAP_SIZE
    box = pygame.Rect(SCREEN_WIDTH - size - 14, SCREEN_HEIGHT - size - 64, size, size)
    ui_panel(screen, box, alpha=170, radius=10)
    view_x = camera.x + SCREEN_WIDTH / 2
    view_y = camera.y + SCREEN_HEIGHT / 2
    half = size / 2
    to_map = lambda x, y: (box.x + half + (x - view_x) * MINIMAP_SCALE, box.y + half + (y - view_y) * MINIMAP_SCALE)
    screen.set_clip(box.inflate(-4, -4))
    # 내 화면 범위
    vw, vh = SCREEN_WIDTH * MINIMAP_SCALE, SCREEN_HEIGHT * MINIMAP_SCALE
    pygame.draw.rect(screen, (90, 84, 76), (box.x + half - vw / 2, box.y + half - vh / 2, vw, vh), 1)
    # 좀비 (점) / 보스 (큰 점)
    reach = half / MINIMAP_SCALE
    for zombie in state.zombies:
        zx, zy = zombie.rect.center
        if abs(zx - view_x) > reach or abs(zy - view_y) > reach:
            continue
        mx, my = to_map(zx, zy)
        if zombie.zombie_type in GUARANTEED_DROP_TYPES:
            pygame.draw.circle(screen, (255, 90, 90), (int(mx), int(my)), 4)
        else:
            screen.fill((170, 70, 60), (int(mx), int(my), 2, 2))
    # 팀원 (가장자리 밖이면 가장자리에 붙여서)
    for p in state.players:
        if p.left:
            continue
        mx, my = to_map(p.rect.centerx, p.rect.centery)
        mx = min(max(mx, box.x + 6), box.right - 6)
        my = min(max(my, box.y + 6), box.bottom - 6)
        color = (130, 130, 130) if p.dead else p.color
        pygame.draw.circle(screen, color, (int(mx), int(my)), 5)
        if p is local:
            pygame.draw.circle(screen, (245, 240, 232), (int(mx), int(my)), 7, 2)
    screen.set_clip(None)
    ui_text(screen, "지도", font_tiny, UI_SUB, (box.x + 8, box.y + 4), shadow=False)


def draw_upgrade_summary(local, top):
    """TAB(설정한 키): 지금까지 얻은 효과를 종합해서 보여 줌 (게임은 계속 진행)"""
    lines = build_cumulative_upgrade_lines(local) or ["아직 얻은 업그레이드가 없습니다"]
    recent = [get_upgrade_entry_name(e) for e in local.obtained_upgrades[-5:]]
    w = 360
    h = min(SCREEN_HEIGHT - top - 300, 60 + len(lines) * 24 + (40 + len(recent) * 22 if recent else 0))
    box = ui_panel(screen, (SCREEN_WIDTH - w - 14, top, w, h), alpha=225)
    ui_text(screen, f"내 능력 종합 (업그레이드 {len(local.obtained_upgrades)}개)", font_hud, UI_ACCENT, (box.x + 14, box.y + 10))
    y = box.y + 44
    room = (box.bottom - 12 - y - (40 + len(recent) * 22 if recent else 0)) // 24   # 칸에 들어가는 줄 수
    if len(lines) > room:   # 다 안 들어가면 마지막 줄에 "외 N개" (잘린 글자가 보이지 않게)
        lines = lines[:max(0, room - 1)] + [f"… 외 {len(lines) - max(0, room - 1)}개 (ESC → 능력 확인)"]
    screen.set_clip(box.inflate(-6, -6))
    for line in lines:
        pygame.draw.circle(screen, UI_GOOD, (box.x + 20, y + 10), 3)
        ui_text(screen, line, ui_fit_font(font_tiny, line, box.w - 40), UI_TEXT, (box.x + 30, y), shadow=False)
        y += 24
    if recent:
        y += 8
        ui_text(screen, "최근 얻은 것", font_tiny, UI_SUB, (box.x + 14, y), shadow=False)
        y += 22
        for name in reversed(recent):
            ui_text(screen, f"· {name}", ui_fit_font(font_tiny, f"· {name}", box.w - 30), (200, 195, 185), (box.x + 20, y), shadow=False)
            y += 22
    screen.set_clip(None)


def draw_match(state, camera, ui):
    local = state.by_pid[state.local_pid]
    view = local if not local.dead else (state.alive_players() or [local])[0]
    fx.elements = [el for el, sk in (("fire", "skill_fire_bullets"), ("ice", "skill_ice_bullets"),
                                     ("electric", "skill_electric_bullets")) if local.skills.get(sk, False)]
    fx.update()
    pred_x, pred_y = ui.get("pred", (0, 0)) if view is local else (0, 0)
    camera.update(view.rect.centerx + pred_x, view.rect.centery + pred_y)
    camera.shake_x, camera.shake_y = fx.shake_offset()
    screen.fill(BLACK)
    camera.draw_background(screen)

    for sprite in state.all_sprites:
        if isinstance(sprite, Player):
            continue
        if isinstance(sprite, Zombie):
            target = getattr(sprite, "chase_target", None) or local   # 눈 방향만 (게임 계산에서 이미 찾은 대상)
            draw_zombie_sprite(screen, camera, sprite, target)
            continue
        sx, sy = camera.apply(sprite.rect.centerx, sprite.rect.centery)
        sy += getattr(sprite, "draw_offset_y", 0)
        iw, ih = sprite.image.get_size()
        if sx + iw / 2 < 0 or sx - iw / 2 > SCREEN_WIDTH or sy + ih / 2 < 0 or sy - ih / 2 > SCREEN_HEIGHT:
            continue    # 화면 밖은 그리지 않음
        screen.blit(sprite.image, (int(sx - iw / 2), int(sy - ih / 2)))

    # 플레이어들 (각자 조준 방향으로 총구가 향하도록 마우스 위치를 잠깐 바꿔서 그림)
    real_get_pos = pygame.mouse.get_pos
    for p in state.players:
        if p.dead or p.left:
            continue
        ax, ay = camera.apply(*p.aim)
        if p is local:
            ax, ay = real_get_pos() if not FRAME_HOOK else (ax, ay)   # 내 총구는 지금 마우스 방향 (입력 지연 없이)
        pygame.mouse.get_pos = lambda ax=ax, ay=ay: (int(ax), int(ay))
        real_rect = p.rect
        if p is local and (pred_x or pred_y):
            p.rect = p.rect.move(round(pred_x), round(pred_y))   # 내 캐릭터는 예측 위치에 그림 (화면 표시만)
        draw_player_sprite(screen, camera, p)
        if p.invuln_time > 20:     # 부활 무적: 깜빡이는 보호막 (일섬 직후 0.2초 무적에는 안 보임)
            cx, cy = camera.apply(p.rect.centerx, p.rect.centery)
            pulse = 4 * math.sin(state.sim_frame * 0.25)
            ring_alpha_color = (150, 230, 255) if p.invuln_time > 60 or p.invuln_time % 10 < 5 else (90, 140, 170)
            pygame.draw.circle(screen, ring_alpha_color, (int(cx), int(cy)), int(32 + pulse), 3)
        sx, sy = camera.apply(p.rect.centerx, p.rect.top)
        p.rect = real_rect
        tag = font_desc.render(p.name + (" (나)" if p.pid == state.local_pid else ""), True, p.color)
        screen.blit(tag, (sx - tag.get_width() // 2, sy - 30))
        bar = pygame.Rect(0, 0, 40, 5)
        bar.midbottom = (int(sx), int(sy - 4))
        pygame.draw.rect(screen, (60, 0, 0), bar)
        pygame.draw.rect(screen, p.color, (bar.x, bar.y, int(40 * max(0, p.health) / p.max_health), 5))
    pygame.mouse.get_pos = real_get_pos
    if ui.get("show_fps", True):
        ping = f" · 핑 {ui['ping']:.0f}ms" if ui.get("ping") is not None else ""
        text = f"FPS {clock.get_fps():.0f}{ping}" if SETTINGS["show_fps"] else ping.strip(" ·")   # FPS는 설정, 핑은 항상
        if text:
            ui_text(screen, text, font_tiny, UI_SUB, (SCREEN_WIDTH - 14, SCREEN_HEIGHT - 52), "topright")
    fx.draw(screen, camera)

    draw_zombie_labels(screen, camera, state.zombies)
    draw_hurt_overlay(screen, fx.hurt)

    # 내 정보 (좌상단) / 웨이브 (가운데) / 보스 체력
    draw_player_status(screen, local)
    progress = (pygame.time.get_ticks() - state.wave_timer_start) / state.wave_interval
    wave_box = draw_wave_panel(screen, state.wave, progress, state.wave_interval)
    draw_boss_bar(screen, state.zombies, wave_box.bottom + 6)

    # 팀 정보 (우상단)
    pw = 300
    team = ui_panel(screen, (SCREEN_WIDTH - pw - 14, 14, pw, 62 + len(state.players) * 50), alpha=232)
    ui_text(screen, "점수", font_tiny, UI_SUB, (team.x + 14, team.y + 18), shadow=False)
    ui_text(screen, f"{state.score:,}", font_hud_big, UI_TEXT, (team.right - 14, team.y + 6), "topright")
    for i, p in enumerate(state.players):
        row = pygame.Rect(team.x + 10, team.y + 56 + i * 50, pw - 20, 44)
        pygame.draw.rect(screen, (46, 43, 39), row, border_radius=8)
        pygame.draw.rect(screen, p.color, (row.x, row.y + 6, 4, row.h - 12), border_radius=2)
        name = p.name + (" (나)" if p.pid == state.local_pid else "")
        ui_text(screen, f"{name} · {p.weapon.name}", font_tiny, ui_bright(p.color), (row.x + 12, row.y + 3), shadow=False)
        bar = pygame.Rect(row.x + 12, row.y + 25, row.w - 24, 13)
        if p.left:
            ui_text(screen, "나감", font_tiny, UI_DIM, (row.right - 10, row.y + 3), "topright", shadow=False)
            ui_bar(screen, bar, 0, (90, 90, 90), back=(40, 40, 46), radius=5)
        elif p.dead:
            left = max(0, REVIVE_WAVES - (state.wave - p.death_wave))
            ui_text(screen, f"부활까지 {left}웨이브", font_tiny, (255, 150, 150), (row.right - 10, row.y + 3), "topright", shadow=False)
            ui_bar(screen, bar, 1 - left / REVIVE_WAVES, (150, 110, 200), back=(40, 30, 50), radius=5)
        else:
            ui_text(screen, f"LV.{p.level}", font_tiny, UI_ACCENT, (row.right - 10, row.y + 3), "topright", shadow=False)
            ratio = max(0, p.health) / max(p.max_health, 1)
            ui_bar(screen, bar, ratio, UI_GOOD if ratio > 0.5 else (255, 200, 60) if ratio > 0.25 else UI_DANGER, radius=5)
    draw_beat_ui(screen, local)
    set_sfx_listener(local)
    music_tick(local, state.zombies)   # 전투/보스 음악
    if ui.get("help"):
        draw_class_help(screen, local)
    if state.n_players > 1:
        draw_minimap(state, camera, local)
        draw_teammate_markers(state, camera, local)
    if ui.get("stack"):
        draw_upgrade_summary(local, team.bottom + 10)

    # 업그레이드 선택 카드 (게임은 계속 진행)
    ui["cards"] = []
    if local.pending_choices and not local.left:
        choices = local.pending_choices[0]
        width, height, gap = 270, 104, 18
        x0 = SCREEN_WIDTH // 2 - (len(choices) * width + (len(choices) - 1) * gap) // 2
        y0 = SCREEN_HEIGHT - 190
        special = bool(choices) and choices[0].get("special", False)
        ui_text(screen, f"{'★ 특수 업그레이드!' if special else '레벨업! 업그레이드'} 선택 (클릭 또는 {binding_label('pick1')}/{binding_label('pick2')}/{binding_label('pick3')}) "
                        f"· 남은 선택 {len(local.pending_choices)}", font_hud, g.SPECIAL_COLOR if special else UI_ACCENT,
                (SCREEN_WIDTH // 2, y0 - 34), "midtop")
        mouse = pygame.mouse.get_pos()
        for i, choice in enumerate(choices):
            rect = pygame.Rect(x0 + i * (width + gap), y0, width, height)
            ui["cards"].append(rect)
            ui_card(screen, rect, choice["color"], rect.collidepoint(mouse), choice["name"], [choice["desc"]], badge=f"[{i + 1}]",
                    title_color=ui_bright(choice["color"]), line_font=font_tiny)

    def banner(text, color, y):
        surf_w = font_hud.size(text)[0] + 40
        box = ui_panel(screen, (SCREEN_WIDTH // 2 - surf_w // 2, y, surf_w, 38), alpha=200, border=color)
        ui_text(screen, text, font_hud, color, box.center, "center")

    if local.dead and not state.game_over:
        banner(f"쓰러졌습니다 - 관전 중 (부활까지 {max(0, REVIVE_WAVES - (state.wave - local.death_wave))}웨이브)", (255, 150, 150), 170)
    if ui.get("waiting", 0) > 30:
        banner("다른 플레이어를 기다리는 중...", UI_ACCENT, 216)
    if ui.get("desync"):
        banner("동기화 오류가 감지되었습니다 (게임은 계속되지만 화면이 서로 다를 수 있음)", UI_DANGER, 262)
    if ui.get("menu"):
        ui_overlay(screen, 170)
        box = pygame.Rect(0, 0, 460, 290)
        box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ui_panel(screen, box, alpha=235, radius=16)
        ui_text(screen, "멀티 게임 메뉴", font_large, UI_TEXT, (box.centerx, box.y + 22), "midtop")
        ui_text(screen, "G  게임 포기 (내 캐릭터, 부활 없음)", font_medium, (230, 150, 110), (box.centerx, box.y + 105), "midtop")
        ui_text(screen, "Q  방 나가기", font_medium, UI_DANGER, (box.centerx, box.y + 160), "midtop")
        ui_text(screen, "ESC  돌아가기", font_medium, UI_GOOD, (box.centerx, box.y + 215), "midtop")
    if state.game_over:
        ranking = sorted(state.players, key=lambda p: -p.damage_dealt)
        rows = [(p.name + (" (나)" if p is local else ""), p.color, p.damage_dealt, p.best_hit) for p in ranking]
        draw_game_over(screen, "전원 쓰러짐 - 게임 오버!", [("점수", state.score), ("웨이브", state.wave), ("인원", state.n_players)],
                       "SPACE / ESC: 멀티 메뉴로", damage_rows=rows)


def run_match(lockstep, seed, roster, local_pid):
    """락스텝 멀티 게임 진행. 돌아가면 멀티 메뉴로."""
    state = MatchState(seed, roster, local_pid)
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    local = state.by_pid[local_pid]
    g.LOCAL_PLAYER = local                # 소리 기준 (내 플레이어)
    warm_up_game_sfx()
    if any(p.weapon.weapon_type == "hammer" for p in state.players):
        warm_up_sfx()                     # 팀원 기타 소리도 미리 (처음 칠 때 멈칫하지 않게)
    g.RHYTHM_SOUND_ON_JUDGE = False       # 일렉 기타 소리는 클릭한 순간 바로 (판정은 입력 지연 뒤)
    pygame.time.get_ticks = lambda: int(state.sim_frame * 1000 / 60)   # 게임 시간은 프레임 기준 (모든 PC 동일)
    pygame.key.get_pressed = lambda: _current_keys[0]
    Bullet.__init__ = _bullet_init_with_owner
    ui = {"cards": [], "waiting": 0, "menu": False, "desync": False}
    next_send = 0
    clicks = {"l": 0, "r": 0, "e": 0, "u": -1}
    my_moves = {}                     # 보냈지만 아직 게임에 반영되지 않은 내 이동 입력 (예측 표시용)
    loops = 0
    pace_start = REAL_GET_TICKS()     # 멈칫한 뒤 따라잡기용 기준 시각
    try:
        while True:
            clock.tick(FPS)
            for event in REAL_EVENT_GET():
                if event.type == pygame.QUIT:
                    lockstep.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if state.game_over and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                        return
                    if event.key == pygame.K_ESCAPE and ui.get("help"):
                        ui["help"] = False          # 설명 화면이 떠 있으면 ESC는 설명만 닫음
                    elif event.key == pygame.K_ESCAPE:
                        ui["menu"] = not ui["menu"]
                    elif ui["menu"] and event.key == pygame.K_q:
                        return
                    elif ui["menu"] and event.key == pygame.K_g:
                        clicks["g"] = 1          # 포기 (모든 PC에 입력으로 전달)
                        ui["menu"] = False
                    elif binding_event(event, "teleport"):
                        clicks["e"] = 1
                    elif binding_event(event, "mute"):
                        toggle_mute()
                    elif binding_event(event, "help"):
                        ui["help"] = not ui.get("help", False)   # 멀티는 게임이 멈추지 않음
                    elif binding_event(event, "attack") and not ui["menu"]:
                        clicks["l"] = 1
                        clicks["b"] = state.sim_frame
                        rhythm_click_sound(local)
                    elif (binding_event(event, "skill")) and not ui["menu"]:
                        clicks["r"] = 1
                    elif binding_event(event, "stack"):
                        ui["stack"] = not ui.get("stack", False)
                    elif pick_from_event(event) >= 0 and local.pending_choices:
                        clicks["u"] = pick_from_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and not ui["menu"]:
                    card = next((i for i, rect in enumerate(ui["cards"]) if rect.collidepoint(event.pos)), None)
                    if card is not None and event.button == 1:
                        clicks["u"] = card        # 업그레이드 카드는 항상 좌클릭
                    elif binding_event(event, "attack"):
                        clicks["l"] = 1
                        clicks["b"] = state.sim_frame
                        rhythm_click_sound(local)
                    elif binding_event(event, "skill"):
                        clicks["r"] = 1
                    elif binding_event(event, "teleport"):          # 마우스 버튼으로 지정한 순간이동 등
                        clicks["e"] = 1
                    elif binding_event(event, "mute"):
                        toggle_mute()
                    elif binding_event(event, "help"):
                        ui["help"] = not ui.get("help", False)
                    elif binding_event(event, "stack"):
                        ui["stack"] = not ui.get("stack", False)
                    elif pick_from_event(event) >= 0 and local.pending_choices:
                        clicks["u"] = pick_from_event(event)

            # 내 입력 보내기 (INPUT_DELAY 프레임 뒤에 반영)
            loops += 1
            if loops % 20 == 1:
                lockstep.ping()
            while next_send <= state.sim_frame + lockstep.input_delay():
                keys = REAL_GET_PRESSED()
                mx, my = pygame.mouse.get_pos()
                held = binding_held("attack", keys) and not ui["menu"]
                bits = 0 if ui["menu"] else (binding_held("up", keys) * 1 | binding_held("left", keys) * 2 |
                                             binding_held("down", keys) * 4 | binding_held("right", keys) * 8)
                inp = {"k": bits, "x": int(mx + camera.x), "y": int(my + camera.y), "l": clicks["l"], "h": int(held),
                       "s": int(binding_held("skill", keys) and not ui["menu"]),
                       "b": clicks.get("b", state.sim_frame),
                       "r": clicks["r"], "e": clicks["e"], "u": clicks["u"], "g": clicks.get("g", 0)}
                inp.update(INPUT_HOOK(state, local) if INPUT_HOOK else {})
                lockstep.submit(next_send, inp)
                my_moves[next_send] = inp["k"]
                clicks = {"l": 0, "r": 0, "e": 0, "u": -1}
                next_send += 1

            # 받은 입력으로 게임 진행 - 1인용과 똑같이 화면 1번 그릴 때 게임 1프레임 진행
            # (예전에는 입력이 도착하는 대로 한 화면에 최대 4프레임씩 진행해서 1인용보다 빨랐고,
            #  실제 시간에 맞추는 방식은 화면과 게임 프레임이 어긋나 툭툭 끊기거나 빨라지는 느낌이 났음)
            # PC가 느려서 60fps가 안 나오면 1인용처럼 다 같이 조금 느려짐 (락스텝이라 모두 같은 속도)
            # 네트워크로 잠깐 멈칫했으면(실제 시간보다 3프레임 이상 늦음) 한 화면에 2프레임씩 조금씩 따라잡음
            # 평소에는 항상 1프레임 (화면과 게임이 어긋나지 않게 여유 범위를 둠)
            behind = int((REAL_GET_TICKS() - pace_start) * FPS / 1000) - state.sim_frame
            if behind > 20 or behind < -20:      # 크게 밀리면(창 이동/긴 끊김) 그냥 지금부터 다시 맞춤
                pace_start = REAL_GET_TICKS() - state.sim_frame * 1000 / FPS
                behind = 0
            max_steps = 2 if behind >= 3 else (0 if behind <= -3 else 1)
            lockstep.poll()
            advanced = 0
            stalled = False
            while advanced < max_steps:
                tick = lockstep.take(state.sim_frame)
                if tick is None:
                    stalled = True
                    break
                inputs, dropped = tick
                state.step(inputs, dropped)
                advanced += 1
                if state.sim_frame % HASH_INTERVAL == 0:
                    lockstep.report_hash(state.sim_frame, state.state_hash())
                    lockstep.poll()
            ui["waiting"] = ui["waiting"] + 1 if stalled and not advanced else 0
            # 내 이동 예측: 아직 반영 안 된 이동 입력만큼 앞서 그림
            for f in [f for f in my_moves if f < state.sim_frame]:
                del my_moves[f]
            if local.dead or local.left:
                ui["pred"] = (0, 0)
            else:
                speed = local.speed * local.slow_multiplier * (ITEM_BUFF_MULTIPLIER if local.speed_buff_time > 0 else 1)
                if local.encore_time > 0:
                    speed *= 1 + ENCORE_SPEED   # 앙코르 (Player.update와 같게)
                if local.bat_charging:
                    speed *= BAT_CHARGE_SLOW
                px = py = 0.0
                for bits in my_moves.values():
                    px += speed * (((bits >> 3) & 1) - ((bits >> 1) & 1))
                    py += speed * (((bits >> 2) & 1) - (bits & 1))
                ui["pred"] = (px, py)
            ui["desync"] = lockstep.desync
            ui["ping"] = lockstep.rtt_ms
            if lockstep.host_lost:
                message_screen("호스트와 연결이 끊겼습니다", "아무 키나 누르면 멀티 메뉴로")
                return
            if FRAME_HOOK:
                if FRAME_HOOK(state) == "stop":
                    return
            draw_match(state, camera, ui)
            pygame.display.flip()
    finally:
        pygame.time.get_ticks = REAL_GET_TICKS
        pygame.key.get_pressed = REAL_GET_PRESSED
        Bullet.__init__ = _original_bullet_init
        lockstep.close()


REAL_EVENT_GET = pygame.event.get
INPUT_HOOK = None     # 자동 시험용: 입력을 덮어쓰는 함수
FRAME_HOOK = None     # 자동 시험용: 매 프레임 호출


# =====================================================================
# 메뉴 / 로비
# =====================================================================
def message_screen(title, subtitle="", wait=True):
    ui_background(screen)
    ui_title(screen, title, SCREEN_HEIGHT // 2 - 80, subtitle)
    pygame.display.flip()
    while wait:
        for event in REAL_EVENT_GET():
            ui_quit_event(event)
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
        clock.tick(30)


BUTTON_COLORS = {"host": (128, 196, 132), "join": (106, 155, 204), "keys": (180, 160, 220), "settings": (120, 190, 200), "quit": (228, 92, 78)}


def button_menu(title, options, info_lines=()):
    """버튼 목록 화면 → 고른 버튼의 key"""
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    while True:
        ui_background(screen)
        top = ui_title(screen, title, SCREEN_HEIGHT * 0.16)
        for i, line in enumerate(info_lines):
            ui_text(screen, line, font_desc, UI_SUB, (SCREEN_WIDTH // 2, top + 16 + i * 28), "midtop", shadow=False)
        mouse = pygame.mouse.get_pos()
        rects = []
        for i, (key, label) in enumerate(options):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 70 + i * 92, 380, 76)
            rects.append((key, rect))
            hover = rect.collidepoint(mouse)
            card = ui_card(screen, rect, BUTTON_COLORS.get(key, UI_ACCENT), hover)
            ui_text(screen, label, font_medium, UI_TEXT, card.center, "center")
        ui_text(screen, "ESC: 뒤로", font_tiny, UI_DIM, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50), "midtop", shadow=False)
        for event in REAL_EVENT_GET():
            ui_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in rects:
                    if rect.collidepoint(event.pos):
                        return key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
        pygame.display.flip()
        clock.tick(30)


def _windows_clipboard():
    """윈도우 클립보드의 글자를 직접 읽음 (추가 설치 없이 동작)"""
    import ctypes
    from ctypes import wintypes
    user32, kernel32 = ctypes.windll.user32, ctypes.windll.kernel32
    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.GetClipboardData.restype = wintypes.HANDLE
    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = wintypes.LPVOID
    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    if not user32.OpenClipboard(None):
        return ""
    try:
        handle = user32.GetClipboardData(13)      # CF_UNICODETEXT
        if not handle:
            return ""
        pointer = kernel32.GlobalLock(handle)
        if not pointer:
            return ""
        try:
            return ctypes.wstring_at(pointer)
        finally:
            kernel32.GlobalUnlock(handle)
    finally:
        user32.CloseClipboard()


def read_clipboard():
    """클립보드 글자 (붙여넣기용) - 윈도우 기본 기능으로 먼저, 안 되면 pygame으로"""
    try:
        if sys.platform == "win32":
            text = _windows_clipboard()
            if text:
                return text
    except Exception:
        pass
    try:
        if not pygame.scrap.get_init():
            pygame.scrap.init()
        return pygame.scrap.get_text() or ""
    except Exception:
        return ""


def clean_address(text):
    """붙여넣은 글자에서 IP에 쓰는 글자(숫자와 점)만 남김 - "192.168.0.5:50007" 같은 것도 처리"""
    import re
    found = re.search(r"\d{1,3}(?:\.\d{1,3}){3}", text)
    if found:
        return found.group(0)
    return "".join(ch for ch in text.strip() if ch.isdigit() or ch == ".")[:40]


def text_input(title, initial=""):
    pygame.key.start_text_input()     # 글자 입력 화면에서만 켬 (게임 중에는 꺼 둠)
    try:
        return _text_input_loop(title, initial)
    finally:
        pygame.key.stop_text_input()


def _text_input_loop(title, initial):
    text = initial
    while True:
        ui_background(screen)
        ui_title(screen, title, SCREEN_HEIGHT // 2 - 150)
        box = pygame.Rect(SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 30, 460, 64)
        ui_panel(screen, box, alpha=235, border=UI_ACCENT, width=2)
        caret = "|" if pygame.time.get_ticks() // 500 % 2 else ""
        ui_text(screen, text + caret, font_medium, UI_TEXT, (box.x + 18, box.centery), "midleft", shadow=False)
        ui_text(screen, "호스트 화면에 보이는 IP를 입력하고 Enter · Ctrl+V/우클릭: 붙여넣기 · ESC: 취소", font_desc, UI_SUB,
                (SCREEN_WIDTH // 2, box.bottom + 20), "midtop", shadow=False)
        for event in REAL_EVENT_GET():
            ui_quit_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text.strip()
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif (event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL) or \
                        (event.key == pygame.K_INSERT and event.mod & pygame.KMOD_SHIFT):
                    pasted = clean_address(read_clipboard())
                    if pasted:
                        text = pasted        # 붙여넣기: 입력칸 내용을 붙여넣은 IP로 바꿈
                elif event.unicode and (event.unicode.isdigit() or event.unicode == ".") and len(text) < 40:
                    text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pasted = clean_address(read_clipboard())
                if pasted:
                    text = pasted            # 우클릭으로도 붙여넣기
        pygame.display.flip()
        clock.tick(30)


def draw_roster(names, top, title):
    """로비: 참가자 목록 패널"""
    box = pygame.Rect(SCREEN_WIDTH // 2 - 260, top, 520, 70 + MAX_PLAYERS * 46)
    ui_panel(screen, box, alpha=220, radius=14)
    ui_text(screen, title, font_hud, UI_ACCENT, (box.x + 20, box.y + 14))
    for i in range(MAX_PLAYERS):
        row = pygame.Rect(box.x + 16, box.y + 54 + i * 46, box.w - 32, 38)
        pygame.draw.rect(screen, (46, 43, 39), row, border_radius=8)
        color = PLAYER_COLORS[i] if i < len(PLAYER_COLORS) else UI_TEXT
        if i < len(names):
            pygame.draw.circle(screen, color, (row.x + 18, row.centery), 7)
            ui_text(screen, names[i], font_desc, UI_TEXT, (row.x + 36, row.centery), "midleft", shadow=False)
        else:
            ui_text(screen, "빈 자리", font_desc, UI_DIM, (row.x + 36, row.centery), "midleft", shadow=False)
    return box


def choose_loadout():
    ability = select_ability()
    weapon = select_weapon()
    return {"ability": ability, "weapon": weapon}


class RoomBeacon:
    """방장: 대기실에 있는 동안 같은 랜에 "방 있어요"를 1초마다 알림 (UDP 방송)"""
    def __init__(self):
        self.sock = None
        self.next_send = 0.0
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except OSError:
            self.sock = None
        targets = {"255.255.255.255", "127.0.0.1"}
        for ip in local_ip_addresses():   # 공유기마다 255.255.255.255가 막힐 수 있어서 내 대역(x.x.x.255)에도 보냄
            parts = ip.split(".")
            if len(parts) == 4:
                targets.add(".".join(parts[:3] + ["255"]))
        self.targets = sorted(targets)
        try:
            self.name = socket.gethostname()[:24]
        except OSError:
            self.name = "방장"

    def tick(self, players, weapon_name):
        if self.sock is None or time.time() < self.next_send:
            return
        self.next_send = time.time() + 1.0
        data = json.dumps({"tag": DISCOVERY_TAG, "build": GAME_BUILD, "name": self.name, "players": players,
                           "max": MAX_PLAYERS, "port": PORT, "weapon": weapon_name}, ensure_ascii=False).encode("utf-8")
        for target in self.targets:
            try:
                self.sock.sendto(data, (target, DISCOVERY_PORT))
            except OSError:
                pass

    def close(self):
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None


class RoomFinder:
    """참가: 같은 랜에서 알림을 보내는 방들을 모음 (3.5초 동안 소식이 없으면 목록에서 뺌)"""
    def __init__(self):
        self.rooms = {}   # ip -> (정보, 마지막으로 들은 시각)
        self.sock = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", DISCOVERY_PORT))
            self.sock.setblocking(False)
        except OSError:
            self.sock = None

    def poll(self):
        if self.sock is not None:
            while True:
                try:
                    data, (ip, _port) = self.sock.recvfrom(2048)
                except (BlockingIOError, OSError):
                    break
                try:
                    info = json.loads(data.decode("utf-8"))
                except ValueError:
                    continue
                if isinstance(info, dict) and info.get("tag") == DISCOVERY_TAG:
                    self.rooms[ip] = (info, time.time())
        now = time.time()
        for ip in [ip for ip, (_info, seen) in self.rooms.items() if now - seen > 3.5]:
            del self.rooms[ip]
        # 같은 PC의 방이 여러 주소(127.0.0.1, 랜, VPN 등)로 들릴 수 있음 → PC 이름별로 하나만, 집 공유기 주소를 우선
        def priority(ip):
            if ip.startswith("192.168.") or ip.startswith("10."):
                return 0
            parts = ip.split(".")
            if ip.startswith("172.") and len(parts) == 4 and parts[1].isdigit() and 16 <= int(parts[1]) <= 31:
                return 0
            return 2 if ip.startswith("127.") else 1
        best = {}
        for ip, (info, _seen) in self.rooms.items():
            key = (info.get("name"), info.get("port"))
            if key not in best or (priority(ip), ip) < (priority(best[key][0]), best[key][0]):
                best[key] = (ip, info)
        return sorted(best.values(), key=lambda item: item[0])

    def close(self):
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None


def browse_rooms():
    """참가하기: 같은 랜의 방 목록 → 고른 방의 IP / "manual"(직접 입력) / None(뒤로)"""
    finder = RoomFinder()
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    notice, notice_until = "", 0
    try:
        while True:
            rooms = finder.poll()
            mouse = pygame.mouse.get_pos()
            ui_background(screen)
            top = ui_title(screen, "참가할 방 고르기", SCREEN_HEIGHT * 0.12,
                           "같은 와이파이/공유기에서 열린 방이 자동으로 나와요")
            cards = []
            y = top + 30
            if finder.sock is None:
                ui_text(screen, f"방 찾기를 쓸 수 없어요 (포트 {DISCOVERY_PORT} 사용 중) - 'IP 직접 입력'을 쓰세요", font_desc, UI_DANGER,
                        (SCREEN_WIDTH // 2, y + 20), "midtop", shadow=False)
            elif not rooms:
                dots = "." * (1 + (pygame.time.get_ticks() // 400) % 3)
                ui_text(screen, f"방을 찾는 중{dots}", font_medium, UI_SUB, (SCREEN_WIDTH // 2, y + 20), "midtop", shadow=False)
                ui_text(screen, "방장이 '방 만들기'를 눌렀는지, 같은 네트워크인지 확인하세요 (방화벽에서 게임 허용이 필요할 수 있어요)",
                        font_tiny, UI_DIM, (SCREEN_WIDTH // 2, y + 70), "midtop", shadow=False)
            for ip, info in rooms[:6]:
                rect = pygame.Rect(SCREEN_WIDTH // 2 - 320, y, 640, 78)
                same = info.get("build") == GAME_BUILD
                full = info.get("players", 0) >= info.get("max", MAX_PLAYERS)
                color = (128, 196, 132) if same and not full else (150, 140, 130)
                card = ui_card(screen, rect, color, same and not full and rect.collidepoint(mouse),
                               f"{info.get('name', '방')}의 방", [f"{ip}  ·  방장 무기: {info.get('weapon', '?')}"], title_font=font_hud)
                status = "가득 참" if full else ("업데이트 필요" if not same else f"{info.get('players', 1)}/{info.get('max', MAX_PLAYERS)}명")
                ui_text(screen, status, font_hud, UI_DANGER if (full or not same) else UI_GOOD, (card.right - 20, card.centery), "midright")
                cards.append((rect, ip, same, full))
                y += 92
            manual = pygame.Rect(SCREEN_WIDTH // 2 - 320, SCREEN_HEIGHT - 150, 310, 64)
            back = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 150, 310, 64)
            ui_button(screen, manual, "IP 직접 입력", (106, 155, 204), manual.collidepoint(mouse))
            ui_button(screen, back, "뒤로", (228, 92, 78), back.collidepoint(mouse))
            if notice and pygame.time.get_ticks() < notice_until:
                ui_text(screen, notice, font_desc, UI_DANGER, (SCREEN_WIDTH // 2, manual.y - 40), "midtop")
            pygame.display.flip()
            for event in REAL_EVENT_GET():
                ui_quit_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if manual.collidepoint(event.pos):
                        return "manual"
                    if back.collidepoint(event.pos):
                        return None
                    for rect, ip, same, full in cards:
                        if rect.collidepoint(event.pos):
                            if not same:
                                notice = "게임 버전이 달라서 들어갈 수 없어요 - 둘 다 최신 버전으로 업데이트하세요"
                            elif full:
                                notice = "방이 가득 찼어요"
                            else:
                                return ip
                            notice_until = pygame.time.get_ticks() + 3000
            clock.tick(30)
    finally:
        finder.close()


def host_lobby(loadout):
    """방 만들기: 참가자를 기다렸다가 시작 → (lockstep, seed, roster)"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("", PORT))
    except OSError:
        message_screen("방을 만들 수 없습니다", f"포트 {PORT}가 이미 사용 중입니다. 아무 키나 누르세요")
        return None
    server.listen(MAX_PLAYERS)
    server.settimeout(0.0)
    clients = {}          # pid -> Connection
    loadouts = {0: loadout}
    ips = local_ip_addresses()
    beacon = RoomBeacon()   # 같은 랜에 "방 있어요" 알림
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    while True:
        # 새 참가자
        try:
            sock, _addr = server.accept()
            sock.setblocking(True)
            pid = next(i for i in range(1, MAX_PLAYERS) if i not in clients) if len(clients) < MAX_PLAYERS - 1 else None
            if pid is None:
                sock.close()
            else:
                clients[pid] = Connection(sock)
                clients[pid].send({"t": "welcome", "pid": pid})
        except (BlockingIOError, OSError):
            pass
        for pid, conn in list(clients.items()):
            for msg in conn.messages():
                if msg["t"] == "hello":
                    loadouts[pid] = {"ability": msg["ability"], "weapon": msg["weapon"]}
            if conn.closed:
                del clients[pid]
                loadouts.pop(pid, None)
        roster_text = [f"P{i + 1}: {WEAPON_STATS[loadouts[pid]['weapon']]['name']}" for i, pid in enumerate(sorted(loadouts))]
        beacon.tick(len(loadouts), WEAPON_STATS[loadout["weapon"]]["name"])
        for conn in clients.values():
            conn.send({"t": "lobby", "players": roster_text})

        ui_background(screen)
        top = ui_title(screen, "멀티 방 (호스트)", 40)
        ip_box = ui_panel(screen, (SCREEN_WIDTH // 2 - 260, top + 20, 520, 64), alpha=220, border=UI_ACCENT)
        ui_text(screen, "같은 랜이면 참가자 화면에 이 방이 자동으로 떠요 (안 뜨면 이 IP를 알려 주세요)", font_tiny, UI_SUB,
                (ip_box.centerx, ip_box.y + 6), "midtop", shadow=False)
        ui_text(screen, f"{', '.join(ips)}   (포트 {PORT})", font_hud, UI_ACCENT, (ip_box.centerx, ip_box.y + 28), "midtop")
        roster_box = draw_roster(roster_text, ip_box.bottom + 16, f"참가 인원 {len(loadouts)}/{MAX_PLAYERS}")
        start = pygame.Rect(SCREEN_WIDTH // 2 - 200, roster_box.bottom + 24, 190, 66)
        cancel = pygame.Rect(SCREEN_WIDTH // 2 + 10, roster_box.bottom + 24, 190, 66)
        mouse = pygame.mouse.get_pos()
        for rect, label, color in ((start, "게임 시작", (128, 196, 132)), (cancel, "취소", (228, 92, 78))):
            card = ui_card(screen, rect, color, rect.collidepoint(mouse))
            ui_text(screen, label, font_medium, UI_TEXT, card.center, "center")
        ui_text(screen, "모든 참가자가 무기를 고르고 들어오면 '게임 시작'을 누르세요", font_desc, UI_SUB,
                (SCREEN_WIDTH // 2, start.bottom + 18), "midtop", shadow=False)
        pygame.display.flip()

        go = LOBBY_HOOK("host", len(loadouts)) if LOBBY_HOOK else None
        for event in REAL_EVENT_GET():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start.collidepoint(event.pos):
                    go = "start"
                elif cancel.collidepoint(event.pos):
                    go = "cancel"
        if go == "cancel":
            beacon.close()
            for conn in clients.values():
                conn.close()
            server.close()
            return None
        if go == "start" and all(pid in loadouts for pid in clients):
            beacon.close()   # 게임이 시작되면 더 이상 알리지 않음
            server.close()
            seed = random.randrange(1 << 30)
            roster = [{"pid": pid, **loadouts[pid]} for pid in sorted(loadouts)]
            for conn in clients.values():
                conn.send({"t": "start", "seed": seed, "roster": roster})
            lockstep = Lockstep("host", 0, client_conns=clients, pids=[r["pid"] for r in roster])
            return lockstep, seed, roster, 0
        clock.tick(30)


def join_lobby(loadout, address):
    try:
        sock = socket.create_connection((address, PORT), timeout=5)
        sock.settimeout(None)
    except OSError:
        message_screen("접속할 수 없습니다", f"{address}:{PORT} - IP와 같은 공유기인지, 방화벽을 확인하세요. 아무 키나 누르세요")
        return None
    conn = Connection(sock)
    conn.send({"t": "hello", **loadout})
    pid = None
    players = []
    while True:
        for msg in conn.messages():
            if msg["t"] == "welcome":
                pid = msg["pid"]
            elif msg["t"] == "lobby":
                players = msg["players"]
            elif msg["t"] == "start":
                return Lockstep("client", pid, host_conn=conn), msg["seed"], msg["roster"], pid
        if conn.closed:
            message_screen("방이 닫혔습니다", "아무 키나 누르세요")
            return None
        ui_background(screen)
        dots = "." * (pygame.time.get_ticks() // 400 % 4)
        top = ui_title(screen, "호스트가 시작하기를 기다리는 중" + dots, 60, f"접속: {address}")
        draw_roster(players, top + 30, "참가자")
        ui_text(screen, "ESC: 나가기", font_desc, UI_SUB, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70), "midtop", shadow=False)
        pygame.display.flip()
        for event in REAL_EVENT_GET():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                conn.close()
                return None
        clock.tick(30)


LOBBY_HOOK = None     # 자동 시험용


def multiplayer_menu():
    last_address = "192.168."
    if not g._music_synth:
        g._prepare_music_thread()   # 기본 배경 음악을 뒤에서 만듦
    apply_volume()
    while True:
        set_music("menu")
        choice = button_menu("좀비 슈팅 - LAN 멀티 (최대 4명)", [("host", "방 만들기 (호스트)"), ("join", "참가하기"), ("keys", "키 설정"), ("settings", "설정"), ("quit", "나가기")],
                             [f"좀비 수 = 1인 기준 x 인원수 x {MOB_FACTOR}  |  죽으면 {REVIVE_WAVES}웨이브 뒤 부활  |  경험치 공유"])
        if choice in (None, "quit"):
            return
        if choice == "keys":
            show_key_settings()
            continue
        if choice == "settings":
            show_settings()
            continue
        if choice == "host":
            result = host_lobby(choose_loadout())
        else:
            address = browse_rooms()   # 같은 랜의 방 목록에서 고르기
            if address == "manual":
                address = text_input("호스트 IP 주소", last_address)
                if address:
                    last_address = address
            if not address:
                continue
            result = join_lobby(choose_loadout(), address)
        if result is not None:
            lockstep, seed, roster, pid = result
            run_match(lockstep, seed, roster, pid)


if __name__ == "__main__":
    try:
        g.UPDATE_ASSET = "ZombieMulti.exe"
        maybe_offer_update()   # exe 실행이면 새 버전 확인
        multiplayer_menu()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    pygame.quit()
    sys.exit()
