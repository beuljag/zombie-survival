"""
===============================================
좀비 슈팅 게임 v1.0
===============================================

【게임 개요】
- 장르: 서바이벌 슈팅 로그라이크
- 플레이 방식: WASD 이동, 마우스 조준 및 좌클릭 발사, 우클릭 스킬 사용
- 목표: 계속 나타나는 좀비를 무찌르고 최대한 오래 생존하기

【조작법】
- WASD: 플레이어 이동
- 마우스: 조준 및 선택
- 좌클릭: 무기 발사
- 우클릭: 무기별 스킬 사용 (쿨타임 있음)
- E: 순간이동 (순간이동 스킬 획득 시)
- TAB: 획득한 업그레이드 목록 표시
- ESC: 게임 일시정지
- 마우스 클릭: 업그레이드 선택

【모든 좀비 이름 목록 (36가지)】
일반 6종: 일반, 스파이크, 갑옷, 헤비, 독, 얼음
탱크 6종: 탱크, 기사, 방패, 돌, 철, 벽
빠른 6종: 빠른, 주자, 닌자, 스파크, 바람, 그림자
폭탄 6종: 폭탄, 광산, 불꽃, 산성, 독가스, 핵
보스 9종: 보스, 갱스터, 임프, 악마, 기사단장, 천사, 용, 왕, 신
거대 6종: 콜로서스, 타이탄, 거인, 베히모스, 리바이어던, 엘더

【게임 진행】
- 좀비를 사냥하면 경험치 획득
- 경험치가 다 차면 레벨업되고 업그레이드 3가지 중 선택 가능
- 웨이브 시스템: 60초마다 난이도 상승 및 보스 등장
- 웨이브 3부터 보스 좀비 출현 시작
- 플레이어 체력이 0 이하면 게임 오버

【근접 무기 (6가지)】 - 조준 방향 부채꼴 범위의 좀비를 모두 타격 (몸에 붙은 좀비는 방향 상관없이)
- 나무 방망이: 데미지 36, 초당 2.8회, 범위 110, 초보자용
- 카타나: 데미지 26, 초당 4회, 범위 120, 가장 높은 근접 DPS
- 도끼: 데미지 65, 초당 1.5회, 범위 125, 강한 넉백
- 창: 데미지 36, 초당 2회, 범위 165 (가장 긴 근접 사거리)
- 해머: 데미지 80, 초당 1.25회, 범위 155, 가장 강한 넉백
- 글로브: 데미지 18, 초당 5회, 범위 100

【원거리 무기 (6가지)】
- 글록: 데미지 16, 초당 4회, 균형 잡힌 기본 권총
- 샷건: 데미지 15 × 3발, 초당 1.5회, 사거리 380 (근거리 전용)
- 저격총: 데미지 50, 초당 1회, 기본 공격이 관통
- 기관총: 데미지 7, 초당 9회, 꾹 누르고 있으면 연사
- 플라즈마: 데미지 28, 초당 2회, 착탄 시 반경 70 폭발 (주변 50%)
- 로켓: 데미지 55, 초당 0.8회, 반경 115 큰 폭발 (주변 50%)

【일반 좀비 (6가지)】
- 일반: 체력 30, 공격력 0.5, 가장 약함, 15% 확률로 한 번 다시 일어남
- 스파이크: 체력 40, 공격력 0.8, 가시 투사체 발사
- 갑옷: 체력 55, 공격력 0.4, 받는 데미지 40% 감소, 죽으면 일반좀비로 부활
- 헤비: 체력 50, 공격력 0.7, 무거운 좀비, 체력 이용 돌진 공격
- 독: 체력 35, 공격력 0.9, 독 장판 생성, 플레이어에 독 상태이상
- 얼음: 체력 38, 공격력 0.5, 얼음 투사체, 플레이어 속도 저하

- 분열: 체력 40, 공격력 0.5, 죽으면 작은 분열좀비 2마리로 나뉨 (2번까지)

【탱크 좀비 (6가지)】
- 탱크: 체력 80, 공격력 0.3, 넉백 완전 저항, 4초마다 발 구르기 충격파 (주변 피해 6)
- 기사: 체력 120, 공격력 0.5, 넉백 면역, 죽으면 방패좀비로 부활
- 방패: 체력 120, 공격력 0.2, 방패 착용, 받는 데미지 95% 감소, 죽으면 갑옷좀비로 부활
- 돌: 체력 140, 공격력 0.15, 화상·둔화 상태이상 면역
- 철: 체력 110, 공격력 0.28, 철갑옷 (받는 피해 25% 감소), 죽으면 돌좀비로 부활
- 벽: 체력 160, 공격력 0.1, 가장 느림, 수호 오라 (주변 좀비가 받는 피해 25% 감소)

- 함성: 체력 45, 공격력 0.5, 주변(220) 좀비의 이동속도 +30% (주황 고리) - 먼저 잡기

【빠른 좀비 (6가지)】
- 빠른: 체력 15, 공격력 0.4, 빠른 이동속도 4.0, 지그재그로 움직여 맞히기 어려움
- 주자: 체력 12, 공격력 0.35, 오래 쫓을수록 빨라짐 (최대 +60%, 맞으면 초기화)
- 닌자: 체력 10, 공격력 0.6, 매우 빠른 이동속도 7.5, 원거리 공격
- 스파크: 체력 14, 공격력 0.5, 닿으면 감전 (0.6초 동안 공격 불가)
- 바람: 체력 8, 공격력 0.3, 속도 130% 증가, 죽으면 광역 혼합 효과
- 그림자: 체력 9, 공격력 0.55, 가장 빠름, 멀리 있으면 거의 안 보임 + 총알 25% 회피

- 저격: 체력 30, 공격력 0.4, 멀리서 멈춰 빨간 조준선을 보여준 뒤 강한 한 발 (조준선을 보고 피하기)

【폭탄 좀비 (6가지)】
- 폭탄: 체력 40, 공격력 0.6, 디토네이터, 죽으면 폭발
- 광산: 체력 50, 공격력 0.8, 지뢰, 죽으면 강한 폭발
- 불꽃: 체력 45, 공격력 0.7, 화염 폭발, 죽으면 광역 화염 피해
- 산성: 체력 42, 공격력 0.65, 닿거나 폭발에 휘말리면 부식 (4초 동안 받는 피해 +30%)
- 독가스: 체력 48, 공격력 0.75, 독성 폭발, 죽으면 독 영역 생성
- 핵: 체력 60, 공격력 1.0, 핵폭발, 죽으면 폭탄/광산/불꽃/산성/독가스 5종 0~3마리씩 소환

【보스 좀비 (9가지)】
- 보스: 체력 200, 공격력 1.5, 갱스터 지속 소환 (2마리), 금색
- 갱스터: 체력 25, 공격력 0.7, 보스가 소환하는 원거리 공격 좀비
- 임프: 체력 15, 공격력 0.4, 악마가 소환, 플레이어에게 닿으면 자폭 (피해 6)
- 악마: 체력 240, 공격력 1.8, 임프 지속 소환, 보라색
- 기사단장: 체력 300, 공격력 2.0, 기사 지속 소환, 죽으면 갑옷좀비로 부활
- 천사: 체력 220, 공격력 1.6, 신성한 폭발 능력, 흰색
- 용: 체력 280, 공격력 2.0, 돌진 공격 + 원거리 파이어볼, 보라색
- 왕: 체력 260, 공격력 1.9, 일반 좀비 대량 소환 (3마리)
- 신: 체력 350, 공격력 2.5, 12초마다 12사도 + 12천사 동시 소환, 죽으면 신성한 폭발, 흰색
  12천사 (각자 다른 능력): 라파엘(치유: 주변 회복) / 미카엘(수호: 주변 피해 30% 감소) / 우리엘(화염: 파이어볼)
  / 하니엘(서리: 둔화 투사체) / 라미엘(번개: 직격 + 감전) / 아리엘(질풍: 빠름 + 주변 이동속도 +30%)
  / 라구엘(심판: 근처 신성 폭발) / 예레미엘(부활: 한 번 부활) / 메타트론(결계: 처음 4번 공격 무효)
  / 산달폰(분열: 죽으면 임프 3마리) / 아즈라엘(흡혈: 체력 흡수) / 가브리엘(순간이동: 플레이어 근처로 이동)

【거대 좀비 (6가지)】
- 콜로서스: 체력 500, 공격력 2.0, 매우 느림, 3초마다 지진 (주변 피해 10 + 화면 흔들림)
- 타이탄: 체력 600, 공격력 2.3, 30% 확률로 거인 2마리로 부활, 느린 이동속도 0.25
- 거인: 체력 450, 공격력 1.8, 4초마다 큰 돌 던지기 (피해 12)
- 베히모스: 체력 700, 공격력 2.5, 가장 큼, 돌진 공격, 이동속도 0.2
- 리바이어던: 체력 650, 공격력 2.4, 가로/세로 쓰나미 공격, 느린 이동속도 0.28
- 엘더: 체력 800, 공격력 2.8, 가장 높은 체력, 4초마다 주변 좀비 체력 8% 회복

【업그레이드 시스템】
기본 업그레이드:
- 체력: +8 또는 +12 최대 체력 증가
- 속도: +0.3 또는 +0.5 이동속도 증가
- 데미지: +2 또는 +5 모든 무기 데미지 증가
- 재생: +0.3 또는 +0.5 초당 체력 회복
- 치명타: 5% 확률로 1.3배 데미지 (중첩 가능, 5%씩 증가) / 저격총 전용 "치명타 데미지 +25%"로 배율 증가 (최대 3.8배)
- 회피: 5% 확률로 피해 회피 (중첩 가능, 5%씩 증가)
- 경험치: +20% 좀비 처치 시 경험치 추가
- 완전 회복: 체력 100% 회복
- 넉백: 적 넉백 강도 +10%

스킬 (레벨 조건):
- 투사체 관통 (Lv3): 찍을 때마다 총알이 좀비를 1마리 더 관통 (최대 10)
- 화염탄 (Lv2): 불 피해 추가
- 얼음탄 (Lv2): 좀비 속도 저하
- 전기탄 (Lv3): 인접한 좀비들에게 전기 전달
- 자동조준 (Lv4): 가까운 적 자동 조준
- 방어막 (Lv3): 플레이어 주변 방어막 생성
- 순간이동 (Lv4): 마우스 위치로 즉시 이동
- 시간감속 (Lv5): 주변 좀비 속도 감소
- 폭발 공격 (Lv4): 공격 시 작은 폭발 (주변 30%, 근접 무기는 12%, 0.2초에 한 번)
- 무한탄약 (Lv2): 30초간 탄약 무한 사용

무기별 스킬 (우클릭):
- 나무 방망이: 홈런 - 앞쪽 좀비를 크게 날려 보냄 (8초)
- 카타나: 일섬 - 마우스 방향으로 순간 돌진하며 지나간 길을 벰, 끝난 뒤 0.2초 무적 (6초)
  적을 처치하면 쿨타임 초기화 + 다음 일섬 데미지 +5% (연참, 중첩), 처치에 실패하거나 1초 안에 다시 쓰지 않으면 원래대로
  일섬으로 처치한 좀비 1마리당 체력 1 회복
  기본 공격 업그레이드(치명타 / 화염·얼음·전기탄 / 폭발)가 일섬에도 적용됨
  "카타나 데미지 +3" 강화 1회당 일섬 데미지 +10% 추가
  오의 연섬 (패시브, 레벨 6부터 업그레이드로 획득): 일섬 피해 25%가 고정 피해로 (최소 대상 최대 체력 6%, 방어 무시)
  "연참 데미지 +3%" 업그레이드로 스택당 보너스 증가
  일섬으로 처치한 좀비는 경험치 75%
- 도끼: 대회전 베기 - 도끼를 크게 한 바퀴 휘둘러 주변을 베고(3.5배) 멀리 날려 버림 + 준 피해의 10% 흡혈 (최대 100) (12초)
- 창: 물보라 - 주변(230)으로 물결을 일으켜 좀비를 튕겨 내고 3초 동안 50% 느리게 함 (2배 데미지) (8초)
  창 데미지는 이동속도에 비례, 창을 들고 달리면 공격하지 않아도 정면 좀비에게 피해 + 넉백
- 해머: 대지 강타 - 마우스 위치를 내려쳐 주변 좀비 1.5초 기절 (12초)
- 글로브: 러시 - 3초 동안 공격 속도 3배 (15초)
- 글록: 항공 폭격 - 비행기가 날아와 조준 방향 직선(약 1000px)에 폭탄을 줄줄이 떨어뜨림
  폭탄 1발 기본 1000 데미지, 공격력이 오르면 같은 비율로 증가 (80초)
- 기관총: 포탑 설치 - 6초 동안 자동으로 쏘는 포탑 (18초)
- 샷건: 용의 숨결 - 앞쪽 부채꼴 화염 방사 + 불붙임 (10초)
- 저격총: 도탄 사격 - 한 발이 맞은 좀비에서 주변 좀비로 10번 튕김 (맞을 때마다 3배 데미지, "도탄 +3회" 업그레이드) (12초)
  튕길 때마다 기본 공격 업그레이드(치명타 / 화염·얼음·전기탄 / 폭발 공격) 적용, 도탄은 치명타 확률 +20%
- 플라즈마: 블랙홀 - 3초 동안 좀비를 빨아들이며 피해, 사라질 때 안에서 죽은 좀비 수만큼 강해지는 붕괴 폭발 (18초)
- 로켓: 미사일 폭격 - 마우스 주변에 미사일 8발 (15초)

【주요 게임 메카닉】
1. 넉백 시스템: 좀비마다 다른 넉백 저항도 (탱크는 완전 저항)
2. 치명타 시스템: 업그레이드로 중첩, 최대 80% (16회)
3. 회피 시스템: 업그레이드로 중첩, 최대 100% (20회)
4. 상태이상: 독 (지속 피해), 얼음 (속도 저하)
5. 부활 시스템:
   - 갑옷 -> 일반으로 부활
   - 기사 -> 방패 -> 갑옷 -> 일반으로 부활
   - 기사단장 -> 갑옷으로 부활
   - 철 -> 돌로 부활
   - 타이탄 -> 30% 확률로 거인 2마리로 부활
6. 특수 부활 소환:
   - 신: 12초마다 12사도 임프 12마리 동시 소환(천사 능력치)
   - 핵: 폭탄 5종(폭탄/광산/불꽃/산성/독가스) 0~3마리씩 랜덤 소환
7. 특수 공격:
   - 리바이어던: 가로/세로 쓰나미 공격 (교차 형태)
   - 용: 돌진 공격 + 부채꼴 파이어볼
   - 바람: 속도 130% 증가
8. 아이템 드롭: 좀비 처치 시 3% 확률 (보스/거대 좀비는 50%) - 체력 +25 / 공격력 +30% 10초 / 이동속도 +30% 10초
9. 웨이브 시스템: 60초마다 난이도 상승, 새로운 좀비 타입 해금
   - 웨이브마다 등장하는 좀비 수 +2, 등장 간격 단축, 보스 소환 수도 증가
   - 보스/거대 좀비 체력 1.6배 (다른 좀비가 소환한 개체 제외)
10. 경험치 부스트: 업그레이드로 추가 경험치 10%씩 증가

【연출 (게임 판정에는 영향 없음)】
- 피격: 좀비 하얀 번쩍임, 데미지 숫자 (치명타는 노란색 큰 숫자), 타격 불꽃
- 처치: 몸 색 파편 + 쓰러지며 사라짐, 보스/거대 좀비는 화면 흔들림
- 무기: 총구 화염, 총알이 날아가는 방향으로 회전, 로켓 연기/플라즈마 잔광/저격 궤적
- 근접: 방망이·카타나는 빠르게 휘두르고, 도끼·해머는 들었다 내려찍고(땅 울림), 창·글로브는 찌르기 + 잔상
- 폭발: 퍼지면서 사라지는 불꽃 + 파편, 큰 폭발은 화면 흔들림
- 좀비/플레이어: 걸을 때 흔들림, 그림자, 눈이 상대를 바라봄 / 피격 시 화면 가장자리 붉은 경고
- 아이템: 둥실 떠 있음, 획득 시 반짝임 + 효과 글자 / 레벨업 고리 + "LEVEL UP!"

【난이도 진행】
- 웨이브 1-2: 일반 좀비 중심
- 웨이브 3+: 보스 좀비 등장, 특수 좀비 증가
- 웨이브 10+: 거대 좀비 등장
- 시간이 지날수록 더 강력한 좀비 조합 출현

===============================================
"""

import pygame
import random
import math
import sys
import os
import json

# pygame 초기화
pygame.init()

# 화면 설정
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()   # 실제로 만들어진 화면 크기 기준으로 UI 배치
pygame.display.set_caption("좀비 슈팅 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 자주 쓰는 무기 타입 상수 (반복 생성 방지)
MELEE_WEAPONS = {"melee", "katana", "axe", "spear", "hammer", "gloves"}

# 좀비가 쏘는 Bullet 타입 (플레이어 총알과 구분: 좀비에게는 맞지 않고 플레이어에게만 맞음)
ENEMY_BULLET_TYPES = {"gangster_bullet", "dragon_fireball", "giant_rock", "zombie_snipe"}

# 신좀비가 12사도와 함께 소환하는 12천사 (역할, 이름, 색) - 이름은 역할에 어울리는 대천사 이름
ANGEL_ROLES = [
    ("healer", "라파엘 (치유)", (120, 255, 150)),       # "신이 치유하신다" - 3초마다 주변 좀비 체력 10% 회복
    ("guardian", "미카엘 (수호)", (150, 180, 255)),     # 천사군의 대장 - 주변 좀비가 받는 피해 30% 감소
    ("flame", "우리엘 (화염)", (255, 140, 60)),         # "신의 불꽃" - 파이어볼 발사
    ("frost", "하니엘 (서리)", (150, 230, 255)),        # 달의 천사 - 얼음 투사체 (이동속도 50% 감소)
    ("thunder", "라미엘 (번개)", (255, 240, 90)),       # "신의 천둥" - 번개 직격 + 잠깐 감전
    ("gale", "아리엘 (질풍)", (200, 255, 230)),         # 자연과 바람의 천사 - 자신은 2배 빠르고 주변 좀비 이동속도 +30%
    ("judgment", "라구엘 (심판)", (255, 215, 120)),     # 정의와 심판의 천사 - 가까이 오면 신성한 폭발
    ("rebirth", "예레미엘 (부활)", (255, 180, 220)),    # 부활의 희망을 맡은 천사 - 한 번 죽어도 체력 50%로 부활
    ("barrier", "메타트론 (결계)", (190, 160, 255)),    # 보호 문양 "메타트론의 큐브" - 처음 4번의 공격을 막아냄
    ("split", "산달폰 (분열)", (255, 120, 170)),        # 메타트론의 쌍둥이 - 죽으면 임프 3마리로 분열
    ("drain", "아즈라엘 (흡혈)", (200, 40, 70)),        # 죽음의 천사 - 플레이어 체력을 빨아들여 회복
    ("blink", "가브리엘 (순간이동)", (160, 120, 255)),  # 홀연히 나타나는 신의 전령 - 플레이어 근처로 순간이동
]

# 플레이어에게서 이 거리보다 멀어진 좀비는 플레이어 근처(ZOMBIE_RESPAWN_DISTANCE)로 다시 배치
ZOMBIE_LEASH_DISTANCE = 2500
ZOMBIE_RESPAWN_DISTANCE = 1000

# 근접 무기 "공격 속도" 업그레이드 1회당 증가율 (창은 스킬 투사체 속도에 적용)
MELEE_SPEED_UPGRADE_RATES = {"melee": 0.08, "katana": 0.12, "spear": 0.08, "gloves": 0.10}

# ===== 무기 밸런스 기준표 =====
# dmg: 1회 데미지 / rate: 초당 공격 횟수 / speed: 탄속(px/프레임)
# 공격 간격(ms) = 1000 / (rate × 공격 속도 배율)   ← 모든 무기가 같은 기준 (예전에는 무기마다 기준이 섞여 있었음)
# 자동 플레이 시뮬레이션(무기당 32회, 웨이브 15까지)으로 무기별 평균 생존 시간이 전체 평균의 ±30% 안에 들도록 조정
#   - 근접은 플레이어 주변 원형 범위의 좀비를 전부 때리지만 붙어 싸워야 해서 DPS를 더 높게
#   - 광역 무기(플라즈마/로켓)는 단일 DPS를 낮추는 대신 폭발 피해, 샷건은 근거리 전용 대신 높은 피해
WEAPON_STATS = {
    # ----- 원거리 -----
    "glock":      {"name": "글록",   "dmg": 16, "rate": 4.0,  "speed": 14, "color": YELLOW},  # DPS 64  기본 권총
    "machinegun": {"name": "기관총", "dmg": 7,  "rate": 9.0, "speed": 14, "color": (100, 100, 100)},  # DPS 63  꾹 눌러 연사
    "shotgun":    {"name": "샷건",   "dmg": 15, "rate": 1.5,  "speed": 13, "color": (200, 100, 0),
                   "max_range": 380},  # DPS 68  (3발 전탄) 근거리 전용
    "sniper":     {"name": "저격총", "dmg": 50, "rate": 1.0,  "speed": 24, "color": GRAY,
                   "pierce": 2},  # DPS 50  기본 공격이 2마리 더 관통
    "plasma":     {"name": "플라즈마", "dmg": 28, "rate": 2.0, "speed": 13, "color": CYAN,
                   "splash_radius": 70, "splash_ratio": 0.4},  # DPS 56  + 착탄 폭발(주변 40%)
    "rocket":     {"name": "로켓",   "dmg": 55, "rate": 0.8,  "speed": 9,  "color": RED,
                   "splash_radius": 115, "splash_ratio": 0.4},  # DPS 44  + 큰 폭발(주변 40%)
    # ----- 근접 (플레이어 주변 원형 범위 전체 타격, 사거리는 Melee 클래스의 attack_range) -----
    "melee":  {"name": "나무 방망이", "dmg": 36, "rate": 2.8,  "color": (139, 69, 19)},  # DPS 101  범위 110
    "katana": {"name": "카타나",      "dmg": 26, "rate": 4.0,  "color": (255, 215, 0)},  # DPS 104  범위 120
    "axe":    {"name": "도끼",        "dmg": 65, "rate": 1.5,  "color": (139, 35, 69)},  # DPS 98   범위 125, 강한 넉백
    "spear":  {"name": "창",          "dmg": 36, "rate": 2.0,  "color": (128, 128, 0)},  # DPS 72   범위 165 (가장 김)
    "hammer": {"name": "해머",        "dmg": 80, "rate": 1.25, "color": (192, 192, 192)},  # DPS 100  범위 155, 가장 강한 넉백
    "gloves": {"name": "글로브",      "dmg": 18, "rate": 5.0,  "color": (255, 192, 203)},  # DPS 90   범위 100
}

# 우클릭 스킬 기본 쿨타임(ms) - "스킬 쿨타임 감소" 업그레이드가 모든 무기에 똑같이 적용됨
SKILL_COOLDOWNS = {
    "melee": 8000, "katana": 6000, "axe": 12000, "spear": 8000, "hammer": 12000, "gloves": 15000,
    "glock": 80000, "machinegun": 18000, "shotgun": 10000, "sniper": 12000, "plasma": 18000, "rocket": 15000,
}

# 카타나 일섬: 끝난 뒤 무적 시간(프레임), 연속 처치(쿨 초기화) 1회당 데미지 증가
KATANA_DASH_INVULN_FRAMES = 12   # 0.2초
KATANA_CHAIN_BONUS = 0.05        # 연속 1회당 +5%
KATANA_DASH_EXP_RATIO = 0.75     # 일섬으로 처치한 좀비의 경험치 비율 (75%)
KATANA_CHAIN_WINDOW = 60         # 연참: 쿨타임 초기화 후 1초 안에 다시 쓰지 않으면 스택 초기화
KATANA_KILL_HEAL = 1             # 일섬으로 처치한 좀비 1마리당 체력 회복
KATANA_CHAIN_UPGRADE = 0.03      # "연참 데미지" 업그레이드 1회당 스택당 보너스 +3%
KATANA_DASH_UPGRADE_BONUS = 0.10 # "카타나 데미지 +3" 강화 1회당 일섬 데미지 추가 +10% (공격력 증가와 별도로)
# 오의 연섬 (카타나 패시브, 레벨 6부터 업그레이드로 1회 획득): 일섬 피해의 25%를 고정 피해로 바꿈
#  고정 피해 = max(떼어낸 25%, 대상 최대 체력의 6%) - 갑옷/방패/수호 오라 감소를 무시
KATANA_OUGI_RATIO = 0.25
KATANA_OUGI_HP_RATIO = 0.06
KATANA_OUGI_MIN_LEVEL = 6

# 도끼 대회전 베기: 크게 한 바퀴 휘두름 (반경 190, 데미지 3.5배) / 흡혈 (준 피해의 10%, 한 번에 최대 100) / 넉백 20
AXE_SKILL_RADIUS = 190
AXE_SKILL_DAMAGE_MULT = 3.5
AXE_SKILL_LIFESTEAL = 0.10
AXE_SKILL_LIFESTEAL_CAP = 100
AXE_SKILL_KNOCKBACK = 20
# 글록 항공 폭격 (쿨타임 80초): 폭탄 1발 기본 데미지 1000, 공격력이 오른 만큼 같은 비율로 증가
#  (폭탄 데미지 = 1000 × 현재 공격력 / 글록 기본 공격력)
#  "폭격 범위" 업그레이드 1회당: 폭격 길이 +100px, 폭발 반경(폭) +15px
GLOCK_STRIKE_BASE_DAMAGE = 1000
# 창: 데미지가 이동속도에 비례 (기본 속도 7 기준) / 들고 달리면 정면 좀비에게 돌진 피해 + 넉백 / 스킬 물보라
SPEAR_BASE_SPEED = 7
SPEAR_CHARGE_RATIO = 0.8          # 돌진 피해 = 현재 창 공격력의 80%
SPEAR_CHARGE_REACH = 100          # 정면 이 거리 안
SPEAR_CHARGE_HALF_ARC = 40        # 이동 방향 ± 이 각도
SPEAR_CHARGE_COOLDOWN_MS = 500    # 같은 좀비는 0.5초에 한 번
SPEAR_CHARGE_KNOCKBACK = 14
SPLASH_RADIUS = 230               # 물보라 기본 반경 ("물보라 범위 +30px" 업그레이드)
SPLASH_DAMAGE_MULT = 2.0
SPLASH_KNOCKBACK = 16
SPLASH_SLOW = 0.5                 # 둔화 배율 (0.5 = 이동속도 50%, "물보라 둔화 +8%" 업그레이드로 더 느리게)
SPLASH_SLOW_FRAMES = 180          # 3초
# 저격총 도탄 사격: 맞을 때마다 공격력 3배, 기본 10번 튕김 ("도탄 +3회" 업그레이드 1회당 +3번)
SNIPER_RICOCHET_DAMAGE_MULT = 3.0
SNIPER_RICOCHET_BOUNCES = 10
SNIPER_RICOCHET_UPGRADE = 3
# 치명타 피해 배율: 기본 1.3배, 저격총 전용 "치명타 데미지 +25%" 업그레이드 1회당 +0.25 (최대 10회 = 3.8배)
CRIT_BASE_MULT = 1.3
SNIPER_CRIT_DAMAGE_UPGRADE = 0.25
SNIPER_CRIT_DAMAGE_MAX = 10
SNIPER_RICOCHET_CRIT_BONUS = 0.20   # 도탄 사격은 치명타 확률 +20% (치명타 업그레이드가 없어도 터짐)
GLOCK_STRIKE_RANGE_LENGTH = 100
GLOCK_STRIKE_RANGE_WIDTH = 15
GLOCK_STRIKE_LENGTH = 850


def tick_katana_chain(player):
    """연참 유지 시간 감소 - 1초 안에 일섬을 다시 쓰지 않으면 스택 초기화"""
    if player.katana_chain > 0:
        player.katana_chain_timer -= 1
        if player.katana_chain_timer <= 0:
            player.katana_chain = 0
            fx.add_text(player.rect.centerx, player.rect.top - 30, "연참 끊김", (160, 160, 180))


def get_katana_chain_bonus(player):
    """연참 스택 1개당 데미지 보너스 (기본 5% + 연참 데미지 업그레이드)"""
    return KATANA_CHAIN_BONUS + KATANA_CHAIN_UPGRADE * player.skill_upgrades["katana"].get("chain", 0)

# 투사체 관통 업그레이드 최대 레벨
MAX_PIERCE_LEVEL = 10

# "폭발 공격" 업그레이드: 주변 피해 비율과 최소 간격(프레임) - 연사 무기로 매 발 터지지 않도록
EXPLOSION_SKILL_RATIO = 0.3
EXPLOSION_SKILL_RATIO_MELEE = 0.12   # 근접 무기(일섬 포함)는 한 번에 여러 마리를 때려서 폭발 피해를 더 낮춤 (30% → 12%)
EXPLOSION_SKILL_COOLDOWN = 12

# ===== 아이템 드롭 =====
ITEM_DROP_CHANCE = 0.03        # 일반 좀비 처치 시 드롭 확률 (3%)
BOSS_ITEM_DROP_CHANCE = 0.5    # 보스/거대 좀비 처치 시 드롭 확률 (50%)
ITEM_LIFETIME_FRAMES = 600     # 바닥에 떨어진 아이템 유지 시간 10초 (일시정지 중에는 줄지 않음)
ITEM_BUFF_FRAMES = 600         # 공격력/이동속도 버프 지속 시간 10초
ITEM_BUFF_MULTIPLIER = 1.3     # 버프 효과 +30%
ITEM_HEAL_AMOUNT = 25
ITEM_COLORS = {"health": RED, "damage": YELLOW, "speed": CYAN}
ITEM_ICON_LABELS = {"health": "체", "damage": "공", "speed": "속"}
# 보스/거대 좀비 (아이템 드롭률 50%, 체력 1.6배) - 다른 좀비가 소환한 개체는 제외
GUARANTEED_DROP_TYPES = {"boss", "paladin", "demon", "angel", "dragon", "king", "god",
                         "colossus", "titan", "giant", "behemoth", "leviathan", "elder"}

# 게임 상태
clock = pygame.time.Clock()
FPS = 60
font_large = pygame.font.SysFont('malgun gothic', 48)
font_small = pygame.font.SysFont('malgun gothic', 36)
font_medium = pygame.font.SysFont('malgun gothic', 28)
font_desc = pygame.font.SysFont('malgun gothic', 20)
font_control = pygame.font.SysFont('malgun gothic', 24)
font_item_info = pygame.font.SysFont('malgun gothic', 20)
font_item_icon = pygame.font.SysFont('malgun gothic', 14, bold=True)


# ===== UI 공통 (배경 / 패널 / 카드 / 게이지) - 모든 메뉴와 HUD가 같은 모양을 쓰도록 =====
font_title = pygame.font.SysFont('malgun gothic', 54, bold=True)
font_hud_big = pygame.font.SysFont('malgun gothic', 32, bold=True)
font_hud = pygame.font.SysFont('malgun gothic', 19, bold=True)
font_tiny = pygame.font.SysFont('malgun gothic', 15)

UI_TEXT = (245, 240, 232)      # 크림색 글자
UI_SUB = (178, 170, 158)
UI_DIM = (120, 113, 104)
UI_PANEL = (30, 28, 26)       # 따뜻한 숯색 패널
UI_BORDER = (78, 72, 64)
UI_ACCENT = (217, 119, 87)    # Claude 코랄
UI_DANGER = (228, 92, 78)
UI_GOOD = (128, 196, 132)
UI_EXP = (106, 155, 204)

_ui_cache = {}


def ui_bright(color, minimum=170):
    """어두운 무기/좀비 색도 어두운 배경 위에서 잘 보이도록 밝게"""
    peak = max(color[:3])
    if peak >= minimum:
        return tuple(color[:3])
    if peak == 0:
        return (minimum, minimum, minimum)
    scale = minimum / peak
    return tuple(min(255, int(c * scale + 25)) for c in color[:3])


def ui_text(surface, text, font, color, pos, anchor="topleft", shadow=True):
    """글자 그리기 (그림자 포함) → 그려진 영역"""
    text = str(text)
    surf, w, h = _render_cached(font, text, color, shadow)
    rect = pygame.Rect(0, 0, w, h)
    setattr(rect, anchor, (int(pos[0]), int(pos[1])))
    surface.blit(surf, rect.topleft)
    return rect


_text_cache = {}


def _render_cached(font, text, color, shadow=False):
    """같은 글자는 다시 그리지 않고 재사용 (좀비 이름표/HUD 글자가 매 프레임 수백 개라 느려지는 것 방지)
    그림자가 있으면 글자+그림자를 한 장으로 합쳐 둠 → (이미지, 글자 폭, 글자 높이)"""
    key = (id(font), text, tuple(color), shadow)
    entry = _text_cache.get(key)
    if entry is None:
        if len(_text_cache) > 3000:
            _text_cache.clear()
        base = font.render(text, True, color)
        w, h = base.get_size()
        if shadow:
            merged = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
            merged.blit(font.render(text, True, (0, 0, 0)), (2, 2))
            merged.blit(base, (0, 0))
            base = merged
        entry = _text_cache[key] = (base, w, h)
    return entry


def ui_wrap(text, font, width):
    """폭에 맞춰 줄바꿈 (띄어쓰기 기준, 너무 긴 단어는 글자 단위)"""
    lines = []
    for paragraph in str(text).split("\n"):
        line = ""
        for word in paragraph.split(" "):
            candidate = word if not line else line + " " + word
            if font.size(candidate)[0] <= width:
                line = candidate
                continue
            if line:
                lines.append(line)
            line = ""
            for ch in word:
                if font.size(line + ch)[0] > width and line:
                    lines.append(line)
                    line = ""
                line += ch
        lines.append(line)
    return lines


def ui_panel(surface, rect, alpha=215, fill=UI_PANEL, border=UI_BORDER, radius=12, width=1):
    """반투명 둥근 패널"""
    rect = pygame.Rect(rect)
    key = ("panel", rect.size, fill, alpha, radius)
    panel = _ui_cache.get(key)
    if panel is None:
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (*fill, alpha), panel.get_rect(), border_radius=radius)
        if len(_ui_cache) > 400:
            _ui_cache.clear()
        _ui_cache[key] = panel
    surface.blit(panel, rect.topleft)
    if border:
        pygame.draw.rect(surface, border, rect, width, border_radius=radius)
    return rect


def ui_overlay(surface, alpha=170, color=(4, 5, 10)):
    key = ("overlay", surface.get_size(), alpha, color)
    overlay = _ui_cache.get(key)
    if overlay is None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((*color, alpha))
        _ui_cache[key] = overlay
    surface.blit(overlay, (0, 0))


def ui_bar(surface, rect, ratio, color, back=(48, 20, 24), label=None, font=None, radius=6, label_color=None):
    """둥근 게이지 (윗부분 하이라이트 + 테두리, 가운데 글자)"""
    rect = pygame.Rect(rect)
    ratio = max(0.0, min(1.0, ratio))
    pygame.draw.rect(surface, back, rect, border_radius=radius)
    if ratio > 0:
        fill = rect.copy()
        fill.width = max(min(rect.width, radius * 2), int(rect.width * ratio))
        pygame.draw.rect(surface, color, fill, border_radius=radius)
        if rect.height >= 10:
            shine = pygame.Rect(fill.x + 3, fill.y + 2, max(0, fill.width - 6), max(2, rect.height // 4))
            pygame.draw.rect(surface, tuple(min(255, c + 70) for c in color), shine, border_radius=radius)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2, border_radius=radius)
    if label:
        if label_color:
            ui_text(surface, label, font or font_hud, label_color, rect.center, "center", shadow=False)
        else:
            ui_text(surface, label, font or font_hud, UI_TEXT, rect.center, "center")


def ui_background(surface):
    """메뉴 배경: 어두운 그라데이션 + 격자 + 가장자리 어둡게 + 떠오르는 불씨"""
    w, h = surface.get_size()
    key = ("bg", w, h)
    bg = _ui_cache.get(key)
    if bg is None:
        bg = pygame.Surface((w, h))
        for y in range(h):
            t = y / max(1, h - 1)
            pygame.draw.line(bg, (int(24 + 16 * t), int(23 + 7 * t), int(21 + 4 * t)), (0, y), (w, y))
        for x in range(0, w, 48):
            pygame.draw.line(bg, (36, 34, 31), (x, 0), (x, h))
        for y in range(0, h, 48):
            pygame.draw.line(bg, (36, 34, 31), (0, y), (w, y))
        small = pygame.Surface((64, 36), pygame.SRCALPHA)
        for sy in range(36):
            for sx in range(64):
                d = math.hypot((sx - 31.5) / 32, (sy - 17.5) / 18)
                small.set_at((sx, sy), (0, 0, 0, int(max(0.0, min(1.0, (d - 0.45) / 0.6)) * 220)))
        bg.blit(pygame.transform.smoothscale(small, (w, h)), (0, 0))
        _ui_cache[key] = bg
    surface.blit(bg, (0, 0))
    t = pygame.time.get_ticks()
    for i in range(36):
        x = (i * 137 + t * 0.012 * (1 + i % 3)) % w
        y = h - (i * 211 + t * 0.03 * (1 + i % 4)) % (h + 40)
        glow = 120 + (i * 37) % 120
        pygame.draw.circle(surface, (glow, int(glow * 0.55), int(glow * 0.4)), (int(x), int(y)), 1 + i % 3)


def ui_title(surface, text, y, sub=None, color=UI_TEXT):
    """화면 제목 (가운데) + 강조 밑줄 + 부제목"""
    rect = ui_text(surface, text, font_title, color, (surface.get_width() // 2, int(y)), "midtop")
    pygame.draw.rect(surface, UI_ACCENT, (rect.centerx - 60, rect.bottom + 4, 120, 4), border_radius=2)
    bottom = rect.bottom + 12
    if sub:
        bottom = ui_text(surface, sub, font_desc, UI_SUB, (rect.centerx, bottom + 4), "midtop", shadow=False).bottom
    return bottom


def ui_card(surface, rect, accent, hover=False, title="", lines=(), badge=None, title_font=None, title_color=UI_TEXT, line_font=None):
    """선택 카드: 왼쪽 색 띠 + 제목 + 설명 줄들. 마우스를 올리면 살짝 떠오르고 빛남.
    lines: 문자열 또는 (문자열, 색) 목록"""
    rect = pygame.Rect(rect)
    accent = ui_bright(accent)
    if hover:
        rect = rect.move(0, -4)
        glow = pygame.Surface((rect.w + 20, rect.h + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*accent, 55), glow.get_rect(), border_radius=18)
        surface.blit(glow, (rect.x - 10, rect.y - 10))
        fill = tuple(int(c * 0.20 + 16) for c in accent)
    else:
        fill = UI_PANEL
    ui_panel(surface, rect, alpha=235, fill=fill, border=accent if hover else UI_BORDER, width=2 if hover else 1)
    pygame.draw.rect(surface, accent, (rect.x + 6, rect.y + 10, 4, rect.h - 20), border_radius=2)
    x, y = rect.x + 20, rect.y + 10
    if badge:
        ui_text(surface, badge, font_tiny, accent if hover else UI_DIM, (rect.right - 10, rect.bottom - 6), "bottomright", shadow=False)
    if title:
        y = ui_text(surface, title, title_font or font_medium, title_color, (x, y)).bottom + 4
    line_font = line_font or font_desc
    for entry in lines:
        text, color = (entry, UI_SUB) if isinstance(entry, str) else entry
        for line in ui_wrap(text, line_font, rect.w - 32):
            if y + line_font.get_height() > rect.bottom - 2:
                break
            y = ui_text(surface, line, line_font, color, (x, y), shadow=False).bottom + 1
    return rect


def ui_button(surface, rect, label, accent, hover=False, desc=None):
    """가로로 긴 메뉴 버튼 (제목 + 설명)"""
    return ui_card(surface, rect, accent, hover, label, [desc] if desc else (), line_font=font_tiny)


def ui_snapshot():
    """지금 화면을 그대로 복사 (메뉴 뒤에 게임 화면이 비쳐 보이게)"""
    return screen.copy()


def ui_quit_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


# ===== 시각 효과 (파티클 / 데미지 숫자 / 화면 흔들림 / 피격 테두리) =====
# 이펙트용 난수는 게임용 random과 따로 써서, 연출이 게임 결과(좀비 종류·치명타 등)를 바꾸지 않게 함
fx_random = random.Random()

font_damage = pygame.font.SysFont('malgun gothic', 18, bold=True)
font_damage_big = pygame.font.SysFont('malgun gothic', 26, bold=True)

# 무기별 타격/총구 화염 색
FX_WEAPON_COLORS = {
    "glock": (255, 230, 90), "shotgun": (255, 170, 50), "sniper": (230, 235, 255), "machinegun": (255, 130, 70),
    "plasma": (90, 255, 255), "rocket": (255, 150, 40), "spear": (130, 210, 255), "gloves": (255, 170, 200),
    "melee": (230, 170, 90), "katana": (210, 230, 255), "axe": (255, 120, 120), "hammer": (230, 230, 230),
}
# 속성탄 색 (화염 / 얼음 / 전기)
ELEMENT_COLORS = {
    "fire": [(255, 120, 20), (255, 200, 60)],
    "ice": [(140, 220, 255), (230, 250, 255)],
    "electric": [(255, 245, 110), (190, 220, 255)],
}

# 총알 꼬리 (색, 크기, 수명 프레임)
FX_TRAILS = {
    "rocket": ((150, 150, 150), 5, 20),
    "plasma": ((90, 255, 255), 3, 9),
    "sniper": ((220, 225, 255), 2, 7),
    "dragon_fireball": ((255, 130, 30), 4, 12),
    "giant_rock": ((140, 120, 100), 4, 14),
    "zombie_snipe": ((255, 70, 70), 3, 10),
    "javelin": ((240, 230, 160), 3, 10),
}


class EffectManager:
    """가벼운 파티클/글자 효과 관리 (스프라이트 대신 리스트로 관리해서 많이 띄워도 가벼움)"""
    MAX_PARTICLES = 800
    MAX_TEXTS = 80

    def __init__(self):
        self.text_cache = {}
        self.reset()

    def reset(self):
        # 파티클: [x, y, vx, vy, 남은수명, 전체수명, 크기, 색, 중력, 감속]
        self.particles = []
        # 글자: [x, y, vy, 남은수명, 전체수명, surface]
        self.texts = []
        self.shake = 0.0
        self.hurt = 0.0
        self.frame = 0
        self.elements = []  # 플레이어가 가진 속성탄 ("fire", "ice", "electric") - 총알 꼬리 색에 사용

    # ----- 파티클 -----
    def burst(self, x, y, color, count, speed=(1.0, 4.0), size=(2, 4), life=(14, 28),
              gravity=0.0, drag=0.9, angle=None, spread=math.pi * 2):
        rnd = fx_random
        for _ in range(int(count)):
            a = rnd.uniform(0, math.pi * 2) if angle is None else angle + rnd.uniform(-spread / 2, spread / 2)
            sp = rnd.uniform(*speed)
            lf = rnd.randint(int(life[0]), int(life[1]))
            self.particles.append([x, y, math.cos(a) * sp, math.sin(a) * sp, lf, lf,
                                   rnd.uniform(*size), color, gravity, drag])
        if len(self.particles) > self.MAX_PARTICLES:
            del self.particles[:len(self.particles) - self.MAX_PARTICLES]

    def hit_spark(self, x, y, color):
        self.burst(x, y, color, 5, speed=(2.0, 5.5), size=(1.5, 3), life=(6, 12), drag=0.82)

    def muzzle_flash(self, x, y, dir_x, dir_y, color):
        angle = math.atan2(dir_y, dir_x)
        self.burst(x, y, (255, 255, 225), 1, speed=(0, 0), size=(7, 9), life=(3, 4))   # 섬광
        self.burst(x, y, color, 5, speed=(2.5, 6.5), size=(1.5, 2.5), life=(4, 8), drag=0.8, angle=angle, spread=0.8)

    def death_burst(self, x, y, color, size):
        count = min(40, 10 + size // 3)
        self.burst(x, y, color, count, speed=(1.5, 5.5), size=(2, 5), life=(18, 34), drag=0.88)
        dark = tuple(max(0, c // 2) for c in color)
        self.burst(x, y, dark, count // 2, speed=(0.5, 2.5), size=(3, 6), life=(24, 40), drag=0.85)

    def ring(self, x, y, color, radius, count=24, size=3):
        # 바깥으로 퍼지는 고리
        speed = radius / 7.3  # 수명(16프레임)·감속(0.9) 동안 정확히 radius까지 퍼지도록
        for i in range(count):
            a = i / count * math.pi * 2
            self.particles.append([x, y, math.cos(a) * speed, math.sin(a) * speed, 16, 16, size, color, 0, 0.9])

    def explosion_debris(self, x, y, radius):
        count = min(40, 8 + radius // 5)
        self.burst(x, y, (255, 205, 90), count, speed=(radius / 40, radius / 13), size=(2, 5), life=(14, 26), drag=0.86)
        self.burst(x, y, (85, 85, 85), count // 2, speed=(radius / 60, radius / 22), size=(4, 8), life=(26, 44),
                   drag=0.9, gravity=-0.05)

    def lightning(self, x1, y1, x2, y2, color=(190, 220, 255)):
        """두 지점을 잇는 지그재그 번개 줄기"""
        dist = math.hypot(x2 - x1, y2 - y1)
        steps = max(3, int(dist / 12))
        for i in range(steps + 1):
            t = i / steps
            jitter = 0 if i in (0, steps) else 7
            x = x1 + (x2 - x1) * t + fx_random.uniform(-jitter, jitter)
            y = y1 + (y2 - y1) * t + fx_random.uniform(-jitter, jitter)
            self.particles.append([x, y, 0, 0, 8, 8, 3.5, color, 0, 1.0])
            self.particles.append([x, y, 0, 0, 6, 6, 1.5, WHITE, 0, 1.0])

    def element_hit(self, x, y, element):
        """속성탄이 맞은 자리 효과"""
        if element == "fire":
            self.burst(x, y, (255, 140, 30), 7, speed=(1.0, 3.5), size=(2, 4), life=(10, 20), drag=0.88, gravity=-0.12)
        elif element == "ice":
            self.burst(x, y, (170, 230, 255), 7, speed=(1.5, 4.0), size=(1.5, 3), life=(10, 18), drag=0.85)
            self.burst(x, y, WHITE, 3, speed=(0.5, 2.0), size=(1, 2), life=(12, 20), drag=0.9)
        elif element == "electric":
            self.burst(x, y, (255, 245, 110), 6, speed=(3.0, 6.0), size=(1.5, 2.5), life=(4, 9), drag=0.75)

    def trail(self, x, y, color, size=3, life=10):
        self.particles.append([x + fx_random.uniform(-1.5, 1.5), y + fx_random.uniform(-1.5, 1.5),
                               0, 0, life, life, size, color, 0, 1.0])

    # ----- 떠오르는 글자 (데미지 숫자 등) -----
    def add_text(self, x, y, text, color, big=False, life=40):
        key = (text, color, big)
        surf = self.text_cache.get(key)
        if surf is None:
            font = font_damage_big if big else font_damage
            body = font.render(text, True, color)
            outline = font.render(text, True, BLACK)
            # 검은 테두리를 둘러서 어떤 배경에서도 잘 보이게
            surf = pygame.Surface((body.get_width() + 2, body.get_height() + 2), pygame.SRCALPHA)
            for ox, oy in ((0, 1), (2, 1), (1, 0), (1, 2)):
                surf.blit(outline, (ox, oy))
            surf.blit(body, (1, 1))
            if len(self.text_cache) > 400:
                self.text_cache.clear()
            self.text_cache[key] = surf
        self.texts.append([x + fx_random.uniform(-8, 8), y, -1.6 if big else -1.2, life, life, surf])
        if len(self.texts) > self.MAX_TEXTS:
            del self.texts[:len(self.texts) - self.MAX_TEXTS]

    def add_damage_text(self, x, y, amount, crit=False):
        if crit:
            self.add_text(x, y, f"{amount:.0f}!", (255, 220, 60), big=True, life=50)
        else:
            self.add_text(x, y, f"{amount:.0f}", WHITE)

    # ----- 화면 흔들림 / 피격 붉은 테두리 -----
    def add_shake(self, amount):
        self.shake = min(16.0, max(self.shake, amount))

    def add_hurt(self, amount):
        self.hurt = min(1.0, self.hurt + amount)

    def shake_offset(self):
        if self.shake <= 0:
            return 0, 0
        return fx_random.uniform(-self.shake, self.shake), fx_random.uniform(-self.shake, self.shake)

    def update(self):
        self.frame += 1
        alive = []
        for p in self.particles:
            p[4] -= 1
            if p[4] <= 0:
                continue
            p[2] *= p[9]
            p[3] = p[3] * p[9] + p[8]
            p[0] += p[2]
            p[1] += p[3]
            alive.append(p)
        self.particles = alive
        texts = []
        for t in self.texts:
            t[3] -= 1
            if t[3] <= 0:
                continue
            t[1] += t[2]
            t[2] *= 0.94
            texts.append(t)
        self.texts = texts
        self.shake = self.shake * 0.85 if self.shake > 0.3 else 0.0
        self.hurt = max(0.0, self.hurt - 0.035)

    def draw(self, surface, camera):
        width, height = camera.width, camera.height
        for x, y, _vx, _vy, life, max_life, size, color, _g, _d in self.particles:
            sx, sy = camera.apply(x, y)
            if -10 < sx < width + 10 and -10 < sy < height + 10:
                radius = size * (0.35 + 0.65 * life / max_life)  # 수명이 줄수록 작아짐
                pygame.draw.circle(surface, color, (int(sx), int(sy)), max(1, int(radius)))
        for x, y, _vy, life, max_life, surf in self.texts:
            sx, sy = camera.apply(x, y)
            fade_start = max_life * 0.4
            surf.set_alpha(255 if life > fade_start else int(255 * life / fade_start))
            surface.blit(surf, (int(sx - surf.get_width() / 2), int(sy - surf.get_height() / 2)))
            surf.set_alpha(255)


fx = EffectManager()
_hurt_overlay = None


def draw_hurt_overlay(surface, strength):
    """피격 시 화면 가장자리를 붉게"""
    global _hurt_overlay
    if strength <= 0.02:
        return
    w, h = surface.get_size()
    if _hurt_overlay is None or _hurt_overlay.get_size() != (w, h):
        _hurt_overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        band = max(1, min(60, w // 2, h // 2))
        for i in range(band):
            alpha = int(170 * (1 - i / band) ** 2)
            pygame.draw.rect(_hurt_overlay, (255, 0, 0, alpha), (i, i, w - 2 * i, h - 2 * i), 1)
    _hurt_overlay.set_alpha(int(255 * min(1.0, strength)))
    surface.blit(_hurt_overlay, (0, 0))


def get_alpha_images(sprite):
    """회전해도 네모난 모서리가 생기지 않는 투명 배경 이미지 + 피격 시 하얀 실루엣 (이미지가 바뀌면 다시 만듦)"""
    img = sprite.image
    w, h = img.get_size()
    key = (id(img), w, h, tuple(img.get_at((w // 2, h // 2))))
    if getattr(sprite, "_alpha_key", None) != key:
        sprite._alpha_key = key
        sprite._alpha_image = img.convert_alpha()
        flash = sprite._alpha_image.copy()
        flash.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
        sprite._flash_image = flash
    return sprite._alpha_image, sprite._flash_image


_spear_art_cache = {}


def draw_spear_art(length, thickness):
    """창 그림 (오른쪽을 향함): 짙은 푸른 자루 + 감은 끈 + 금빛 고리 + 잎 모양 강철 날 + 물빛 리본"""
    key = (int(length), int(thickness))
    art = _spear_art_cache.get(key)
    if art is not None:
        return art
    t = max(2, int(thickness))
    h = t * 5
    art = pygame.Surface((int(length), h), pygame.SRCALPHA)
    cy = h // 2
    blade_start = int(length * 0.68)
    pygame.draw.rect(art, (32, 55, 92), (0, cy - t // 2, blade_start + 2, t), border_radius=max(1, t // 2))          # 자루
    pygame.draw.line(art, (70, 105, 150), (0, cy - t // 2 + 1), (blade_start, cy - t // 2 + 1), max(1, t // 3))     # 자루 윗면 빛
    for x in range(int(length * 0.06), int(length * 0.3), max(4, t + 2)):                                           # 손잡이 끈
        pygame.draw.line(art, (150, 120, 70), (x, cy - t // 2), (x + t // 2, cy + t // 2), max(1, t // 3))
    pygame.draw.rect(art, (230, 185, 70), (blade_start - t, cy - t, t + 2, t * 2), border_radius=max(1, t // 2))     # 금빛 고리
    for sign in (-1, 1):                                                                                              # 물빛 리본
        pygame.draw.polygon(art, (80, 170, 255), [(blade_start - t, cy + sign * t // 2),
                                                  (blade_start - t * 5, cy + sign * t * 2),
                                                  (blade_start - t * 3, cy + sign * t // 2)])
    blade = [(blade_start, cy - int(t * 1.1)), (int(length * 0.85), cy - int(t * 1.9)), (int(length) - 1, cy),
             (int(length * 0.85), cy + int(t * 1.9)), (blade_start, cy + int(t * 1.1))]
    pygame.draw.polygon(art, (195, 215, 235), blade)                                                                 # 날
    pygame.draw.polygon(art, (90, 125, 165), blade, max(1, t // 3))
    pygame.draw.line(art, (245, 252, 255), (blade_start + t, cy), (int(length) - t, cy), max(1, t // 3))            # 날 가운데 선
    _spear_art_cache[key] = art
    return art


def draw_shadow(surface, sx, sy, width, height):
    shadow_w = max(10, int(width * 0.95))
    shadow_h = max(4, int(width * 0.3))
    pygame.draw.ellipse(surface, (18, 18, 18), (int(sx - shadow_w / 2), int(sy + height / 2 - shadow_h / 2), shadow_w, shadow_h))


def draw_eyes(surface, cx, cy, width, height, look_x, look_y, color=WHITE):
    eye_r = max(2, int(min(width, height) / 9))
    gap = max(eye_r + 1, int(width * 0.22))
    ey = cy - height * 0.18
    dist = math.hypot(look_x, look_y) or 1
    px, py = look_x / dist * eye_r * 0.55, look_y / dist * eye_r * 0.55
    for side in (-1, 1):
        ex = cx + side * gap
        pygame.draw.circle(surface, color, (int(ex), int(ey)), eye_r)
        pygame.draw.circle(surface, BLACK, (int(ex + px), int(ey + py)), max(1, eye_r // 2))


_zombie_body_cache = {}
EYE_DIRECTIONS = 16      # (눈을 몸 이미지에 같이 그릴 때의 방향 수 - 지금은 눈을 따로 그림)


def _zombie_body(zombie, image, angle, frozen, flicker, sparking, stealth, eye_dir=None):
    """좀비 몸 이미지 (회전 + 얼음/불/전기 색 + 은신 투명도)
    같은 종류·크기·색의 좀비끼리 같이 쓰고, 같은 조합은 한 번만 만듦 (예전: 좀비마다 매 프레임 회전/색칠)"""
    w, h = zombie.rect.size
    key = (zombie.zombie_type, image.get_size(), zombie._alpha_key[3], image is zombie._flash_image,
           angle, frozen, flicker, sparking, stealth, eye_dir, w, h)
    surf = _zombie_body_cache.get(key)
    if surf is None:
        if len(_zombie_body_cache) > 6000:
            _zombie_body_cache.clear()
        surf = pygame.transform.rotate(image, angle)
        if frozen:
            surf.fill((130, 190, 255), special_flags=pygame.BLEND_RGB_MULT)
            surf.fill((50, 80, 120), special_flags=pygame.BLEND_RGB_ADD)
        if flicker is not None:
            surf.fill((110 + flicker, 45, 0), special_flags=pygame.BLEND_RGB_ADD)
        if sparking:
            surf.fill((120, 120, 40), special_flags=pygame.BLEND_RGB_ADD)
        if eye_dir is not None:
            a = eye_dir / EYE_DIRECTIONS * 2 * math.pi
            draw_eyes(surf, surf.get_width() / 2, surf.get_height() / 2, w, h, math.cos(a), math.sin(a))
        if stealth:
            surf.set_alpha(40)
        _zombie_body_cache[key] = surf
    return surf


def draw_zombie_sprite(surface, camera, zombie, player):
    """좀비: 걸을 때 위아래로 흔들리고 몸을 기울이며, 눈은 플레이어를 바라봄 (그리기 전용, 판정은 그대로)"""
    sx, sy = camera.apply(zombie.rect.centerx, zombie.rect.centery)
    w, h = zombie.rect.size
    if not (-w - 80 < sx < camera.width + w + 80 and -h - 80 < sy < camera.height + h + 80):
        return
    base, flash = get_alpha_images(zombie)
    walk = fx.frame * 0.12 * (0.7 + min(zombie.speed * zombie.slow_multiplier, 6) * 0.25) + zombie.anim_phase
    bob = abs(math.sin(walk)) * (2 + h * 0.03)
    tilt = math.sin(walk) * 5
    if getattr(zombie, "is_charging", False) or getattr(zombie, "dragon_charging", False):
        tilt *= 2.5  # 돌진 중에는 더 크게 흔들림
    flashing = zombie.hit_flash > 0
    look_x = player.rect.centerx - zombie.rect.centerx
    look_y = player.rect.centery - zombie.rect.centery
    # 그림자좀비: 플레이어와 멀리 있으면 거의 보이지 않음 (눈만 희미하게)
    stealth = zombie.zombie_type == "shadow" and math.hypot(look_x, look_y) > 250
    # 상태이상 표시: 불타는 중(주황빛 + 불꽃), 느려진 중(푸른빛 + 서리)
    burning = zombie.burn_time > 0
    frozen = zombie.slow_time > 0 and zombie.slow_multiplier < 1.0
    flicker = (25 if fx.frame % 6 < 3 else 0) if burning else None
    electrified = zombie.electric_fx > 0
    if electrified:
        zombie.electric_fx -= 1
    sparking = electrified and fx.frame % 4 < 2  # 번쩍번쩍
    rotated = _zombie_body(zombie, flash if flashing else base, int(round(tilt)), frozen, flicker, sparking, stealth)
    if frozen:
        if fx.frame % 3 == 0:
            fx.burst(zombie.rect.centerx + fx_random.uniform(-w / 2, w / 2), zombie.rect.centery + fx_random.uniform(-h / 2, h / 2),
                     fx_random.choice(ELEMENT_COLORS["ice"]), 1, speed=(0.1, 0.5), size=(1.5, 2.5), life=(14, 22), drag=0.95)
    if burning:
        fx.burst(zombie.rect.centerx + fx_random.uniform(-w / 2.5, w / 2.5), zombie.rect.top + h * fx_random.uniform(0.2, 0.7),
                 fx_random.choice(ELEMENT_COLORS["fire"]), 1, speed=(0.3, 1.2), size=(2, 5), life=(10, 20),
                 drag=0.95, gravity=-0.18)
    if not stealth:
        draw_shadow(surface, sx, sy, w, h)
    center = (int(sx), int(sy - bob))
    surface.blit(rotated, rotated.get_rect(center=center))
    ring_r = int(max(w, h) * 0.75)
    if getattr(zombie, "guard_mult", 1.0) < 1.0:      # 수호 오라 안 (받는 피해 감소)
        pygame.draw.circle(surface, (150, 180, 255), center, ring_r, 2)
    if zombie.zombie_type == "howler":                # 함성 범위 (이 안의 좀비는 이동속도 +30%)
        pulse = 220 - (fx.frame * 3) % 60
        pygame.draw.circle(surface, (200, 120, 40), center, 220, 1)
        pygame.draw.circle(surface, (255, 170, 60), center, pulse, 2)
    elif getattr(zombie, "hasted", False):              # 이동속도 버프 받는 중: 발밑 주황 화살표
        tip_y = center[1] + h // 2 + 6
        pygame.draw.lines(surface, (255, 170, 60), False,
                          [(center[0] - 6, tip_y), (center[0], tip_y - 5), (center[0] + 6, tip_y)], 2)
    if getattr(zombie, "block_hits", 0) > 0:          # 결계 (공격 무효)
        pygame.draw.circle(surface, (190, 160, 255), center, ring_r + 5, 3)
    if frozen:                                        # 얼음 테두리
        pygame.draw.rect(surface, (200, 240, 255), rotated.get_rect(center=center).inflate(-4, -4), 2, border_radius=3)
    if electrified:                                   # 몸 주변으로 튀는 작은 번개
        for _ in range(2):
            a = fx_random.uniform(0, math.pi * 2)
            r1, r2 = max(w, h) * 0.3, max(w, h) * 0.75
            p1 = (center[0] + math.cos(a) * r1, center[1] + math.sin(a) * r1)
            mid = (center[0] + math.cos(a + 0.4) * (r1 + r2) / 2, center[1] + math.sin(a + 0.4) * (r1 + r2) / 2)
            p2 = (center[0] + math.cos(a - 0.1) * r2, center[1] + math.sin(a - 0.1) * r2)
            pygame.draw.lines(surface, (255, 245, 120), False, [p1, mid, p2], 2)
    draw_eyes(surface, sx, sy - bob, w, h, look_x, look_y, color=(90, 70, 110) if stealth else WHITE)
    if getattr(zombie, "aiming", 0) > 0:
        # 저격좀비 조준선: 발사가 가까울수록 굵어지고, 마지막 0.25초는 깜빡임
        tx, ty = camera.apply(zombie.aim_x, zombie.aim_y)
        progress = 1 - zombie.aiming / 72
        if zombie.aiming > 15 or fx.frame % 4 < 2:
            pygame.draw.line(surface, (255, 40, 40), center, (int(tx), int(ty)), 1 + int(progress * 3))
            pygame.draw.circle(surface, (255, 60, 60), (int(tx), int(ty)), 10, 2)


def draw_player_sprite(surface, camera, player):
    """플레이어: 걸을 때 흔들리고, 조준 방향으로 총구/무기가 향함"""
    sx, sy = camera.apply(player.rect.centerx, player.rect.centery)
    w, h = player.rect.size
    if player.is_moving:
        bob = abs(math.sin(player.walk_phase)) * 3
        tilt = math.sin(player.walk_phase) * 4
    else:
        bob = (math.sin(fx.frame * 0.05) + 1) * 0.8  # 가만히 있을 때는 숨쉬듯 살짝
        tilt = 0
    base, flash = get_alpha_images(player)
    image = flash if (player.hurt_flash > 0 and player.hurt_flash % 4 < 2) else base
    rotated = pygame.transform.rotate(image, tilt)
    if getattr(player, "invuln_time", 0) > 0:   # 무적 (일섬 직후): 하늘빛 반투명
        rotated = rotated.copy()
        rotated.fill((90, 140, 160), special_flags=pygame.BLEND_RGB_ADD)
        rotated.set_alpha(150)
    draw_shadow(surface, sx, sy, w, h)
    body_y = sy - bob
    surface.blit(rotated, rotated.get_rect(center=(int(sx), int(body_y))))

    mx, my = pygame.mouse.get_pos()
    aim_x, aim_y = mx - sx, my - body_y
    dist = math.hypot(aim_x, aim_y) or 1
    ux, uy = aim_x / dist, aim_y / dist
    if player.weapon is not None and player.weapon.weapon_type == "spear":
        held = pygame.transform.rotate(draw_spear_art(64, 3), -math.degrees(math.atan2(uy, ux)))
        surface.blit(held, held.get_rect(center=(int(sx + ux * 26), int(body_y + uy * 26))))
    elif player.weapon is not None:
        color = player.weapon.color
        if player.weapon.weapon_type in MELEE_WEAPONS:
            start, end, width = 8, 20, 5     # 손에 든 근접 무기 손잡이
        else:
            start, end, width = 6, 26, 7     # 총구
        p1 = (int(sx + ux * start), int(body_y + uy * start))
        p2 = (int(sx + ux * end), int(body_y + uy * end))
        pygame.draw.line(surface, (20, 20, 20), p1, p2, width + 4)
        pygame.draw.line(surface, color, p1, p2, width)
    draw_eyes(surface, sx, body_y, w, h, aim_x, aim_y)


def fire_muzzle_flash(player, target_x, target_y, kick=0.0):
    """총을 쏠 때 총구 화염 + (강한 무기는) 반동 흔들림"""
    dx = target_x - player.rect.centerx
    dy = target_y - player.rect.centery
    dist = math.hypot(dx, dy) or 1
    ux, uy = dx / dist, dy / dist
    color = FX_WEAPON_COLORS.get(player.weapon.weapon_type, YELLOW)
    fx.muzzle_flash(player.rect.centerx + ux * 28, player.rect.centery + uy * 28, ux, uy, color)
    if kick:
        fx.add_shake(kick)


class DeathFade(pygame.sprite.Sprite):
    """좀비가 쓰러지며 작아지고 사라지는 연출"""
    def __init__(self, zombie):
        super().__init__()
        self.base_image, _ = get_alpha_images(zombie)
        self.frames = 0
        self.duration = 18
        self.spin = fx_random.choice((-1, 1)) * fx_random.uniform(25, 60)
        self.center = zombie.rect.center
        self.image = self.base_image
        self.rect = self.image.get_rect(center=self.center)

    def update(self):
        self.frames += 1
        if self.frames >= self.duration:
            self.kill()
            return
        progress = self.frames / self.duration
        image = pygame.transform.rotozoom(self.base_image, self.spin * progress, 1 - 0.55 * progress)
        image.set_alpha(int(255 * (1 - progress)))
        self.image = image
        self.rect = image.get_rect(center=self.center)


# 카메라 클래스
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        # 화면 흔들림 오프셋 (그리기에만 적용, 마우스 조준 좌표에는 영향 없음)
        self.shake_x = 0
        self.shake_y = 0

    def update(self, target_x, target_y):
        # 카메라가 대상을 화면 중앙에 유지
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2

    def apply(self, x, y):
        # 월드 좌표를 화면 좌표로 변환 (+ 화면 흔들림)
        return x - self.x + self.shake_x, y - self.y + self.shake_y

    def draw_background(self, surface):
        # 그리드 배경 그리기 (무한한 느낌)
        grid_size = 50
        start_x = -(int(self.x - self.shake_x) % grid_size)
        start_y = -(int(self.y - self.shake_y) % grid_size)

        for x in range(start_x, self.width + grid_size, grid_size):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, self.height), 1)
        for y in range(start_y, self.height + grid_size, grid_size):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (self.width, y), 1)

# 아이템 클래스 (좀비 처치 시 드롭)
class Item(pygame.sprite.Sprite):
    EFFECT_TEXTS = {
        "health": f"체력 +{ITEM_HEAL_AMOUNT}",
        "damage": "공격력 +30% (10초)",
        "speed": "이동속도 +30% (10초)",
    }

    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type  # "health", "damage", "speed"
        self.effect = self.EFFECT_TEXTS[item_type]

        # 색깔 아이콘 + 글자 (체/공/속)
        size = 26
        self.base_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.base_image, ITEM_COLORS[item_type], (0, 0, size, size), border_radius=6)
        pygame.draw.rect(self.base_image, WHITE, (0, 0, size, size), 2, border_radius=6)
        label = font_item_icon.render(ITEM_ICON_LABELS[item_type], True, BLACK)
        self.base_image.blit(label, label.get_rect(center=(size // 2, size // 2)))
        self.blank_image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image = self.base_image

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # 프레임 단위 수명 (게임이 진행될 때만 줄어들어서 일시정지/업그레이드 메뉴 중에는 사라지지 않음)
        self.frames_left = ITEM_LIFETIME_FRAMES
        self.bob_phase = fx_random.uniform(0, math.pi * 2)
        self.draw_offset_y = 0

    def update(self):
        self.frames_left -= 1
        if self.frames_left <= 0:
            self.kill()
            return
        self.bob_phase += 0.08
        self.draw_offset_y = math.sin(self.bob_phase) * 4
        # 사라지기 3초 전부터 깜빡임
        if self.frames_left < 180 and (self.frames_left // 10) % 2 == 0:
            self.image = self.blank_image
        else:
            self.image = self.base_image


def maybe_drop_item(zombie_type, x, y, items, all_sprites, summoned=False):
    """좀비 사망 시 아이템 드롭 (일반 좀비 3%, 보스/거대 좀비 50%, 소환된 좀비는 일반 확률)"""
    chance = BOSS_ITEM_DROP_CHANCE if (zombie_type in GUARANTEED_DROP_TYPES and not summoned) else ITEM_DROP_CHANCE
    if random.random() >= chance:
        return None
    item_type = random.choices(["health", "damage", "speed"], weights=[50, 25, 25])[0]
    item = Item(x, y, item_type)
    items.add(item)
    all_sprites.add(item)
    return item

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, ability=None):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # rect는 정수 좌표라 소수점 이동(속도 +0.3, 둔화 등)이 반올림으로 사라지므로 실수 좌표를 따로 보관
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        self._synced_center = self.rect.center
        # 모션/연출용 상태
        self.is_moving = False
        self.walk_phase = 0.0
        self.hurt_flash = 0
        self.speed = 7
        self.health = 100
        self.max_health = 100
        self.damage = 25
        self.ability = ability
        self.weapon = None  # Weapon 객체
        self.last_direction_x = 1
        self.last_direction_y = 0

        # 경험치 시스템
        self.exp = 0
        self.exp_to_level = 100
        self.level = 1
        self.exp_level = 1

        # 무기별 업그레이드
        self.weapon_upgrades = {
            "glock": {"fire_rate": 0, "damage": 0, "ammo": 0},
            "shotgun": {"fire_rate": 0, "damage": 0, "ammo": 0},
            "sniper": {"fire_rate": 0, "damage": 0, "ammo": 0},
            "machinegun": {"fire_rate": 0, "damage": 0, "ammo": 0},
            "plasma": {"fire_rate": 0, "damage": 0, "ammo": 0},
            "rocket": {"fire_rate": 0, "damage": 0, "ammo": 0},
            "melee": {"damage": 0},
            "katana": {"damage": 0},
            "axe": {"damage": 0},
            "spear": {"damage": 0},
            "hammer": {"damage": 0},
            "gloves": {"damage": 0}
        }

        self.levels = {
            "health": 0,
            "speed": 0,
            "damage": 0,
            "regen": 0,
            "crit": 0,
            "dodge": 0,
            "exp_boost": 0,
            "knockback": 0
        }

        # 체력 재생
        self.regen = 0

        # 스킬 시스템
        self.skills = {
            "skill_infinity_ammo": False,
            "skill_piercing": False,
            "skill_fire_bullets": False,
            "skill_ice_bullets": False,
            "skill_electric_bullets": False,
            "skill_auto_aim": False,
            "skill_shield": False,
            "skill_teleport": False,
            "skill_slowdown": False,
            "skill_explosion": False,
        }
        self.shield_active = False  # 방어막 활성화
        self.pierce_level = 0  # 투사체 관통 레벨 (총알이 이 수만큼 좀비를 더 관통)
        self.crit_chance = 0  # 치명타 확률
        self.dodge_chance = 0  # 회피 확률

        self.infinity_ammo_time = 0
        self.explosion_cooldown = 0  # "폭발 공격" 최소 간격
        self.active_skills = []  # 여러 프레임 유지되는 스킬 (대회전 베기, 항공 폭격, 포탑, 블랙홀 등)
        self.rush_time = 0       # 글로브 러시: 남은 시간 동안 공격 속도 3배
        self.invuln_time = 0     # 무적 남은 시간 (카타나 일섬 직후)
        self.katana_chain = 0    # 일섬 연속 처치 횟수 (처치 실패 시 0으로)
        self.katana_chain_timer = 0  # 연참 유지 남은 시간 (0이 되면 스택 초기화)
        # 아이템 버프 남은 시간 (프레임)
        self.damage_buff_time = 0
        self.speed_buff_time = 0
        self.teleport_cooldown = 0
        self.teleport_cooldown_max = 180  # 3초

        # 우클릭 스킬 쿨타임 (무기별)
        self.skill_cooldowns = {
            "melee": 0,
            "katana": 0,
            "axe": 0,
            "spear": 0,
            "hammer": 0,
            "gloves": 0,
            "glock": 0,
            "shotgun": 0,
            "sniper": 0,
            "machinegun": 0,
            "plasma": 0,
            "rocket": 0
        }

        # 스킬 쿨타임 감소 (0~1.0 비율: 0.2 = 20% 감소)
        self.skill_cooldown_reduction = 0

        # 무기별 스킬 업그레이드 효과
        self.skill_upgrades = {
            # 근접 무기
            "melee": {"range": 0, "speed": 0, "damage": 0, "area": 0},  # 범위 확대, 공격속도, 데미지, 광역 범위
            "katana": {"strikes": 0, "speed": 0, "damage": 0, "cooldown": 0, "chain": 0, "ougi": 0},  # 연격 수, 공격속도, 데미지, 쿨타임 감소
            "axe": {"range": 0, "knockback": 0, "damage": 0, "area": 0},  # 범위, 넉백 강화, 데미지, 지진파 범위
            "spear": {"pierces": 0, "speed": 0, "range": 0, "damage": 0},  # 관통 수, 공격속도, 사거리, 데미지
            "hammer": {"range": 0, "damage": 0, "cooldown": 0, "stun": 0},  # 범위, 데미지, 쿨타임, 스턴 효과
            "gloves": {"strikes": 0, "speed": 0, "damage": 0, "combo": 0},  # 연격 수, 공격속도, 데미지, 콤보 게이지
            # 원거리 무기
            "glock": {"burst": 0, "damage": 0, "fire_rate": 0, "accuracy": 0},  # 연사 탄수, 데미지, 발사 속도, 정확도
            "shotgun": {"range": 0, "damage": 0, "spread": 0, "pellets": 3},  # 범위, 데미지, 퍼짐, 펠릿 수(기본 3발)
            "sniper": {"pierces": 0, "damage": 0, "range": 0, "penetration": 0, "crit_damage": 0},  # 관통 수, 데미지, 사거리, 관통력
            "machinegun": {"burst": 0, "fire_rate": 0, "damage": 0},  # 연사 탄수, 연사 속도, 데미지
            "plasma": {"range": 0, "damage": 0, "energy": 0, "explosion": 0},  # 범위, 데미지, 에너지 효율, 폭발 범위
            "rocket": {"count": 0, "damage": 0, "explosion": 0, "tracking": 0}  # 로켓 수, 데미지, 폭발 범위, 유도 기능
        }

        # 획득한 업그레이드 추적 (중복 허용: 스택 표시/제한 체크에 사용)
        self.obtained_upgrades = []

        # 좀비 능력에 의한 상태 이상
        self.poison_time = 0  # poison 좀비에 의한 독 지속 시간
        self.poison_damage_cooldown = 0  # 독 데미지 쿨타임
        self.pool_damage_cooldown = 0  # 독 장판 데미지 쿨타임 (독 상태와 따로 계산)
        self.shock_time = 0    # 감전 (스파크좀비/번개의 천사): 남은 시간 동안 공격 불가
        self.corrode_time = 0  # 부식 (산성좀비): 남은 시간 동안 받는 피해 +30%
        self.slow_time = 0  # ice 좀비에 의한 둔화 지속 시간
        self.slow_multiplier = 1.0  # 속도 감소 배수

        # 능력에 따른 초기 설정
        if ability == "speed":
            self.speed = 10
            self.max_health = 80
            self.health = 80  # 현재 체력이 최대 체력(80)보다 크게 시작하던 문제 수정
        elif ability == "tank":
            self.max_health = 150
            self.health = 150
            self.speed = 5
        elif ability == "damage":
            self.damage = 40
            self.max_health = 90
            self.health = 90

    def update(self):
        # 순간이동 등으로 rect가 외부에서 바뀌었으면 실수 좌표를 다시 맞춤
        if self.rect.center != self._synced_center:
            self.pos_x, self.pos_y = self.rect.center

        keys = pygame.key.get_pressed()
        # 둔화 상태에서는 속도 감소, 이동속도 아이템 버프 중에는 증가
        current_speed = self.speed * self.slow_multiplier
        if self.speed_buff_time > 0:
            current_speed *= ITEM_BUFF_MULTIPLIER

        if keys[pygame.K_w]:
            self.pos_y -= current_speed
            self.last_direction_y = -1
        if keys[pygame.K_s]:
            self.pos_y += current_speed
            self.last_direction_y = 1
        if keys[pygame.K_a]:
            self.pos_x -= current_speed
            self.last_direction_x = -1
        if keys[pygame.K_d]:
            self.pos_x += current_speed
            self.last_direction_x = 1

        self.rect.center = (round(self.pos_x), round(self.pos_y))
        self._synced_center = self.rect.center

        # 걷기 모션용
        self.is_moving = bool(keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d])
        # 이동 방향 (창 돌진 판정용, 멈춰 있으면 None)
        move_x = int(bool(keys[pygame.K_d])) - int(bool(keys[pygame.K_a]))
        move_y = int(bool(keys[pygame.K_s])) - int(bool(keys[pygame.K_w]))
        length = math.hypot(move_x, move_y)
        self.move_dir = (move_x / length, move_y / length) if length else None
        if self.is_moving:
            self.walk_phase += 0.3
        if self.hurt_flash > 0:
            self.hurt_flash -= 1

        # 경계 제약 제거 - 무한 맵

    def draw_health(self, surface):
        draw_player_status(surface, self)


# 좀비 클래스
class Zombie(pygame.sprite.Sprite):
    ZOMBIE_CONFIGS = {
        # 일반 계열 (6가지)
        "normal": {"w": 25, "h": 35, "color": (200, 0, 0), "speed": 2, "health": 30, "dmg": 0.5, "size": 30},
        "spike": {"w": 27, "h": 37, "color": (200, 50, 50), "speed": 2.1, "health": 40, "dmg": 0.8, "size": 32},
        "armored": {"w": 28, "h": 36, "color": (100, 100, 150), "speed": 1.8, "health": 55, "dmg": 0.4, "size": 34},
        "heavy": {"w": 32, "h": 38, "color": (150, 100, 50), "speed": 1.5, "health": 50, "dmg": 0.7, "size": 36},
        "poison": {"w": 26, "h": 36, "color": (0, 200, 50), "speed": 2.2, "health": 35, "dmg": 0.9, "size": 31},
        "ice": {"w": 26, "h": 36, "color": (100, 200, 255), "speed": 1.6, "health": 38, "dmg": 0.5, "size": 31},

        # 탱크 계열 (6가지)
        "tank": {"w": 40, "h": 50, "color": (100, 50, 0), "speed": 1.5, "health": 80, "dmg": 0.3, "size": 45},
        "knight": {"w": 42, "h": 52, "color": (150, 150, 200), "speed": 1.4, "health": 120, "dmg": 0.5, "size": 48},
        "shield": {"w": 44, "h": 54, "color": (180, 100, 50), "speed": 1.3, "health": 120, "dmg": 0.2, "size": 50},
        "stone": {"w": 46, "h": 56, "color": (120, 120, 130), "speed": 1.2, "health": 140, "dmg": 0.15, "size": 52},
        "iron": {"w": 42, "h": 52, "color": (80, 80, 100), "speed": 1.1, "health": 110, "dmg": 0.28, "size": 47},
        "wall": {"w": 50, "h": 60, "color": (100, 60, 20), "speed": 0.8, "health": 160, "dmg": 0.1, "size": 55},

        # 빠른 계열 (6가지)
        "fast": {"w": 15, "h": 25, "color": (255, 100, 0), "speed": 4, "health": 15, "dmg": 0.4, "size": 20},
        "runner": {"w": 17, "h": 27, "color": (255, 120, 0), "speed": 4.5, "health": 12, "dmg": 0.35, "size": 22},
        "ninja": {"w": 14, "h": 24, "color": (50, 50, 100), "speed": 7.5, "health": 10, "dmg": 0.6, "size": 19},
        "spark": {"w": 16, "h": 26, "color": (255, 200, 0), "speed": 4.2, "health": 14, "dmg": 0.5, "size": 21},
        "wind": {"w": 13, "h": 23, "color": (150, 200, 200), "speed": 5.2, "health": 8, "dmg": 0.3, "size": 18},
        "shadow": {"w": 14, "h": 24, "color": (80, 40, 100), "speed": 9.6, "health": 9, "dmg": 0.55, "size": 19},

        # 새 좀비 3종
        "slime": {"w": 30, "h": 30, "color": (90, 220, 90), "speed": 1.6, "health": 40, "dmg": 0.5, "size": 32},       # 분열좀비
        "sniper_z": {"w": 24, "h": 36, "color": (70, 100, 70), "speed": 1.8, "health": 30, "dmg": 0.4, "size": 28},    # 저격좀비
        "howler": {"w": 28, "h": 38, "color": (230, 140, 40), "speed": 1.5, "health": 45, "dmg": 0.5, "size": 34},     # 함성좀비 (주변 이동속도 +30%)

        # 폭탄 계열 (6가지)
        "bomber": {"w": 30, "h": 40, "color": (139, 0, 139), "speed": 1.8, "health": 40, "dmg": 0.6, "size": 35, "exp": 1},
        "mine": {"w": 32, "h": 42, "color": (100, 0, 100), "speed": 1.2, "health": 50, "dmg": 0.8, "size": 37, "exp": 1},
        "flame": {"w": 31, "h": 41, "color": (255, 100, 0), "speed": 1.9, "health": 45, "dmg": 0.7, "size": 36, "exp": 1},
        "acid": {"w": 29, "h": 39, "color": (150, 200, 0), "speed": 1.7, "health": 42, "dmg": 0.65, "size": 34, "exp": 1},
        "toxic": {"w": 30, "h": 40, "color": (100, 200, 50), "speed": 1.6, "health": 48, "dmg": 0.75, "size": 35, "exp": 1},
        "nuclear": {"w": 34, "h": 44, "color": (200, 100, 0), "speed": 1.5, "health": 60, "dmg": 1.0, "size": 39, "exp": 1},

        # 보스 계열 (6가지)
        "boss": {"w": 60, "h": 80, "color": (255, 215, 0), "speed": 1.2, "health": 200, "dmg": 1.5, "size": 70, "range": 150},
        "gangster": {"w": 30, "h": 40, "color": (100, 100, 100), "speed": 2.5, "health": 25, "dmg": 0.7, "size": 35, "range": 300},  # 갱스터: 보스가 소환하는 원거리 공격 좀비
        "paladin": {"w": 64, "h": 84, "color": (200, 200, 150), "speed": 1.2, "health": 300, "dmg": 2.0, "size": 74, "range": 160},  # 기사단장: 기사 좀비 소환
        "imp": {"w": 20, "h": 28, "color": (200, 50, 100), "speed": 2.8, "health": 15, "dmg": 0.4, "size": 22},  # 임프: 악마가 소환하는 작은 좀비
        "demon": {"w": 62, "h": 82, "color": (200, 0, 100), "speed": 1.3, "health": 240, "dmg": 1.8, "size": 72, "range": 160},
        "angel": {"w": 62, "h": 82, "color": (255, 255, 200), "speed": 1.4, "health": 220, "dmg": 1.6, "size": 72, "range": 155},
        "apostle": {"w": 62, "h": 82, "color": (255, 255, 200), "speed": 1.4, "health": 220, "dmg": 1.6, "size": 72, "range": 155},  # 12사도: 신이 소환하는 천사 능력치 좀비
        "dragon": {"w": 70, "h": 90, "color": (150, 0, 150), "speed": 1.1, "health": 280, "dmg": 2.0, "size": 80, "range": 170},
        "king": {"w": 65, "h": 85, "color": (255, 200, 100), "speed": 1.15, "health": 260, "dmg": 1.9, "size": 75, "range": 165},
        "god": {"w": 75, "h": 95, "color": (255, 255, 255), "speed": 1.0, "health": 350, "dmg": 2.5, "size": 85, "range": 180},

        # 거대 계열 (6가지)
        "colossus": {"w": 100, "h": 130, "color": (40, 40, 40), "speed": 0.3, "health": 500, "dmg": 2, "size": 115, "range": 200},
        "titan": {"w": 110, "h": 140, "color": (100, 50, 0), "speed": 0.25, "health": 600, "dmg": 2.3, "size": 125, "range": 210},
        "giant": {"w": 95, "h": 125, "color": (150, 100, 50), "speed": 0.35, "health": 450, "dmg": 1.8, "size": 105, "range": 190},
        "behemoth": {"w": 120, "h": 150, "color": (80, 80, 80), "speed": 0.2, "health": 700, "dmg": 2.5, "size": 135, "range": 220},
        "leviathan": {"w": 105, "h": 135, "color": (0, 100, 150), "speed": 0.28, "health": 650, "dmg": 2.4, "size": 120, "range": 215},
        "elder": {"w": 115, "h": 145, "color": (100, 150, 100), "speed": 0.22, "health": 800, "dmg": 2.8, "size": 130, "range": 225},
    }

    def __init__(self, x, y, zombie_type="normal", wave=1, parent_zombie=None):
        super().__init__()
        self.zombie_type = zombie_type
        self.wave = wave
        self.knockback_vel_x = 0
        self.knockback_vel_y = 0
        self.knockback_decay = 0.95
        self.knockback_resistance = 1.0  # 기본값: 100% 넉백 받음 (0.0 = 완전 저항)
        self.attack_cooldown = 0
        self.slow_time = 0
        self.slow_multiplier = 1.0
        self.burn_time = 0
        self.burn_damage_cooldown = 0

        # 소환자 좀비 추적 (왕좀비가 소환한 좀비 등)
        self.parent_zombie = parent_zombie

        # 좀비 타입별 설정
        config = self.ZOMBIE_CONFIGS.get(zombie_type, self.ZOMBIE_CONFIGS["normal"])

        self.image = pygame.Surface((config["w"], config["h"]))
        self.image.fill(config["color"])
        self.speed = config["speed"] + wave * 0.1
        self.health = config["health"] + wave * (config["health"] // 3)
        # 보스/거대 좀비는 체력 1.6배 (다른 좀비가 소환한 개체는 제외)
        if zombie_type in GUARANTEED_DROP_TYPES and parent_zombie is None:
            self.health *= 1.6
        self.max_health = self.health  # 최대 체력 저장
        self.damage = config["dmg"] + wave * (config["dmg"] / 5)
        self.size = config["size"]

        # ===== 고유 능력 설정 =====
        # normal: 특수 능력 없음

        # spike: 가시 - 원거리 가시 투사체 공격
        if zombie_type == "spike":
            self.spike_damage = 1.0
            self.spike_attack_cooldown = 0
            self.spike_attack_interval = 120  # 120프레임 = 2초 (60fps 기준)

        # armored: 갑옷 - 받는 데미지 감소 + 죽으면 일반좀비로 부활
        if zombie_type == "armored":
            self.armor_reduction = 0.6  # 60%의 데미지만 받음
            self.max_health_original = self.health

        # heavy: 무거운 - 넉백 완전 저항 + 체력 비례 돌진 능력
        if zombie_type == "heavy":
            self.knockback_resistance = 0.0  # 넉백 완전 면역
            self.charge_cooldown = 0
            self.charge_interval = 180  # 180프레임 = 3초 (60fps 기준)
            self.is_charging = False
            self.charge_timer = 0
            self.charge_range = 500  # 이 거리 안에서만 돌진 준비
            self.charge_speed_mult = 4  # 이동속도의 4배로 돌진
            self.charge_duration = 12  # 12프레임 동안 돌진
            self.charge_health_scaled = True  # 체력 비례 돌진력 (체력이 줄면 약해짐)

        # 베히모스: 돌진 공격 (게임 설명에는 있었지만 구현이 없었음)
        if zombie_type == "behemoth":
            self.charge_cooldown = 0
            self.charge_interval = 300  # 5초마다
            self.is_charging = False
            self.charge_timer = 0
            self.charge_range = 600
            self.charge_speed_mult = 8  # 느린 대신 돌진은 이동속도의 8배
            self.charge_duration = 30  # 0.5초 동안 돌진
            self.charge_health_scaled = False

        # poison: 독 - 따라온 자리에 독 장판 생성
        if zombie_type == "poison":
            self.poison_active = False
            self.poison_cooldown = 0
            self.poison_pool_interval = 30  # 30프레임 = 0.5초마다 장판 생성 (60fps 기준)
            self.last_poison_x = x
            self.last_poison_y = y

        # ice: 얼음 - 플레이어 속도 저하 + 죽으면 속도 저하 투사체 투척
        if zombie_type == "ice":
            self.slow_effect = 0.1  # 플레이어 속도 90% 감소

        # 탱크 계열: 넉백 완전 면역
        if zombie_type in ["tank", "knight", "shield", "stone", "iron", "wall"]:
            self.knockback_resistance = 0.0  # 넉백 완전 면역

        # 기사: 죽으면 방패좀비로 부활
        if zombie_type == "knight":
            self._knight_resurrected = False

        # 방패: 받는 데미지 95% 감소 (5%만 받음) + 죽으면 갑옷좀비로 부활
        if zombie_type == "shield":
            self.shield_reduction = 0.95  # 95% 데미지 감소
            self._shield_resurrected = False

        # 닌자: 원거리 공격 능력
        if zombie_type == "ninja":
            self.ninja_attack_interval = 100  # 1.67초마다 공격
            # 사거리에 들어오고 0.25초 뒤 첫 표창을 던짐
            # (0부터 시작하면 너무 빨라서 첫 공격 전에 근접해 버려 원거리 공격이 사실상 안 나왔음)
            self.ninja_attack_cooldown = self.ninja_attack_interval - 15
            self.ninja_attack_range = 350

        # 바람: 죽을 때 광역 효과 (약한 데미지 + 밀치기), 속도 증가
        if zombie_type == "wind":
            self.wind_blast_radius = 200
            self.wind_blast_damage = 0.5
            self.wind_blast_knockback = 15
            self.speed = config["speed"] * 1.3 + wave * 0.1  # 기본 속도 130% 증가

        # 불꽃: 죽을 때 광역 대미지
        if zombie_type == "flame":
            self.flame_explosion_radius = 180
            self.flame_explosion_damage = 2.0

        # 보스/거대 좀비: 넉백 완전 면역
        # (기사단장이 보스인데 목록에서 빠져 있어서 넉백을 받던 문제 수정)
        if zombie_type in ["boss", "paladin", "demon", "angel", "apostle", "dragon", "king", "god", "colossus", "titan", "giant", "behemoth", "leviathan", "elder"]:
            self.knockback_resistance = 0.0  # 넉백 완전 면역

        # 악마 (demon): 임프 지속 소환
        if zombie_type == "demon":
            self.imp_spawn_cooldown = 0
            self.imp_spawn_interval = 200  # 3.3초마다 소환 (60fps 기준)
            self.imp_spawn_radius = 200

        # 보스 (boss): 갱스터 지속 소환
        if zombie_type == "boss":
            self.gangster_spawn_cooldown = 0
            self.gangster_spawn_interval = 200  # 3.3초마다 소환 (60fps 기준)
            self.gangster_spawn_radius = 180
            self.gangster_spawn_count = 2  # 한 번에 2마리 소환

        # 기사단장 (paladin): 기사 지속 소환
        if zombie_type == "paladin":
            self.knight_spawn_cooldown = 0
            self.knight_spawn_interval = 280  # 4.7초마다 소환
            self.knight_spawn_radius = 220
            self._paladin_resurrected = False  # 부활 플래그

        # 철: 죽으면 돌좀비로 부활
        if zombie_type == "iron":
            self._iron_resurrected = False

        # 타이탄: 30% 확률로 거인 2마리로 부활
        if zombie_type == "titan":
            self._titan_resurrected = False

        # 천사 (angel): 약해진 신성한 폭발 능력
        if zombie_type == "angel":
            self.divine_explosion_radius = 180
            self.divine_explosion_damage = 3.0

        # 신 (god): 12초마다 12사도 12명 동시 소환
        if zombie_type == "god":
            self.apostle_spawn_cooldown = 0
            self.apostle_spawn_interval = 720  # 12초마다 소환 (720프레임 = 12초 @60fps)
            self.divine_explosion_radius = 250
            self.divine_explosion_damage = 5.0

        # 왕 (king): 일반 좀비 대량 소환
        if zombie_type == "king":
            self.minion_spawn_cooldown = 0
            self.minion_spawn_interval = 150  # 2.5초마다 소환 (60fps 기준)
            self.minion_spawn_radius = 200
            self.minion_spawn_count = 3  # 한 번에 3마리 소환

        # 용 (dragon): 돌진 공격 + 원거리 공격
        if zombie_type == "dragon":
            # 돌진 공격 설정
            self.dragon_charge_cooldown = 0
            self.dragon_charge_interval = 300  # 5초마다 돌진 (60fps 기준)
            self.dragon_charge_speed = 24.0  # 돌진 속도 (기존 8.0 × 3배)
            self.dragon_charging = False  # 돌진 중 여부
            self.dragon_charge_duration = 0  # 돌진 지속 시간
            self.dragon_charge_max_duration = 60  # 1초간 돌진

            # 원거리 공격 설정
            self.dragon_ranged_cooldown = 0
            self.dragon_ranged_interval = 180  # 3초마다 원거리 공격 (60fps 기준)
            self.dragon_ranged_projectiles = 3  # 한 번에 3개의 투사체

        # 리바이어던: 가로/세로 쓰나미 공격 (초기화가 없어서 쓰나미가 한 번도 발동하지 않던 문제 수정)
        if zombie_type == "leviathan":
            self.tsunami_cooldown = 0
            self.tsunami_interval = 300  # 5초마다 쓰나미 (60fps 기준)
            self.tsunami_range = 400

        # ===== 추가 고유 능력 상태값 =====
        self.angel_role = None      # 12천사 역할
        self.guard_mult = 1.0       # 수호 오라(벽좀비/수호의 천사) 안에 있으면 받는 피해 감소
        self.hasted = False         # 질풍의 천사 오라 안에 있으면 이동속도 +30%
        self.block_hits = 0         # 결계: 남은 공격 무효 횟수
        self.no_reward = False      # 자폭한 임프는 점수/경험치 없음
        self.ability_cooldown = 0   # 추가 능력 쿨타임 (프레임)
        if zombie_type == "fast":
            self.zigzag_phase = random.uniform(0, math.pi * 2)
        if zombie_type == "runner":
            self.chase_bonus = 0.0
            self._runner_hp = self.health
        self.slime_gen = 0      # 분열좀비 세대 (0 → 1 → 2까지 분열)
        self.aiming = 0         # 저격좀비 조준 남은 프레임
        self.aim_x = self.aim_y = 0
        self.burrowed = 0       # (예전 땅굴좀비용, 항상 0 - 멀티 파일 호환용으로 남김)

        # 폭탄 좀비 타입 설정
        if zombie_type in ["bomber", "mine", "flame", "acid", "toxic", "nuclear"]:
            self.explosion_radius = 150
            self.explosion_damage = 30 + wave * 5

        # 보스/거대 좀비 설정
        if "range" in config:
            self.attack_range = config["range"]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # rect는 정수 좌표라 느린 이동/대각선 이동이 반올림으로 왜곡되므로 실수 좌표를 따로 보관
        self.pos_x = float(x)
        self.pos_y = float(y)
        self._synced_center = self.rect.center
        # 연출용 상태 (게임 판정과 무관)
        self.anim_phase = fx_random.uniform(0, math.pi * 2)
        self.hit_flash = 0
        self.last_health = self.health
        self.damage_accum = 0.0
        self.damage_text_cooldown = 0
        self.crit_marked = False
        self.electric_fx = 0  # 전기탄 감전 연출 남은 프레임

    def _move(self, move_x, move_y):
        """실수 좌표로 이동한 뒤 rect에 반영"""
        self.pos_x += move_x
        self.pos_y += move_y
        self.rect.center = (round(self.pos_x), round(self.pos_y))
        self._synced_center = self.rect.center

    def kill(self):
        """죽음 처리 - 부활 체인: 기사->방패->갑옷->일반, 철->돌, 타이탄->거인(30%), 핵->폭탄"""
        # 기사단장 부활 체크
        if self.zombie_type == "paladin" and not self._paladin_resurrected:
            self._paladin_resurrected = True
            self.zombie_type = "armored"
            self.armor_reduction = 0.6
            self.image.fill((100, 100, 150))  # 갑옷 좀비 회색
            self.health = self.max_health * 0.6
            return  # 부활했으므로 kill하지 않음

        # 기사 부활 체크 (방패로 부활)
        if self.zombie_type == "knight" and not self._knight_resurrected:
            self._knight_resurrected = True
            self.zombie_type = "shield"
            self.shield_reduction = 0.95
            self._shield_resurrected = False  # 방패 좀비의 부활 플래그 초기화
            self.image.fill((180, 100, 50))  # 방패 좀비 갈색
            self.health = self.max_health * 0.7
            return  # 부활했으므로 kill하지 않음

        # 방패 부활 체크 (갑옷으로 부활)
        if self.zombie_type == "shield" and not self._shield_resurrected:
            self._shield_resurrected = True
            self.zombie_type = "armored"
            self.armor_reduction = 0.6
            if hasattr(self, 'shield_reduction'):
                delattr(self, 'shield_reduction')
            self.image.fill((100, 100, 150))  # 갑옷 좀비 회색
            self.health = self.max_health * 0.6
            return  # 부활했으므로 kill하지 않음

        # 갑옷 좀비 부활 체크 (일반으로 부활)
        if self.zombie_type == "armored" and not hasattr(self, '_resurrected'):
            self._resurrected = True
            self.zombie_type = "normal"
            if hasattr(self, 'armor_reduction'):
                delattr(self, 'armor_reduction')
            self.image.fill((200, 0, 0))  # 일반 좀비 빨강
            self.health = self.max_health * 0.5
            return  # 부활했으므로 kill하지 않음

        # 철 부활 체크 (돌로 부활)
        if self.zombie_type == "iron" and not self._iron_resurrected:
            self._iron_resurrected = True
            self.zombie_type = "stone"
            self.image.fill((120, 120, 130))  # 돌 좀비 회색
            self.health = self.max_health * 0.65
            return  # 부활했으므로 kill하지 않음

        # 일반좀비: 15% 확률로 한 번 다시 일어남 (체력 30%)
        if self.zombie_type == "normal" and not getattr(self, "_normal_revived", False) and random.random() < 0.15:
            self._normal_revived = True
            self.health = self.max_health * 0.3
            return

        # 부활의 천사: 처음 한 번은 체력 50%로 부활
        if self.angel_role == "rebirth" and not getattr(self, "_rebirth_used", False):
            self._rebirth_used = True
            self.health = self.max_health * 0.5
            return

        # 타이탄 부활 체크 (30% 확률로 거인 2마리 부활)
        # 타이탄 자신은 죽고, 사망 처리에서 이 플래그를 보고 거인 2마리를 소환함
        if self.zombie_type == "titan" and not self._titan_resurrected:
            self._titan_resurrected = True
            if random.random() < 0.3:  # 30% 확률
                self.titan_respawn_as_giants = True

        # 일반 kill 실행
        super().kill()

    def update(self, player, bullets=None, all_sprites=None, explosions=None):
        # rect가 외부에서 바뀌었으면 실수 좌표를 다시 맞춤
        if self.rect.center != self._synced_center:
            self.pos_x, self.pos_y = self.rect.center

        # 넉백 적용 (모든 좀비에 저항값 적용)
        self._move(self.knockback_vel_x * self.knockback_resistance,
                   self.knockback_vel_y * self.knockback_resistance)
        self.knockback_vel_x *= self.knockback_decay
        self.knockback_vel_y *= self.knockback_decay

        # 넉백이 거의 없을 때 정상화
        if abs(self.knockback_vel_x) < 0.5:
            self.knockback_vel_x = 0
        if abs(self.knockback_vel_y) < 0.5:
            self.knockback_vel_y = 0

        if self.slow_time > 0:
            self.slow_time -= 1
        else:
            self.slow_multiplier = 1.0

        if self.burn_time > 0:
            self.burn_time -= 1
            self.burn_damage_cooldown -= 1
            if self.burn_damage_cooldown <= 0:
                self.health -= 0.4
                self.burn_damage_cooldown = 20

        # 돌좀비: 화상·둔화 면역
        if self.zombie_type == "stone":
            self.burn_time = 0
            self.slow_time = 0
            self.slow_multiplier = 1.0

        # 플레이어 방향으로 이동
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        current_speed = self.speed * self.slow_multiplier
        if self.hasted:
            current_speed *= 1.3  # 질풍의 천사 오라
        # 주자좀비: 오래 쫓을수록 빨라짐 (최대 +60%), 맞으면 초기화
        if self.zombie_type == "runner":
            if self.health < self._runner_hp:
                self.chase_bonus = 0.0
            else:
                self.chase_bonus = min(0.6, self.chase_bonus + 0.004)
            self._runner_hp = self.health
            current_speed *= 1 + self.chase_bonus
        if self.aiming > 0:
            current_speed = 0          # 저격좀비: 조준하는 동안 멈춤

        if distance > 0:
            move_x = (dx / distance) * current_speed
            move_y = (dy / distance) * current_speed
            # 빠른좀비: 지그재그로 움직여 맞히기 어려움
            if self.zombie_type == "fast":
                self.zigzag_phase += 0.15
                wiggle = math.sin(self.zigzag_phase) * current_speed * 0.9
                move_x += (-dy / distance) * wiggle
                move_y += (dx / distance) * wiggle
            self._move(move_x, move_y)

        # 공격 쿨타임 감소
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # ===== 특수 능력 업데이트 =====
        if self.zombie_type == "spike" and distance < 400:
            self.spike_attack_cooldown += 1
            if self.spike_attack_cooldown >= self.spike_attack_interval:
                # 가시 투사체 발사
                if bullets is not None and all_sprites is not None:
                    spike_proj = SpikeProjectile(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery
                    )
                    bullets.add(spike_proj)
                    all_sprites.add(spike_proj)
                self.spike_attack_cooldown = 0

        elif self.zombie_type == "poison":
            # 독 장판 생성
            dist_moved = math.sqrt((self.rect.centerx - self.last_poison_x)**2 +
                                  (self.rect.centery - self.last_poison_y)**2)
            if dist_moved > 50:  # 일정 거리 이동했을 때만 생성
                if explosions is not None and all_sprites is not None:
                    poison_pool = PoisonPool(self.rect.centerx, self.rect.centery)
                    explosions.add(poison_pool)
                    all_sprites.add(poison_pool)
                self.last_poison_x = self.rect.centerx
                self.last_poison_y = self.rect.centery

        # 무거운좀비 / 베히모스: 돌진
        # (돌진 도중 플레이어가 사거리 밖으로 나가도 돌진이 멈춘 채로 굳지 않도록 is_charging이면 계속 처리)
        elif self.zombie_type in ("heavy", "behemoth") and (distance < self.charge_range or self.is_charging):
            if distance < self.charge_range:
                self.charge_cooldown += 1
            if self.charge_cooldown >= self.charge_interval and not self.is_charging:
                # 돌진 시작
                self.is_charging = True
                self.charge_cooldown = 0

            if self.is_charging:
                # 플레이어 방향으로 빠르게 이동
                if distance > 0:
                    health_ratio = max(0.5, self.health / self.max_health) if self.charge_health_scaled else 1.0
                    charge_speed = self.speed * self.slow_multiplier * self.charge_speed_mult * health_ratio
                    self._move((dx / distance) * charge_speed, (dy / distance) * charge_speed)

                    # 차지 이펙트 생성
                    if all_sprites is not None:
                        charge_effect = ChargeEffect(
                            self.rect.centerx, self.rect.centery,
                            dx / distance, dy / distance,
                            radius=max(40, self.size // 2)
                        )
                        all_sprites.add(charge_effect)

                # 돌진 지속 시간
                self.charge_timer += 1
                if self.charge_timer > self.charge_duration:
                    self.is_charging = False
                    self.charge_timer = 0

        elif self.zombie_type == "ninja" and distance < self.ninja_attack_range:  # 설정해 둔 사거리(350) 사용
            # 닌자: 원거리 공격
            self.ninja_attack_cooldown += 1
            if self.ninja_attack_cooldown >= self.ninja_attack_interval:
                if bullets is not None and all_sprites is not None:
                    ninja_proj = NinjaProjectile(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery
                    )
                    bullets.add(ninja_proj)
                    all_sprites.add(ninja_proj)
                self.ninja_attack_cooldown = 0

        elif self.zombie_type == "gangster" and distance < 500:
            # 갱스터: 원거리 공격 (총알 발사)
            if not hasattr(self, 'gangster_attack_cooldown'):
                self.gangster_attack_cooldown = 0
                self.gangster_attack_interval = 80  # 1.33초마다 공격

            self.gangster_attack_cooldown += 1
            if self.gangster_attack_cooldown >= self.gangster_attack_interval:
                if bullets is not None and all_sprites is not None:
                    # 플레이어 방향으로 총알 발사
                    bullet = Bullet(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery,
                        damage=8.0,
                        bullet_type="normal",
                        weapon_type="gangster_bullet"
                    )
                    bullet.speed = 10
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                self.gangster_attack_cooldown = 0

        elif self.zombie_type == "dragon":
            # 용: 돌진 공격 + 원거리 공격
            if self.dragon_charging:
                # 돌진 중인 상태
                if distance > 0:
                    dragon_speed = self.dragon_charge_speed * self.slow_multiplier
                    self._move((dx / distance) * dragon_speed, (dy / distance) * dragon_speed)

                self.dragon_charge_duration += 1
                if self.dragon_charge_duration >= self.dragon_charge_max_duration:
                    self.dragon_charging = False
                    self.dragon_charge_duration = 0
            else:
                # 일반 이동 중
                # 돌진 공격 쿨다운 감소
                self.dragon_charge_cooldown += 1
                if self.dragon_charge_cooldown >= self.dragon_charge_interval and distance < 600:
                    self.dragon_charging = True
                    self.dragon_charge_cooldown = 0

                # 원거리 공격
                self.dragon_ranged_cooldown += 1
                if self.dragon_ranged_cooldown >= self.dragon_ranged_interval and distance < 700:
                    if bullets is not None and all_sprites is not None:
                        # 3개의 투사체 발사 (부채꼴 형태)
                        base_angle = math.atan2(dy, dx)
                        for i in range(self.dragon_ranged_projectiles):
                            angle_offset = (i - 1) * 0.4  # -0.4, 0, 0.4
                            angle = base_angle + angle_offset
                            target_x = self.rect.centerx + math.cos(angle) * 500
                            target_y = self.rect.centery + math.sin(angle) * 500

                            # 드래곤 파이어볼 발사
                            dragon_proj = Bullet(
                                self.rect.centerx, self.rect.centery,
                                target_x, target_y,
                                damage=20.0,
                                bullet_type="normal",
                                weapon_type="dragon_fireball"
                            )
                            dragon_proj.speed = 8
                            bullets.add(dragon_proj)
                            all_sprites.add(dragon_proj)

                    self.dragon_ranged_cooldown = 0

        # 리바이어던: 가로/세로 쓰나미 공격 (대각선 불가)
        elif self.zombie_type == "leviathan":
            if hasattr(self, 'tsunami_cooldown'):
                self.tsunami_cooldown += 1
                if self.tsunami_cooldown >= self.tsunami_interval and distance < 500:
                    if explosions is not None and all_sprites is not None:
                        # 가로 쓰나미 (수평선)
                        horizontal_tsunami = TsunamiEffect(
                            self.rect.centerx, self.rect.centery,
                            direction="horizontal", range_dist=self.tsunami_range
                        )
                        explosions.add(horizontal_tsunami)
                        all_sprites.add(horizontal_tsunami)

                        # 세로 쓰나미 (수직선)
                        vertical_tsunami = TsunamiEffect(
                            self.rect.centerx, self.rect.centery,
                            direction="vertical", range_dist=self.tsunami_range
                        )
                        explosions.add(vertical_tsunami)
                        all_sprites.add(vertical_tsunami)

                    self.tsunami_cooldown = 0

        # ===== 추가 고유 능력 =====
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1
        if self.zombie_type == "tank":
            # 탱크: 4초마다 발 구르기 충격파 (주변 140px)
            if self.ability_cooldown <= 0 and distance < 140:
                self.ability_cooldown = 240
                apply_player_damage(player, 6)
                if all_sprites is not None:
                    all_sprites.add(MeleePoundEffect(self.rect.centerx, self.rect.centery, 140))
                fx.add_shake(3)
        elif self.zombie_type == "colossus":
            # 콜로서스: 3초마다 지진 (주변 220px)
            if self.ability_cooldown <= 0 and distance < 260:
                self.ability_cooldown = 180
                if distance < 220:
                    apply_player_damage(player, 10)
                if all_sprites is not None:
                    all_sprites.add(MeleePoundEffect(self.rect.centerx, self.rect.centery, 220))
                fx.add_shake(6)
        elif self.zombie_type == "giant":
            # 거인: 4초마다 큰 돌 던지기
            if self.ability_cooldown <= 0 and distance < 600 and bullets is not None and all_sprites is not None:
                self.ability_cooldown = 240
                rock = Bullet(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery,
                              damage=12.0, bullet_type="normal", weapon_type="giant_rock")
                bullets.add(rock)
                all_sprites.add(rock)
        elif self.zombie_type == "sniper_z":
            # 저격좀비: 멀리서 멈춰 1.2초 조준(빨간 조준선) 후 강한 한 발
            if self.aiming > 0:
                self.aiming -= 1
                if self.aiming > 15:   # 발사 직전 0.25초는 조준점 고정 (피할 수 있게)
                    self.aim_x, self.aim_y = player.rect.center
                if self.aiming == 0 and bullets is not None and all_sprites is not None:
                    shot = Bullet(self.rect.centerx, self.rect.centery, self.aim_x, self.aim_y,
                                  damage=15.0, bullet_type="normal", weapon_type="zombie_snipe")
                    bullets.add(shot)
                    all_sprites.add(shot)
                    self.ability_cooldown = 200
            elif self.ability_cooldown <= 0 and distance < 480:
                self.aiming = 72
                self.aim_x, self.aim_y = player.rect.center
        elif self.angel_role is not None and self.ability_cooldown <= 0:
            self._use_angel_ability(player, distance, dx, dy, bullets, all_sprites)

    def _use_angel_ability(self, player, distance, dx, dy, bullets, all_sprites):
        """12천사 고유 능력 (치유/수호/질풍 오라는 main의 오라 처리, 부활은 kill(), 분열은 사망 처리, 결계는 피격 처리에서)"""
        role = self.angel_role
        cx, cy = self.rect.center
        if role == "flame" and distance < 600 and bullets is not None:
            self.ability_cooldown = 150
            fireball = Bullet(cx, cy, player.rect.centerx, player.rect.centery,
                              damage=10.0, bullet_type="normal", weapon_type="dragon_fireball")
            bullets.add(fireball)
            all_sprites.add(fireball)
        elif role == "frost" and distance < 500 and bullets is not None:
            self.ability_cooldown = 180
            ice = IceProjectile(cx, cy, player.rect.centerx, player.rect.centery)
            ice.slow_effect = 0.5  # 이동속도 50% 감소 (얼음좀비보다 약하게)
            bullets.add(ice)
            all_sprites.add(ice)
        elif role == "thunder" and distance < 450:
            self.ability_cooldown = 200
            apply_player_damage(player, 8)
            player.shock_time = max(player.shock_time, 20)
            for i in range(11):  # 번개 줄기
                t = i / 10
                fx.trail(cx + dx * t + fx_random.uniform(-10, 10), cy + dy * t + fx_random.uniform(-10, 10),
                         (255, 245, 120), 4, 12)
        elif role == "judgment" and distance < 200:
            self.ability_cooldown = 240
            if all_sprites is not None:
                all_sprites.add(HolyExplosionEffect(cx, cy, 160, 8.0))
            if distance < 160:
                apply_player_damage(player, 8)
        elif role == "drain" and distance < 300:
            self.ability_cooldown = 120
            apply_player_damage(player, 4)
            self.health = min(self.max_health, self.health + 12)
            for i in range(9):  # 플레이어 → 천사로 빨려가는 붉은 기운
                t = i / 8
                fx.trail(player.rect.centerx - dx * t, player.rect.centery - dy * t, (220, 40, 70), 3, 14)
        elif role == "blink" and distance > 120:
            self.ability_cooldown = 240
            fx.burst(cx, cy, (160, 120, 255), 12, speed=(1, 4), size=(2, 4), life=(10, 20))
            angle = random.uniform(0, math.pi * 2)
            radius = random.uniform(150, 230)
            self.pos_x = player.rect.centerx + math.cos(angle) * radius
            self.pos_y = player.rect.centery + math.sin(angle) * radius
            self.rect.center = (round(self.pos_x), round(self.pos_y))
            self._synced_center = self.rect.center
            fx.burst(self.rect.centerx, self.rect.centery, (160, 120, 255), 12, speed=(1, 4), size=(2, 4), life=(10, 20))


def make_role_angel(x, y, role_index, wave, parent):
    """신좀비가 소환하는 12천사 (각자 다른 능력, 사도/보스 천사보다 작고 체력 40%)"""
    role, name, color = ANGEL_ROLES[role_index]
    angel = Zombie(x, y, zombie_type="angel", wave=wave, parent_zombie=parent)
    angel.angel_role = role
    angel.base_name = name
    angel.custom_name = name
    center = angel.rect.center
    angel.image = pygame.Surface((40, 52))
    angel.image.fill(color)
    angel.rect = angel.image.get_rect(center=center)
    angel._synced_center = angel.rect.center
    angel.size = 46
    angel.health *= 0.4
    angel.max_health = angel.health
    angel.last_health = angel.health
    if role == "gale":
        angel.speed *= 2
    if role == "barrier":
        angel.block_hits = 4
        angel.custom_name = f"{name} [4]"
    angel.ability_cooldown = random.randint(30, 120)  # 12명이 동시에 능력을 쓰지 않도록 엇갈림
    return angel


# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage=25, bullet_type="normal", weapon_type=None):
        super().__init__()
        self.bullet_type = bullet_type
        self.weapon_type = weapon_type
        self.damage = damage
        # 좀비(갱스터/용)가 쏜 총알인지 여부: 좀비끼리는 맞지 않고 플레이어에게만 피해
        self.is_enemy = weapon_type in ENEMY_BULLET_TYPES
        # 기본 관통 수 (이 수만큼 좀비를 더 뚫고 지나감). 실제 관통 수 = 기본 관통 + 플레이어 관통 레벨
        self.pierce = 0
        self.dodged = set()  # 이 총알을 회피한 좀비 (그림자좀비)
        # 착탄 폭발 (플라즈마): 반경과 주변 좀비 피해 비율
        self.splash_radius = 0
        self.splash_ratio = 0
        # 최대 사거리(px): 이만큼 날아가면 사라짐 (샷건은 짧게)
        self.max_range = 3000
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 10

        # 무기별 총알 디자인
        if weapon_type == "glock":
            # 글록 - 작은 노란 원형 탄약
            self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (3, 3), 3)
            pygame.draw.circle(self.image, (255, 200, 0), (3, 3), 2)
            self.speed = 12
        elif weapon_type == "shotgun":
            # 샷건 - 큰 주황색 원형 탄약
            self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 140, 0), (6, 6), 6)
            pygame.draw.circle(self.image, (255, 200, 0), (6, 6), 4)
            self.speed = 10
        elif weapon_type == "sniper":
            # 저격총 - 길쭉한 은색 탄약
            self.image = pygame.Surface((4, 16), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (200, 200, 200), (1, 0, 2, 16))
            pygame.draw.polygon(self.image, (150, 150, 150), [(0, 14), (4, 14), (2, 16)])
            self.speed = 18
        elif weapon_type == "machinegun":
            # 기관총 - 작은 빨간 직사각형 탄약
            self.image = pygame.Surface((5, 10), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (1, 0, 3, 10))
            pygame.draw.rect(self.image, (200, 0, 0), (1, 7, 3, 3))
            self.speed = 14
        elif weapon_type == "plasma":
            # 플라즈마 - 화려한 청록색 에너지볼
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (100, 255, 255), (8, 8), 8)   # 외부 광원
            pygame.draw.circle(self.image, (0, 220, 255), (8, 8), 6)     # 중간 고리
            pygame.draw.circle(self.image, (0, 255, 220), (8, 8), 4)     # 중심
            pygame.draw.circle(self.image, WHITE, (8, 8), 2)             # 매우 중심
            self.speed = 13
        elif weapon_type == "rocket":
            # 로켓 - 빨간 로켓 모양
            self.image = pygame.Surface((12, 20), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, RED, [(2, 0), (10, 0), (12, 8), (10, 16), (2, 16), (0, 8)])  # 로켓 몸체
            pygame.draw.polygon(self.image, (200, 0, 0), [(3, 16), (9, 16), (8, 20), (4, 20)])  # 로켓 꼬리
            self.speed = 8
        elif weapon_type == "dragon_fireball":
            # 드래곤 파이어볼 - 주황/빨강 원형
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 100, 0), (5, 5), 5)  # 외부
            pygame.draw.circle(self.image, (255, 150, 0), (5, 5), 3)  # 중간
            self.speed = 8
        elif weapon_type == "gangster_bullet":
            # 갱스터 총알 - 회색 작은 원형
            self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (150, 150, 150), (2, 2), 2)  # 회색
            pygame.draw.circle(self.image, (100, 100, 100), (2, 2), 1)  # 어두운 회색
            self.speed = 10
        elif weapon_type == "zombie_snipe":
            # 저격좀비 탄환 - 길쭉한 빨간 탄 (탄두가 위쪽)
            self.image = pygame.Surface((6, 18), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (220, 40, 40), (1, 4, 4, 14))
            pygame.draw.polygon(self.image, (255, 200, 200), [(3, 0), (6, 5), (0, 5)])
            self.speed = 20
        elif weapon_type == "javelin":
            # 창 스킬 투창 - 길쭉한 창 (탄두가 위쪽)
            self.image = pygame.Surface((10, 64), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (150, 120, 40), (4, 12, 3, 52))
            pygame.draw.polygon(self.image, (230, 220, 150), [(5, 0), (10, 14), (0, 14)])
            self.speed = 22
        elif weapon_type == "giant_rock":
            # 거인 좀비가 던지는 큰 돌
            self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (115, 100, 85), (11, 11), 11)
            pygame.draw.circle(self.image, (160, 145, 125), (8, 8), 4)
            self.speed = 6
        elif bullet_type == "normal":
            self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (4, 4), 4)
            self.speed = 10
        elif bullet_type == "shotgun":
            self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (3, 3), 3)
            self.speed = 12
        elif bullet_type == "laser":
            self.image = pygame.Surface((4, 20), pygame.SRCALPHA)
            pygame.draw.line(self.image, CYAN, (2, 0), (2, 20), 4)
            self.speed = 20
        elif bullet_type == "plasma":
            # 플라즈마 - 더 큰 크기와 화려한 색상
            self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (100, 255, 255), (7, 7), 7)  # 외부 광원
            pygame.draw.circle(self.image, (0, 200, 255), (7, 7), 5)    # 중간 고리
            pygame.draw.circle(self.image, (0, 255, 200), (7, 7), 3)    # 중심
            self.speed = 15
        elif bullet_type == "rocket":
            self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (4, 0, 7, 15))
            self.speed = 8
        else:
            # 기본값
            self.image = pygame.Surface((8, 8))
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 0
        self.hit_targets = set()
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.start_x = float(x)
        self.start_y = float(y)

        # 목표 방향 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
        # 방향이 정해진 뒤 속도 벡터 계산
        self.speed = self._speed
        # 길쭉한 탄은 날아가는 방향으로 그림만 회전 (충돌 판정 rect는 그대로)
        self._orient_image()
        trail_key = self.weapon_type if self.weapon_type in FX_TRAILS else self.bullet_type
        self.trail = FX_TRAILS.get(trail_key)

    def _orient_image(self):
        if self.dir_x == 0 and self.dir_y == 0:
            return
        angle = math.degrees(math.atan2(-self.dir_y, self.dir_x))
        if self.weapon_type == "sniper":
            rotation = angle + 90       # 탄두가 이미지 아래쪽
        elif self.weapon_type in ("machinegun", "rocket", "javelin", "zombie_snipe") or self.bullet_type in ("rocket", "laser"):
            rotation = angle - 90       # 탄두가 이미지 위쪽
        else:
            return                      # 둥근 탄은 회전할 필요 없음
        self.image = pygame.transform.rotate(self.image, rotation)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        # 생성 후 bullet.speed = ... 로 바꿔도 실제 이동 속도에 반영되도록 속도 벡터를 다시 계산
        # (예전에는 생성 시점에만 계산해서 무기별 탄속/스킬 탄속 설정이 전부 무시됐음)
        self._speed = value
        self.vel_x = self.dir_x * value
        self.vel_y = self.dir_y * value

    def update(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.center = (round(self.pos_x), round(self.pos_y))
        self.lifetime += 1

        # 총알 꼬리 (로켓 연기, 플라즈마 잔광, 저격 궤적, 용 파이어볼)
        if self.trail is not None:
            color, size, life = self.trail
            fx.trail(self.pos_x - self.vel_x * 0.5, self.pos_y - self.vel_y * 0.5, color, size, life)
            if self.weapon_type == "sniper":  # 빠른 탄은 중간에 하나 더 찍어서 끊기지 않게
                fx.trail(self.pos_x - self.vel_x, self.pos_y - self.vel_y, color, size, life)

        # 속성탄 꼬리 (플레이어 총알만, 가진 속성 색을 번갈아)
        if fx.elements and not self.is_enemy:
            element = fx.elements[(self.lifetime // 2) % len(fx.elements)]
            colors = ELEMENT_COLORS[element]
            fx.trail(self.pos_x, self.pos_y, colors[self.lifetime % 2], 3, 9)

        # 발사 지점에서 최대 사거리보다 멀어지면 제거
        # (예전에는 월드 원점 기준 ±10000이라, 플레이어가 원점에서 멀리 가면 쏘자마자 총알이 사라졌음)
        travel_x = self.pos_x - self.start_x
        travel_y = self.pos_y - self.start_y
        if travel_x * travel_x + travel_y * travel_y > self.max_range * self.max_range:
            self.kill()

        # 로켓은 일정 시간 후 사라짐
        if (self.bullet_type == "rocket" or self.weapon_type == "rocket") and self.lifetime > 120:
            self.kill()


# 레이저 클래스
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, duration=30):
        super().__init__()
        self.image = pygame.Surface((600, 5))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.duration = duration
        self.created_time = pygame.time.get_ticks()

        # 방향에 따라 회전
        angle = math.degrees(math.atan2(direction_y, direction_x))
        rotated_image = pygame.transform.rotate(self.image, -angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if pygame.time.get_ticks() - self.created_time > self.duration * 1000 / 60:
            self.kill()


_explosion_frames = {}


# 폭발 클래스 (로켓/스킬/폭탄좀비 폭발 공용) - 판정과는 무관한 연출
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=100):
        super().__init__()
        self.radius = int(radius)
        size = self.radius * 2 + 6
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.created_time = pygame.time.get_ticks()
        self.duration = 30  # 30 프레임
        self.frames = 0
        self._draw_frame()
        # 파편이 튀고, 큰 폭발은 화면이 흔들림
        fx.explosion_debris(x, y, self.radius)
        if self.radius >= 100:
            fx.add_shake(min(12, self.radius / 18))

    def _draw_frame(self):
        # 같은 크기 폭발의 같은 프레임은 한 번만 그려 두고 같이 씀 (예전에는 폭발마다 매 프레임 새로 그렸음)
        key = (self.radius, self.frames, self.duration)
        image = _explosion_frames.get(key)
        if image is None:
            if len(_explosion_frames) > 2000:
                _explosion_frames.clear()
            image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            progress = self.frames / self.duration
            c = image.get_width() // 2
            grow = min(1.0, 0.35 + progress * 2.4)   # 처음에 빠르게 커짐
            r = max(2, int(self.radius * grow))
            fade = max(0.0, 1 - progress)
            pygame.draw.circle(image, (255, 110, 0, int(160 * fade)), (c, c), r)
            pygame.draw.circle(image, (255, 200, 70, int(190 * fade)), (c, c), max(1, int(r * 0.62)))
            if progress < 0.35:  # 중심 섬광
                pygame.draw.circle(image, (255, 255, 230, int(255 * (1 - progress / 0.35))), (c, c), max(1, int(r * 0.33)))
            pygame.draw.circle(image, (255, 235, 160, int(230 * fade)), (c, c), r, 3)  # 충격파 테두리
            _explosion_frames[key] = image
        self.image = image

    def update(self):
        self.frames += 1
        if self.frames >= self.duration:
            self.kill()
            return
        self._draw_frame()


def apply_player_damage(player, amount):
    # 무적 (카타나 일섬 직후)
    if getattr(player, "invuln_time", 0) > 0:
        return
    # 회피 (levels["dodge"] * 5%): 접촉뿐 아니라 투사체/폭발/독 등 모든 피해에 적용
    if random.random() < player.levels.get("dodge", 0) * 0.05:
        return
    if player.corrode_time > 0:
        amount *= 1.3  # 부식 (산성좀비)
    if player.shield_active:
        amount *= 0.5
    player.health -= amount


def get_crit_multiplier(player):
    """치명타 피해 배율 (기본 1.3배 + 저격총 "치명타 데미지" 업그레이드)"""
    return CRIT_BASE_MULT + SNIPER_CRIT_DAMAGE_UPGRADE * player.skill_upgrades["sniper"].get("crit_damage", 0)


def roll_crit_damage(player, damage, target=None, bonus_chance=0.0):
    """치명타 판정 (levels["crit"] * 5% (+ bonus_chance) 확률로 치명타 배율만큼 데미지). target을 주면 치명타 숫자 연출용으로 표시"""
    if random.random() < player.levels.get("crit", 0) * 0.05 + bonus_chance:
        if target is not None:
            target.crit_marked = True
        return damage * get_crit_multiplier(player)
    return damage


def apply_hit_elements(player, zombie, zombies, base_damage, chain_range=150):
    """속성탄 업그레이드 효과 (화염: 불붙임 / 얼음: 둔화 / 전기: 주변 2마리에게 연쇄 피해) - 일섬 등 스킬에도 적용"""
    if player.skills.get("skill_fire_bullets", False):
        zombie.burn_time = max(zombie.burn_time, 180)
        zombie.burn_damage_cooldown = 0
        fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "fire")
    if player.skills.get("skill_ice_bullets", False):
        zombie.slow_time = max(zombie.slow_time, 120)
        zombie.slow_multiplier = min(zombie.slow_multiplier, 0.6)
        fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "ice")
    if player.skills.get("skill_electric_bullets", False):
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


def melee_sweep(melee, zombies):
    """근접 무기를 휘두르는 도중 범위(부채꼴)에 새로 들어온 좀비도 맞음 - 한 번 휘두를 때 좀비마다 한 번만
    (예전에는 클릭한 순간 범위 안에 있던 좀비만 맞고, 휘두르는 동안 들어온 좀비는 무기가 지나가도 안 맞았음)"""
    player = melee.owner
    if player is None:
        return
    px, py = player.rect.center
    knockback_mult = get_knockback_multiplier(player)
    for zombie in list(zombies):
        if zombie.health <= 0 or zombie in melee.has_hit:
            continue
        dx, dy = zombie.rect.centerx - px, zombie.rect.centery - py
        dist = math.hypot(dx, dy)
        in_range = dist < Melee.CLOSE_HIT_RADIUS
        if not in_range and dist < melee.attack_range:
            angle_diff = abs((math.degrees(math.atan2(-dy, dx)) - melee.base_angle + 180) % 360 - 180)
            in_range = angle_diff <= melee.hit_half_arc
        if not in_range:
            continue
        melee.has_hit.add(zombie)
        zombie.health -= roll_crit_damage(player, melee.damage, zombie) * get_damage_multiplier(zombie)
        fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, FX_WEAPON_COLORS.get(melee.weapon_type, WHITE))
        apply_hit_elements(player, zombie, zombies, melee.damage, 150)
        if dist > 0:
            zombie.knockback_vel_x = dx / dist * melee.knockback_power / 100 * knockback_mult
            zombie.knockback_vel_y = dy / dist * melee.knockback_power / 100 * knockback_mult


def get_knockback_multiplier(player):
    """넉백 강화 업그레이드 반영 (1회당 +10%)"""
    return 1.0 + 0.1 * player.levels.get("knockback", 0)


def get_spear_speed_factor(player):
    """창 데미지 배율 = 현재 이동속도 / 기본 이동속도 (이동속도 업그레이드·버프·둔화 반영)"""
    speed = player.speed * player.slow_multiplier
    if player.speed_buff_time > 0:
        speed *= ITEM_BUFF_MULTIPLIER
    return max(0.4, speed / SPEAR_BASE_SPEED)


def get_weapon_damage(player):
    """현재 무기 공격력 (공격력 아이템 버프 반영, 창은 이동속도 비례)"""
    damage = player.weapon.damage
    if player.damage_buff_time > 0:
        damage *= ITEM_BUFF_MULTIPLIER
    if player.weapon.weapon_type == "spear":
        damage *= get_spear_speed_factor(player)
    return damage


def spear_charge(player, zombies):
    """창 돌진: 창을 든 채 달리면 공격하지 않아도 정면의 좀비에게 피해 + 넉백 (좀비마다 0.5초에 한 번)"""
    if player.weapon.weapon_type != "spear" or getattr(player, "move_dir", None) is None:
        return
    mx, my = player.move_dir
    px, py = player.rect.center
    now = pygame.time.get_ticks()
    damage = get_weapon_damage(player) * SPEAR_CHARGE_RATIO
    min_dot = math.cos(math.radians(SPEAR_CHARGE_HALF_ARC))
    for zombie in list(zombies):
        if zombie.health <= 0:
            continue
        dx, dy = zombie.rect.centerx - px, zombie.rect.centery - py
        dist = math.hypot(dx, dy)
        if dist < 1 or dist > SPEAR_CHARGE_REACH + zombie.size * 0.4 or (dx * mx + dy * my) / dist < min_dot:
            continue
        cooldowns = zombie.__dict__.setdefault("_spear_cd", {})
        if cooldowns.get(player, -1) > now:
            continue
        cooldowns[player] = now + SPEAR_CHARGE_COOLDOWN_MS
        zombie.health -= roll_crit_damage(player, damage, zombie) * get_damage_multiplier(zombie)
        push_zombie(zombie, px, py, SPEAR_CHARGE_KNOCKBACK)
        fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, FX_WEAPON_COLORS["spear"])


def get_damage_multiplier(zombie):
    """좀비가 받는 피해 배율 (모든 공격에 공통 적용): 갑옷/방패/철갑옷 + 수호 오라"""
    mult = 1.0
    if zombie.zombie_type == "armored" and hasattr(zombie, 'armor_reduction'):
        mult = zombie.armor_reduction
    elif zombie.zombie_type == "shield" and hasattr(zombie, 'shield_reduction'):
        mult = zombie.shield_reduction
    elif zombie.zombie_type == "iron":
        mult = 0.75  # 철갑옷: 받는 피해 25% 감소
    return mult * getattr(zombie, "guard_mult", 1.0)


def compensate_paused_time(player, paused_ms):
    """메뉴(일시정지/업그레이드)로 멈춰 있던 시간만큼 쿨타임을 뒤로 미룸 (메뉴 중에 쿨타임이 흐르지 않도록)"""
    for weapon_type, ready_time in player.skill_cooldowns.items():
        if ready_time > 0:
            player.skill_cooldowns[weapon_type] = ready_time + paused_ms
    if player.weapon:
        player.weapon.last_shot_time += paused_ms


def trigger_bomb_explosion(zombie, player, zombies, all_sprites, explosions, radius, damage, player_damage=None):
    explosion = Explosion(zombie.rect.centerx, zombie.rect.centery, radius)
    all_sprites.add(explosion)
    if explosions is not None:
        explosions.add(explosion)

    # 플레이어가 받는 폭발 피해 (지정하지 않으면 좀비와 같은 피해)
    if player_damage is None:
        player_damage = damage
    player_distance = math.sqrt((player.rect.centerx - zombie.rect.centerx) ** 2 + (player.rect.centery - zombie.rect.centery) ** 2)
    if player_distance < radius:
        apply_player_damage(player, player_damage)

    for other_zombie in list(zombies):
        if other_zombie is zombie or other_zombie not in zombies:
            continue

        distance = math.sqrt((other_zombie.rect.centerx - zombie.rect.centerx) ** 2 + (other_zombie.rect.centery - zombie.rect.centery) ** 2)
        if distance >= radius:
            continue

        damage_multiplier = get_damage_multiplier(other_zombie)

        other_zombie.health -= damage * damage_multiplier


def get_exp_reward(player, wave):
    """경험치 보상 계산 (exp_boost 중첩 반영: 획득 1회당 +20%)"""
    base_exp = int(20 + (wave - 1) * 8)
    exp_multiplier = 1.0 + (0.2 * player.levels.get("exp_boost", 0))
    return int(base_exp * exp_multiplier)


def get_auto_aim_target(player, zombies, max_range=600):
    nearest = None
    nearest_dist = max_range
    for zombie in zombies:
        dx = zombie.rect.centerx - player.rect.centerx
        dy = zombie.rect.centery - player.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < nearest_dist:
            nearest = zombie
            nearest_dist = dist

    if nearest is None:
        return None
    return nearest.rect.centerx, nearest.rect.centery


# ===== 무기별 우클릭 스킬 =====
# 나무 방망이: 홈런 / 카타나: 일섬 / 도끼: 대회전 베기 / 창: 물보라 / 해머: 대지 강타 / 글로브: 러시
# 글록: 항공 폭격 / 기관총: 포탑 설치 / 샷건: 용의 숨결 / 저격총: 도탄 사격 / 플라즈마: 블랙홀 / 로켓: 미사일 폭격

def skill_damage(zombie, amount):
    """스킬 피해 (갑옷/방패/수호 오라 감소 적용)"""
    zombie.health -= amount * get_damage_multiplier(zombie)


def push_zombie(zombie, from_x, from_y, power):
    dx = zombie.rect.centerx - from_x
    dy = zombie.rect.centery - from_y
    dist = math.hypot(dx, dy) or 1
    zombie.knockback_vel_x = dx / dist * power
    zombie.knockback_vel_y = dy / dist * power


def zombies_in_cone(zombies, ox, oy, angle, half_angle, radius):
    """(ox, oy)에서 angle(라디안) 방향 ± half_angle, 반경 radius 안의 좀비"""
    result = []
    for zombie in zombies:
        if zombie.health <= 0:
            continue
        dx = zombie.rect.centerx - ox
        dy = zombie.rect.centery - oy
        dist = math.hypot(dx, dy)
        if dist > radius + zombie.size * 0.3:
            continue
        diff = abs((math.atan2(dy, dx) - angle + math.pi) % (math.pi * 2) - math.pi)
        if dist < 40 or diff <= half_angle:
            result.append(zombie)
    return result


def zombies_near_line(zombies, x1, y1, x2, y2, width):
    """선분 (x1,y1)-(x2,y2)에서 width 안에 있는 좀비"""
    result = []
    lx, ly = x2 - x1, y2 - y1
    length_sq = lx * lx + ly * ly or 1
    for zombie in zombies:
        if zombie.health <= 0:
            continue
        px, py = zombie.rect.centerx - x1, zombie.rect.centery - y1
        t = max(0.0, min(1.0, (px * lx + py * ly) / length_sq))
        if math.hypot(px - lx * t, py - ly * t) < width + zombie.size * 0.3:
            result.append(zombie)
    return result


def nearest_zombie(zombies, x, y, max_range):
    best, best_dist = None, max_range
    for zombie in zombies:
        if zombie.health <= 0:
            continue
        dist = math.hypot(zombie.rect.centerx - x, zombie.rect.centery - y)
        if dist < best_dist:
            best, best_dist = zombie, dist
    return best


class ConeFlash(pygame.sprite.Sprite):
    """부채꼴 범위 섬광 (스킬이 맞는 범위를 그대로 보여줌)"""
    def __init__(self, x, y, angle, half_angle, radius, color, duration=16):
        super().__init__()
        self.center = (x, y)
        self.angle, self.half_angle, self.radius = angle, half_angle, int(radius)
        self.color = color
        self.duration = duration
        self.frames = 0
        self._draw()

    def _draw(self):
        size = self.radius * 2 + 8
        c = size // 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        fade = 1 - self.frames / self.duration
        points = [(c, c)]
        steps = max(3, int(math.degrees(self.half_angle) / 5))
        for i in range(steps * 2 + 1):
            a = self.angle - self.half_angle + self.half_angle * i / steps
            points.append((c + math.cos(a) * self.radius, c + math.sin(a) * self.radius))
        r, g, b = self.color
        pygame.draw.polygon(self.image, (r, g, b, int(120 * fade)), points)
        pygame.draw.lines(self.image, (255, 255, 255, int(200 * fade)), False, points[1:], 3)
        self.rect = self.image.get_rect(center=self.center)

    def update(self):
        self.frames += 1
        if self.frames >= self.duration:
            self.kill()
            return
        self._draw()


class LineFlash(pygame.sprite.Sprite):
    """두 점을 잇는 굵은 광선/베기 궤적"""
    def __init__(self, x1, y1, x2, y2, color, width=16, duration=18):
        super().__init__()
        self.points = (x1, y1, x2, y2)
        self.color, self.width, self.duration = color, width, duration
        self.frames = 0
        self._draw()

    def _draw(self):
        x1, y1, x2, y2 = self.points
        pad = self.width + 6
        left, top = min(x1, x2) - pad, min(y1, y2) - pad
        w, h = int(abs(x2 - x1) + pad * 2), int(abs(y2 - y1) + pad * 2)
        self.image = pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
        fade = 1 - self.frames / self.duration
        p1, p2 = (x1 - left, y1 - top), (x2 - left, y2 - top)
        r, g, b = self.color
        pygame.draw.line(self.image, (r, g, b, int(150 * fade)), p1, p2, max(2, int(self.width * (0.6 + 0.4 * fade))))
        pygame.draw.line(self.image, (255, 255, 255, int(255 * fade)), p1, p2, max(1, int(self.width * 0.35)))
        self.rect = self.image.get_rect(center=((x1 + x2) / 2, (y1 + y2) / 2))

    def update(self):
        self.frames += 1
        if self.frames >= self.duration:
            self.kill()
            return
        self._draw()


class SkillVisual(pygame.sprite.Sprite):
    """지속형 스킬이 직접 그림을 바꾸는 스프라이트 (스스로는 아무것도 하지 않음)"""
    def __init__(self, image, center):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=center)

    def update(self):
        pass


class ActiveSkill:
    """여러 프레임 동안 유지되는 스킬 (main에서 매 프레임 update 호출, False를 돌려주면 끝)"""
    def __init__(self, duration):
        self.frames = 0
        self.duration = duration
        self.visual = None

    def update(self, player, zombies, bullets, all_sprites, explosions):
        self.frames += 1
        alive = self.frames < self.duration and self.tick(player, zombies, bullets, all_sprites, explosions) is not False
        if not alive and self.visual is not None:
            self.visual.kill()
        return alive

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        return True


class GreatSwingSkill(ActiveSkill):
    """도끼 대회전 베기: 도끼를 크게 한 바퀴 휘둘러 날이 지나가는 좀비를 베고, 준 피해만큼 흡혈"""
    SWING_FRAMES = 18    # 한 바퀴 0.3초

    def __init__(self, player, all_sprites, damage, radius, knockback, aim):
        super().__init__(self.SWING_FRAMES + 10)   # 끝난 뒤 잔상 0.17초
        self.damage, self.radius, self.knockback, self.aim = damage, radius, knockback, aim
        self.axe_image = pygame.transform.scale_by(Melee(0, 0, 1, 0, 1, "axe").base_image, 1.6)
        self.hit = set()
        self.healed = 0.0
        size = int(radius * 2 + 80)
        self.visual = SkillVisual(pygame.Surface((size, size), pygame.SRCALPHA), player.rect.center)
        all_sprites.add(self.visual)
        fx.add_shake(5)

    def blade_angle(self, frame):
        return self.aim + 2 * math.pi * min(1.0, frame / self.SWING_FRAMES)

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        cx, cy = player.rect.center
        if self.frames <= self.SWING_FRAMES:
            prev, now = self.blade_angle(self.frames - 1), self.blade_angle(self.frames)
            dealt = 0.0
            for zombie in list(zombies):
                if zombie.health <= 0 or zombie in self.hit:
                    continue
                dx, dy = zombie.rect.centerx - cx, zombie.rect.centery - cy
                dist = math.hypot(dx, dy)
                if dist > self.radius + max(zombie.rect.width, zombie.rect.height) / 2:
                    continue
                # 날이 이번 프레임에 지나간 각도 안에 있으면 맞음 (몸에 붙은 좀비는 바로 맞음)
                rel = (math.atan2(dy, dx) - prev) % (2 * math.pi)
                if dist > 40 and rel > now - prev:
                    continue
                self.hit.add(zombie)
                before = zombie.health
                skill_damage(zombie, self.damage)
                dealt += before - max(0.0, zombie.health)
                push_zombie(zombie, cx, cy, self.knockback)
                fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, FX_WEAPON_COLORS["axe"])
            # 흡혈: 준 피해의 10% (한 번 휘두를 때 최대 100)
            if dealt > 0 and player.health < player.max_health and self.healed < AXE_SKILL_LIFESTEAL_CAP:
                heal = min(AXE_SKILL_LIFESTEAL_CAP - self.healed, dealt * AXE_SKILL_LIFESTEAL, player.max_health - player.health)
                player.health += heal
                self.healed += heal
            if self.frames == self.SWING_FRAMES and self.healed >= 1:
                fx.add_text(player.rect.centerx, player.rect.top - 26, f"흡혈 +{self.healed:.0f}", (120, 255, 140), big=True)
        # 그림: 큰 범위 원 + 날이 지나간 자리의 붉은 궤적 + 커다란 도끼
        size = self.visual.image.get_width()
        c = size // 2
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        fade = 1.0 if self.frames <= self.SWING_FRAMES else max(0.0, 1 - (self.frames - self.SWING_FRAMES) / 10)
        pygame.draw.circle(image, (255, 90, 90, int(35 * fade)), (c, c), int(self.radius))
        pygame.draw.circle(image, (255, 150, 150, int(140 * fade)), (c, c), int(self.radius), 3)
        current = self.blade_angle(min(self.frames, self.SWING_FRAMES))
        for i in range(14):   # 궤적: 날 뒤쪽으로 갈수록 흐려짐
            a = current - i * 0.16
            if a < self.aim:
                break
            alpha = int((200 - i * 13) * fade)
            if alpha <= 0:
                break
            inner, outer = self.radius * 0.35, self.radius
            pygame.draw.line(image, (255, 120, 100, alpha), (c + math.cos(a) * inner, c + math.sin(a) * inner),
                             (c + math.cos(a) * outer, c + math.sin(a) * outer), 7)
        if self.frames <= self.SWING_FRAMES:
            rotated = pygame.transform.rotate(self.axe_image, -math.degrees(current))
            reach = self.radius - self.axe_image.get_width() / 2
            image.blit(rotated, rotated.get_rect(center=(c + math.cos(current) * reach, c + math.sin(current) * reach)))
        self.visual.image = image
        self.visual.rect = image.get_rect(center=(cx, cy))


_plane_images = {}


def _plane_image(angle_deg):
    """폭격기 그림 (오른쪽을 보는 전투기를 진행 방향으로 회전)"""
    key = int(round(angle_deg)) % 360
    image = _plane_images.get(key)
    if image is None:
        base = pygame.Surface((120, 100), pygame.SRCALPHA)
        body = (150, 160, 175)
        dark = (95, 105, 120)
        pygame.draw.polygon(base, dark, [(30, 50), (62, 6), (74, 6), (70, 50)])            # 왼쪽 날개
        pygame.draw.polygon(base, dark, [(30, 50), (62, 94), (74, 94), (70, 50)])          # 오른쪽 날개
        pygame.draw.polygon(base, dark, [(6, 50), (14, 30), (22, 30), (22, 50)])           # 꼬리 날개
        pygame.draw.polygon(base, dark, [(6, 50), (14, 70), (22, 70), (22, 50)])
        pygame.draw.ellipse(base, body, (4, 40, 110, 20))                                  # 몸통
        pygame.draw.ellipse(base, (90, 200, 255), (78, 44, 22, 10))                        # 조종석
        pygame.draw.circle(base, (255, 170, 60), (8, 50), 5)                               # 엔진 불꽃
        image = _plane_images[key] = pygame.transform.rotozoom(base, key, 1.6)   # 크게 (1.6배)
    return image


class AirStrikeSkill(ActiveSkill):
    """글록 항공 폭격: 비행기가 화면 밖에서 날아와 조준 방향 직선을 따라 폭탄을 줄줄이 떨어뜨림"""
    PLANE_SPEED = 28        # 비행기 속도 (px/프레임)
    ENTRY = 1100            # 플레이어 뒤쪽 이만큼 떨어진 곳(화면 밖)에서 진입
    SPACING = 70            # 폭탄 간격
    FALL_FRAMES = 12        # 폭탄이 떨어지는 시간
    BLAST_RADIUS = 75

    def __init__(self, player, all_sprites, damage, dir_x, dir_y, length, blast_radius=None):
        cx, cy = player.rect.center
        self.dir_x, self.dir_y, self.damage = dir_x, dir_y, damage
        self.blast_radius = blast_radius or self.BLAST_RADIUS
        self.start = (cx - dir_x * self.ENTRY, cy - dir_y * self.ENTRY)
        offsets = list(range(-150, int(length) + 1, self.SPACING))
        self.drops = [(self.ENTRY + d, cx + dir_x * d, cy + dir_y * d) for d in offsets]   # (진입점에서의 거리, x, y)
        self.travel = self.ENTRY + length + 1000
        super().__init__(int(self.travel / self.PLANE_SPEED) + self.FALL_FRAMES + 5)
        self.next_drop = 0
        self.falling = []
        angle = -math.degrees(math.atan2(dir_y, dir_x))
        self.visual = SkillVisual(_plane_image(angle), self.start)
        all_sprites.add(self.visual)
        # 폭격 예고선 (붉은 선)
        first, last = self.drops[0], self.drops[-1]
        all_sprites.add(LineFlash(first[1], first[2], last[1], last[2], (255, 70, 50), width=int(self.blast_radius / 6), duration=50))
        fx.add_text(cx, player.rect.top - 30, "항공 폭격!", (255, 200, 90), big=True)

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        dist = self.frames * self.PLANE_SPEED
        px, py = self.start[0] + self.dir_x * dist, self.start[1] + self.dir_y * dist
        self.visual.rect = self.visual.image.get_rect(center=(int(px), int(py)))
        if dist < self.travel and self.frames % 2 == 0:
            fx.trail(px - self.dir_x * 55, py - self.dir_y * 55, (255, 190, 90), 4, 10)    # 엔진 불꽃 꼬리
        while self.next_drop < len(self.drops) and dist >= self.drops[self.next_drop][0]:
            _, bx, by = self.drops[self.next_drop]
            self.falling.append([bx, by, self.FALL_FRAMES])
            self.next_drop += 1
        for bomb in self.falling:
            bomb[2] -= 1
            fx.trail(bomb[0], bomb[1] - bomb[2] * 6, (60, 60, 60), 3, 3)                       # 떨어지는 폭탄
            if bomb[2] <= 0:
                bx, by = bomb[0], bomb[1]
                boom = Explosion(bx, by, self.blast_radius)
                explosions.add(boom)
                all_sprites.add(boom)
                for zombie in list(zombies):
                    if zombie.health > 0 and math.hypot(zombie.rect.centerx - bx, zombie.rect.centery - by) < self.blast_radius:
                        skill_damage(zombie, self.damage)
                        push_zombie(zombie, bx, by, 6)
                fx.add_shake(2)
        self.falling = [bomb for bomb in self.falling if bomb[2] > 0]
        if dist >= self.travel and self.next_drop >= len(self.drops) and not self.falling:
            return False
        if dist >= self.travel:
            self.visual.rect.center = (-99999, -99999)   # 화면 밖으로 사라짐


class RicochetSkill(ActiveSkill):
    """저격총 도탄 사격: 한 발을 쏘면 처음 맞은 좀비에서 주변 좀비로 계속 튕겨 다님
    (아직 안 맞은 좀비를 먼저 노리고, 없으면 이미 맞은 좀비에게라도 튕김)"""
    HOP_FRAMES = 4        # 한 번 튕기는 데 걸리는 프레임 (0.07초)
    BOUNCE_RANGE = 450    # 다음 대상을 찾는 거리
    RANGE = 1400          # 첫 발 사거리

    def __init__(self, cx, cy, dir_x, dir_y, damage, bounces, zombies, all_sprites):
        super().__init__((bounces + 2) * self.HOP_FRAMES + 2)
        self.damage, self.bounces_left = damage, bounces
        self.pos = (cx, cy)
        self.hit_count = {}
        self.hits = 0
        end_x, end_y = cx + dir_x * self.RANGE, cy + dir_y * self.RANGE
        on_line = zombies_near_line(zombies, cx, cy, end_x, end_y, 28)
        self.target = min(on_line, key=lambda z: math.hypot(z.rect.centerx - cx, z.rect.centery - cy)) if on_line else None
        if self.target is None:   # 아무도 없으면 허공으로 날아감
            all_sprites.add(LineFlash(cx, cy, end_x, end_y, (150, 230, 255), width=8, duration=12))
        fx.add_shake(3)

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        if self.target is None:
            return False
        if self.frames % self.HOP_FRAMES:
            return True
        target = self.target
        if target not in zombies or target.health <= 0:      # 날아가는 사이 다른 공격에 죽었으면 근처의 다른 좀비로
            target = self._next_target(zombies, None)
            if target is None:
                return False
        tx, ty = target.rect.center
        all_sprites.add(LineFlash(self.pos[0], self.pos[1], tx, ty, (180, 240, 255), width=11, duration=24))
        # 일반 탄환처럼 기본 공격 업그레이드 적용: 치명타 + 속성탄 + 폭발 공격
        was_marked = getattr(target, "crit_marked", False)
        dealt = roll_crit_damage(player, self.damage, target, SNIPER_RICOCHET_CRIT_BONUS)
        skill_damage(target, dealt)
        if dealt > self.damage:   # 치명타: 붉은 섬광 + 글자
            fx.ring(tx, ty, (255, 80, 80), 46, count=16, size=3)
            fx.add_text(tx, ty - 30, "치명타!", (255, 90, 90), big=True, life=36)
        elif not was_marked:
            target.crit_marked = False
        apply_hit_elements(player, target, zombies, self.damage)
        if player.skills.get("skill_explosion", False) and player.explosion_cooldown <= 0:
            player.explosion_cooldown = EXPLOSION_SKILL_COOLDOWN
            boom = Explosion(tx, ty, 70)
            explosions.add(boom)
            all_sprites.add(boom)
            for other in list(zombies):
                if other is not target and math.hypot(other.rect.centerx - tx, other.rect.centery - ty) < 70:
                    other.health -= self.damage * EXPLOSION_SKILL_RATIO * get_damage_multiplier(other)
        fx.hit_spark(tx, ty, (150, 230, 255))
        fx.ring(tx, ty, (150, 230, 255), 34, count=12)
        self.hit_count[target] = self.hit_count.get(target, 0) + 1
        self.hits += 1
        self.pos = (tx, ty)
        if self.bounces_left <= 0:
            fx.add_text(tx, ty - 40, f"도탄 x{self.hits}", (150, 230, 255))
            return False
        self.target = self._next_target(zombies, target)
        if self.target is None:
            fx.add_text(tx, ty - 40, f"도탄 x{self.hits}", (150, 230, 255))
            return False
        self.bounces_left -= 1
        return True

    def _next_target(self, zombies, current):
        """지금 위치에서 가장 가까운 좀비 (안 맞은 좀비 우선)"""
        px, py = self.pos
        best, best_key = None, None
        for zombie in zombies:
            if zombie is current or zombie.health <= 0:
                continue
            d = math.hypot(zombie.rect.centerx - px, zombie.rect.centery - py)
            if d > self.BOUNCE_RANGE:
                continue
            key = (self.hit_count.get(zombie, 0), d)
            if best_key is None or key < best_key:
                best, best_key = zombie, key
        return best


class WaterSplashSkill(ActiveSkill):
    """창 물보라: 하늘에서 거대한 창이 내 자리에 꽂히고, 그 자리에서 물결이 퍼져 닿은 좀비를 튕겨 내고 느리게 함"""
    FALL_FRAMES = 14       # 창이 떨어지는 시간 (0.23초)
    SPREAD_FRAMES = 18     # 물결이 끝까지 퍼지는 시간 (0.3초)
    FADE_FRAMES = 16
    DROP_HEIGHT = 520

    def __init__(self, player, all_sprites, damage, radius, slow):
        super().__init__(self.FALL_FRAMES + self.SPREAD_FRAMES + self.FADE_FRAMES)
        self.damage, self.radius, self.slow = damage, radius, slow
        self.center = player.rect.center
        self.hit = set()
        size = int(radius * 2 + 40)
        self.visual = SkillVisual(pygame.Surface((size, size), pygame.SRCALPHA), self.center)
        all_sprites.add(self.visual)
        self.spear_image = pygame.transform.rotate(draw_spear_art(300, 15), -90)     # 날이 아래를 향함
        self.spear = SkillVisual(self.spear_image.copy(), (self.center[0], self.center[1] - self.DROP_HEIGHT))
        all_sprites.add(self.spear)

    def update(self, player, zombies, bullets, all_sprites, explosions):
        alive = super().update(player, zombies, bullets, all_sprites, explosions)
        if not alive:
            self.spear.kill()
        return alive

    def _place_spear(self, tip_y):
        cx = self.center[0]
        self.spear.rect = self.spear.image.get_rect(midbottom=(cx, int(tip_y)))

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        cx, cy = self.center
        size = self.visual.image.get_width()
        c = size // 2
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        if self.frames <= self.FALL_FRAMES:
            # 1) 거대한 창이 떨어짐 (점점 빨라짐) + 바닥 그림자가 커짐
            t = self.frames / self.FALL_FRAMES
            self._place_spear(cy + 12 - self.DROP_HEIGHT * (1 - t * t))
            shadow_w = int(30 + 60 * t)
            pygame.draw.ellipse(image, (0, 0, 0, int(60 + 80 * t)), (c - shadow_w // 2, c - shadow_w // 6, shadow_w, shadow_w // 3))
            if self.frames == self.FALL_FRAMES:   # 꽂히는 순간
                fx.add_shake(9)
                fx.ring(cx, cy, (150, 220, 255), 70, count=30, size=4)
                fx.burst(cx, cy, (120, 200, 255), 26, speed=(2, 6), size=(2, 5), life=(14, 26), drag=0.9, gravity=0.15)
            self.visual.image = image
            self.visual.rect = image.get_rect(center=(cx, cy))
            return True
        # 2) 물결이 퍼짐
        spread = self.frames - self.FALL_FRAMES
        progress = min(1.0, spread / self.SPREAD_FRAMES)
        wave = self.radius * progress
        if spread <= self.SPREAD_FRAMES:
            for zombie in list(zombies):
                if zombie.health <= 0 or zombie in self.hit:
                    continue
                if math.hypot(zombie.rect.centerx - cx, zombie.rect.centery - cy) <= wave + zombie.size * 0.4:
                    self.hit.add(zombie)
                    skill_damage(zombie, self.damage)
                    push_zombie(zombie, cx, cy, SPLASH_KNOCKBACK)
                    zombie.slow_time = max(zombie.slow_time, SPLASH_SLOW_FRAMES)
                    zombie.slow_multiplier = min(zombie.slow_multiplier, self.slow)
                    fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "ice")
            for i in range(6):   # 물결 가장자리에서 튀는 물방울
                a = (spread * 0.9 + i * math.pi / 3) % (2 * math.pi)
                fx.burst(cx + math.cos(a) * wave, cy + math.sin(a) * wave, (120, 200, 255), 1,
                         speed=(1.0, 3.0), size=(2, 4), life=(12, 20), drag=0.92, gravity=0.1)
        fade = 1.0 if spread <= self.SPREAD_FRAMES else max(0.0, 1 - (spread - self.SPREAD_FRAMES) / self.FADE_FRAMES)
        r = max(4, int(wave))
        pygame.draw.circle(image, (70, 150, 255, int(55 * fade)), (c, c), r)
        pygame.draw.circle(image, (150, 220, 255, int(220 * fade)), (c, c), r, 8)
        pygame.draw.circle(image, (230, 250, 255, int(200 * fade)), (c, c), max(2, r - 10), 2)
        pygame.draw.ellipse(image, (0, 0, 0, int(140 * fade)), (c - 45, c - 15, 90, 30))      # 꽂힌 창 밑 그림자
        self.visual.image = image
        self.visual.rect = image.get_rect(center=(cx, cy))
        # 꽂힌 창은 그대로 있다가 서서히 사라짐
        self.spear.image = self.spear_image.copy()
        self.spear.image.set_alpha(int(255 * fade))
        self._place_spear(cy + 12)


class TurretSkill(ActiveSkill):
    """기관총 포탑: 설치한 자리에서 가장 가까운 좀비를 자동 사격"""
    def __init__(self, x, y, duration, damage, all_sprites):
        super().__init__(duration)
        self.x, self.y, self.damage = x, y, damage
        self.aim = 0.0
        self.visual = SkillVisual(pygame.Surface((60, 60), pygame.SRCALPHA), (x, y))
        all_sprites.add(self.visual)
        fx.ring(x, y, (180, 180, 180), 50, count=16)

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        target = nearest_zombie(zombies, self.x, self.y, 520)
        if target is not None:
            self.aim = math.atan2(target.rect.centery - self.y, target.rect.centerx - self.x)
            if self.frames % 7 == 0:
                bullet = Bullet(self.x, self.y, target.rect.centerx, target.rect.centery, self.damage, "normal", "machinegun")
                bullet.speed = 15
                bullets.add(bullet)
                all_sprites.add(bullet)
                fx.muzzle_flash(self.x + math.cos(self.aim) * 26, self.y + math.sin(self.aim) * 26,
                                math.cos(self.aim), math.sin(self.aim), FX_WEAPON_COLORS["machinegun"])
        image = pygame.Surface((60, 60), pygame.SRCALPHA)
        remain = 1 - self.frames / self.duration
        pygame.draw.circle(image, (70, 70, 80), (30, 30), 16)
        pygame.draw.circle(image, (150, 150, 160), (30, 30), 16, 3)
        pygame.draw.arc(image, (120, 255, 120), (8, 8, 44, 44), 0, math.pi * 2 * remain, 3)  # 남은 시간
        end = (30 + math.cos(self.aim) * 26, 30 + math.sin(self.aim) * 26)
        pygame.draw.line(image, (30, 30, 30), (30, 30), end, 9)
        pygame.draw.line(image, (160, 160, 170), (30, 30), end, 5)
        self.visual.image = image


class BlackHoleSkill(ActiveSkill):
    """플라즈마 블랙홀: 좀비를 중심으로 끌어당기며 계속 피해.
    유지되는 동안 블랙홀 안에서 죽은 좀비 수를 세었다가, 사라질 때 그 수만큼 강해지는 붕괴 폭발을 일으킴"""
    KILL_BONUS = 1.5  # 처치 1마리당 붕괴 폭발 피해 (지속 피해 1회의 1.5배)

    def __init__(self, x, y, radius, damage, all_sprites):
        super().__init__(180)
        self.x, self.y, self.radius, self.damage = x, y, radius, damage
        self.kills = 0
        self.inside = set()   # 지난 프레임에 블랙홀 안에 있던 좀비
        size = int(radius * 2 + 10)
        self.visual = SkillVisual(pygame.Surface((size, size), pygame.SRCALPHA), (x, y))
        all_sprites.add(self.visual)

    def _count_kills(self):
        """지난 프레임에 안에 있다가 죽은 좀비 수를 셈 (어떤 공격으로 죽었든 포함, 부활한 좀비는 제외)"""
        for zombie in list(self.inside):
            if not zombie.alive() or zombie.health <= 0:
                self.kills += 1
                self.inside.discard(zombie)
                fx.burst(self.x, self.y, (200, 150, 255), 4, speed=(0.5, 2), size=(2, 3), life=(8, 14))

    def update(self, player, zombies, bullets, all_sprites, explosions):
        alive = super().update(player, zombies, bullets, all_sprites, explosions)
        if not alive:
            self._count_kills()
            self._collapse(zombies, all_sprites, explosions)
        return alive

    def _collapse(self, zombies, all_sprites, explosions):
        """블랙홀이 사라질 때: 안에서 죽은 좀비 수 × 위력의 붕괴 폭발"""
        if self.kills <= 0:
            fx.burst(self.x, self.y, (150, 90, 255), 12, speed=(1, 4), size=(2, 4), life=(10, 18))
            return
        damage = self.damage * self.KILL_BONUS * self.kills
        radius = int(self.radius * 1.2)
        boom = Explosion(self.x, self.y, radius)
        explosions.add(boom)
        all_sprites.add(boom)
        fx.ring(self.x, self.y, (180, 120, 255), radius, count=40, size=4)
        fx.add_shake(min(14, 4 + self.kills))
        fx.add_text(self.x, self.y - 40, f"붕괴! x{self.kills}", (200, 150, 255), big=True, life=70)
        for zombie in list(zombies):
            if zombie.health > 0 and math.hypot(zombie.rect.centerx - self.x, zombie.rect.centery - self.y) < radius:
                skill_damage(zombie, damage)
                push_zombie(zombie, self.x, self.y, 10)

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        self._count_kills()
        for zombie in list(zombies):
            if zombie.health <= 0:
                continue
            dx, dy = self.x - zombie.rect.centerx, self.y - zombie.rect.centery
            dist = math.hypot(dx, dy)
            if 8 < dist < self.radius:
                pull = 3.2 * max(0.35, zombie.knockback_resistance)  # 보스/거대 좀비는 덜 끌려옴
                zombie._move(dx / dist * pull, dy / dist * pull)
            if dist < self.radius and self.frames % 15 == 0:
                skill_damage(zombie, self.damage)
            if dist < self.radius:
                self.inside.add(zombie)
        if self.frames % 2 == 0:  # 빨려 들어가는 입자
            a = fx_random.uniform(0, math.pi * 2)
            r = self.radius * fx_random.uniform(0.6, 1.0)
            fx.particles.append([self.x + math.cos(a) * r, self.y + math.sin(a) * r,
                                 -math.cos(a) * r / 14, -math.sin(a) * r / 14, 14, 14, 3,
                                 fx_random.choice(((90, 255, 255), (180, 120, 255))), 0, 1.0])
        size = self.visual.image.get_width()
        c = size // 2
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(image, (60, 0, 90, 60), (c, c), int(self.radius))
        pygame.draw.circle(image, (150, 90, 255, 140), (c, c), int(self.radius), 2)
        spin = self.frames * 0.15
        for i in range(3):
            a = spin + i * math.pi * 2 / 3
            rect = (c - self.radius * 0.6, c - self.radius * 0.6, self.radius * 1.2, self.radius * 1.2)
            pygame.draw.arc(image, (120, 230, 255, 200), rect, a, a + 1.4, 4)
        core = 22 + min(18, self.kills * 2)   # 삼킨 좀비가 많을수록 중심이 커짐
        pygame.draw.circle(image, (10, 0, 20, 255), (c, c), core)
        pygame.draw.circle(image, (200, 150, 255, 255), (c, c), core, 3)
        if self.kills > 0:   # 지금까지 삼킨 수
            count = font_damage.render(str(self.kills), True, (220, 180, 255))
            image.blit(count, count.get_rect(center=(c, c)))
        self.visual.image = image


class BombardmentSkill(ActiveSkill):
    """로켓 미사일 폭격: 지정한 곳 주변에 미사일이 차례로 떨어짐"""
    def __init__(self, x, y, count, damage, radius):
        super().__init__(count * 6 + 1)
        self.x, self.y, self.damage, self.radius = x, y, damage, radius

    def tick(self, player, zombies, bullets, all_sprites, explosions):
        if self.frames % 6:
            return
        bx = self.x + random.uniform(-150, 150)
        by = self.y + random.uniform(-150, 150)
        boom = Explosion(bx, by, self.radius)
        explosions.add(boom)
        all_sprites.add(boom)
        for zombie in list(zombies):
            if zombie.health > 0 and math.hypot(zombie.rect.centerx - bx, zombie.rect.centery - by) < self.radius:
                skill_damage(zombie, self.damage)
                push_zombie(zombie, bx, by, 6)


# 우클릭 스킬 실행 함수
def execute_weapon_skill(weapon_type, player, mouse_world_x, mouse_world_y, zombies, bullets, all_sprites, explosions):
    current_time = pygame.time.get_ticks()

    # 쿨타임 체크
    if player.skill_cooldowns[weapon_type] > current_time:
        return

    # 미리 계산할 방향
    dx = mouse_world_x - player.rect.centerx
    dy = mouse_world_y - player.rect.centery
    distance = math.sqrt(dx**2 + dy**2)
    if distance > 0:
        direction_x = dx / distance
        direction_y = dy / distance
    else:
        direction_x = player.last_direction_x
        direction_y = player.last_direction_y
    aim = math.atan2(direction_y, direction_x)
    cx, cy = player.rect.center
    reset_cooldown = False  # 카타나 일섬으로 적을 처치하면 쿨타임 초기화
    base = get_weapon_damage(player)
    up = player.skill_upgrades[weapon_type]

    if weapon_type == "melee":
        # 홈런: 앞쪽 부채꼴의 좀비를 크게 날려 보냄
        radius = 190 + up["range"]
        all_sprites.add(ConeFlash(cx, cy, aim, math.radians(60), radius, (230, 170, 90)))
        hit = zombies_in_cone(zombies, cx, cy, aim, math.radians(60), radius)
        for zombie in hit:
            skill_damage(zombie, base * 3)
            push_zombie(zombie, cx, cy, 26 * get_knockback_multiplier(player))
            fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, (255, 220, 120))
        if hit:
            fx.add_text(cx, player.rect.top - 30, "홈런!", (255, 220, 120), big=True)
        fx.add_shake(4)

    elif weapon_type == "katana":
        # 일섬: 마우스 방향으로 순간 돌진하며 지나간 길의 좀비를 벰
        dash = 260 + up["strikes"] * 40
        end_x, end_y = cx + direction_x * dash, cy + direction_y * dash
        # 연속 일섬 보너스: 처치로 쿨타임이 초기화될 때마다 +25% (실패하면 원래대로)
        chain_mult = 1 + get_katana_chain_bonus(player) * player.katana_chain
        # 카타나 강화(데미지 +3)는 공격력에 더해지는 것에 더해 일섬에 1회당 +10% 더 반영
        katana_mult = 1 + KATANA_DASH_UPGRADE_BONUS * player.weapon_upgrades["katana"]["damage"]
        dash_kills = 0
        ougi_hits = 0
        first_hit = None
        for zombie in zombies_near_line(zombies, cx, cy, end_x, end_y, 45):
            # 기본 공격 업그레이드도 적용: 치명타 + 속성탄 (화염/얼음/전기)
            dash_damage = roll_crit_damage(player, base * 4 * (1 + 0.3 * up["damage"]) * katana_mult * chain_mult, zombie)
            if up.get("ougi", 0):
                # 오의 연섬: 일부를 대상 최대 체력 비례 고정 피해로 (방어 무시)
                skill_damage(zombie, dash_damage * (1 - KATANA_OUGI_RATIO))
                zombie.health -= max(dash_damage * KATANA_OUGI_RATIO, zombie.max_health * KATANA_OUGI_HP_RATIO)
                ougi_hits += 1
                size = max(zombie.rect.width, zombie.rect.height) * 0.9
                for sign in (1, -1):   # 붉은 X자 베기
                    all_sprites.add(LineFlash(zombie.rect.centerx - size, zombie.rect.centery - sign * size,
                                              zombie.rect.centerx + size, zombie.rect.centery + sign * size,
                                              (255, 70, 70), width=6, duration=14))
            else:
                skill_damage(zombie, dash_damage)
            apply_hit_elements(player, zombie, zombies, base)
            fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, (210, 230, 255))
            if first_hit is None:
                first_hit = zombie
            if zombie.health <= 0:
                reset_cooldown = True  # 처치 → 쿨타임 초기화
                zombie.dash_kill = True  # 일섬 처치는 경험치가 적음
                dash_kills += 1
        # 폭발 업그레이드: 처음 벤 좀비 위치에서 폭발 (기본 공격과 쿨타임 공유)
        if first_hit is not None and player.skills.get("skill_explosion", False) and player.explosion_cooldown <= 0:
            player.explosion_cooldown = EXPLOSION_SKILL_COOLDOWN
            boom_x, boom_y = first_hit.rect.center
            boom = Explosion(boom_x, boom_y, 80)
            explosions.add(boom)
            all_sprites.add(boom)
            for other in list(zombies):
                if other is not first_hit and math.hypot(other.rect.centerx - boom_x, other.rect.centery - boom_y) < 80:
                    other.health -= base * EXPLOSION_SKILL_RATIO_MELEE * get_damage_multiplier(other)
        all_sprites.add(LineFlash(cx, cy, end_x, end_y, (150, 200, 255), width=22, duration=16))
        if ougi_hits:
            fx.add_text((cx + end_x) / 2, (cy + end_y) / 2 - 40, "오의 · 연섬", (255, 90, 90), big=True, life=50)
        for i in range(10):  # 잔상
            t = i / 9
            fx.trail(cx + (end_x - cx) * t, cy + (end_y - cy) * t, (200, 230, 255), 5, 14)
        player.rect.center = (round(end_x), round(end_y))  # Player.update가 실수 좌표를 다시 맞춤
        fx.add_shake(3)
        player.invuln_time = KATANA_DASH_INVULN_FRAMES  # 일섬이 끝난 뒤 0.2초 무적
        if dash_kills > 0:   # 일섬으로 처치한 좀비 1마리당 체력 1 회복
            healed = min(player.max_health - player.health, dash_kills * KATANA_KILL_HEAL)
            player.health += healed
            if healed > 0:
                fx.add_text(player.rect.centerx + 30, player.rect.top - 10, f"+{healed:.0f}", (120, 255, 120))
        if reset_cooldown:
            player.katana_chain += 1
            player.katana_chain_timer = KATANA_CHAIN_WINDOW   # 1초 안에 다시 써야 스택 유지
            bonus = int(round(get_katana_chain_bonus(player) * player.katana_chain * 100))
            fx.add_text(player.rect.centerx, player.rect.top - 30, f"쿨타임 초기화! 연속 {player.katana_chain} (+{bonus}%)",
                        (150, 230, 255), big=True)
            fx.ring(player.rect.centerx, player.rect.centery, (150, 230, 255), 70 + player.katana_chain * 10, count=18)
        else:
            if player.katana_chain > 0:
                fx.add_text(player.rect.centerx, player.rect.top - 30, "연속 끊김", (160, 160, 180))
            player.katana_chain = 0
            player.katana_chain_timer = 0

    elif weapon_type == "axe":
        # 대회전 베기: 도끼를 크게 한 바퀴 휘둘러 지나가는 좀비를 모두 베고 흡혈
        radius = AXE_SKILL_RADIUS + up["range"]
        knockback = AXE_SKILL_KNOCKBACK * (1 + 0.12 * up["knockback"]) * get_knockback_multiplier(player)
        player.active_skills.append(GreatSwingSkill(player, all_sprites, base * AXE_SKILL_DAMAGE_MULT, radius, knockback, aim))

    elif weapon_type == "spear":
        # 물보라: 주변으로 물결을 일으켜 좀비를 튕겨 내고 느리게 함
        radius = SPLASH_RADIUS + up["pierces"] * 30
        slow = max(0.15, SPLASH_SLOW - up["speed"])
        player.active_skills.append(WaterSplashSkill(player, all_sprites, base * SPLASH_DAMAGE_MULT, radius, slow))

    elif weapon_type == "hammer":
        # 대지 강타: 마우스 위치(최대 300px)를 내려쳐 주변 좀비 피해 + 1.5초 기절
        reach = min(distance, 300)
        tx, ty = cx + direction_x * reach, cy + direction_y * reach
        radius = 160 + up["range"]
        all_sprites.add(MeleePoundEffect(tx, ty, radius))
        boom = Explosion(tx, ty, radius)
        explosions.add(boom)
        all_sprites.add(boom)
        for zombie in list(zombies):
            if zombie.health > 0 and math.hypot(zombie.rect.centerx - tx, zombie.rect.centery - ty) < radius:
                skill_damage(zombie, base * 3 * (1 + 0.10 * up["damage"]))
                zombie.slow_time = max(zombie.slow_time, 90)
                zombie.slow_multiplier = 0.0  # 기절 (돌좀비는 면역)
        fx.add_text(tx, ty - radius * 0.5, "기절!", (230, 230, 230), big=True)
        fx.add_shake(8)

    elif weapon_type == "gloves":
        # 러시: 잠시 동안 공격 속도 3배
        player.rush_time = 180 + up["strikes"] * 30
        fx.ring(cx, cy, (255, 160, 200), 90, count=20)
        fx.add_text(cx, player.rect.top - 30, "러시!", (255, 160, 200), big=True)

    elif weapon_type == "glock":
        # 항공 폭격: 비행기가 날아와 조준 방향 직선으로 폭탄을 줄줄이 떨어뜨림
        length = GLOCK_STRIKE_LENGTH + up["burst"] * GLOCK_STRIKE_RANGE_LENGTH
        blast = AirStrikeSkill.BLAST_RADIUS + up["burst"] * GLOCK_STRIKE_RANGE_WIDTH
        bomb_damage = GLOCK_STRIKE_BASE_DAMAGE * base / WEAPON_STATS["glock"]["dmg"]
        player.active_skills.append(AirStrikeSkill(player, all_sprites, bomb_damage, direction_x, direction_y, length, blast))

    elif weapon_type == "machinegun":
        # 포탑 설치: 그 자리에서 자동 사격하는 포탑
        duration = 360 + up["burst"] * 30
        player.active_skills.append(TurretSkill(cx, cy, duration, base * 1.2, all_sprites))

    elif weapon_type == "shotgun":
        # 용의 숨결: 앞쪽 부채꼴로 화염 방사 + 불붙임
        radius = 260 + up["range"]
        half = math.radians(35)
        all_sprites.add(ConeFlash(cx, cy, aim, half, radius, (255, 120, 20), duration=20))
        fx.burst(cx + direction_x * 20, cy + direction_y * 20, (255, 140, 30), 40, speed=(4, 12), size=(3, 6),
                 life=(12, 22), drag=0.9, angle=aim, spread=half * 2)
        fx.burst(cx + direction_x * 20, cy + direction_y * 20, (255, 220, 80), 20, speed=(3, 9), size=(2, 4),
                 life=(10, 18), drag=0.9, angle=aim, spread=half * 2)
        for zombie in zombies_in_cone(zombies, cx, cy, aim, half, radius):
            skill_damage(zombie, base * 4 * (1 + 0.08 * up["damage"]))
            zombie.burn_time = max(zombie.burn_time, 240)
            zombie.burn_damage_cooldown = 0
        fx.add_shake(3)

    elif weapon_type == "sniper":
        # 도탄 사격: 한 발이 맞은 좀비에서 주변 좀비로 10번 튕김 ("도탄 +3회" 업그레이드로 증가)
        bounces = SNIPER_RICOCHET_BOUNCES + up["pierces"] * SNIPER_RICOCHET_UPGRADE
        player.active_skills.append(RicochetSkill(cx, cy, direction_x, direction_y, base * SNIPER_RICOCHET_DAMAGE_MULT,
                                                  bounces, zombies, all_sprites))
        fire_muzzle_flash(player, mouse_world_x, mouse_world_y, kick=3.0)

    elif weapon_type == "plasma":
        # 블랙홀: 마우스 위치에 3초 동안 좀비를 끌어당기며 피해
        radius = 220 + up["range"]
        player.active_skills.append(BlackHoleSkill(mouse_world_x, mouse_world_y, radius,
                                                   base * 0.8 * (1 + 0.08 * up["damage"]), all_sprites))

    elif weapon_type == "rocket":
        # 미사일 폭격: 마우스 주변에 미사일 8발이 차례로 떨어짐
        radius = 90 + up["explosion"] // 2
        player.active_skills.append(BombardmentSkill(mouse_world_x, mouse_world_y, 8,
                                                     base * 1.2 * (1 + 0.05 * up["damage"]), radius))

    player.skill_cooldowns[weapon_type] = current_time + int(SKILL_COOLDOWNS[weapon_type] * (1 - player.skill_cooldown_reduction))
    if reset_cooldown:
        player.skill_cooldowns[weapon_type] = current_time  # 바로 다시 사용 가능


# 무기 클래스
class Weapon:
    def __init__(self, weapon_type):
        self.weapon_type = weapon_type
        self.last_shot_time = 0

        # 무기별 초기 설정은 WEAPON_STATS 기준표에서 가져옴
        stats = WEAPON_STATS[weapon_type]
        self.name = stats["name"]
        self.color = stats["color"]
        self.damage = stats["dmg"]
        self.fire_rate = stats["rate"]          # 초당 공격 횟수
        self.attack_speed = 1.0                 # 공격 속도 배율 (근접 공격 속도 업그레이드로 증가)
        self.bullet_speed = stats.get("speed", 0)
        self.pierce = stats.get("pierce", 0)                # 기본 공격 관통 수
        self.max_range = stats.get("max_range", 3000)       # 총알 최대 사거리(px)
        self.splash_radius = stats.get("splash_radius", 0)  # 착탄 폭발 반경 (0이면 없음)
        self.splash_ratio = stats.get("splash_ratio", 0)    # 폭발이 주변 좀비에게 주는 피해 비율

    def get_attack_interval(self):
        """공격 간격(ms) - 글로브 러시 중에는 3배 빠름"""
        return 1000.0 / (self.fire_rate * self.attack_speed * getattr(self, "rush_mult", 1.0))

    def can_fire(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.get_attack_interval()

    def fire(self):
        if self.can_fire():
            self.last_shot_time = pygame.time.get_ticks()
            return True
        return False


# 참격 이펙트
class SlashEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, damage=100):
        super().__init__()
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.damage = damage
        self.created_time = pygame.time.get_ticks()
        self.duration = 200  # 200ms 동안 표시
        self.angle = math.degrees(math.atan2(-direction_y, direction_x))

        self.attack_range = 220

        # 참격 이펙트: 실제 피해 범위(반경 attack_range 원)를 옅게 + 앞쪽으로 휘어진 큰 초승달 칼날
        # (이미지는 오른쪽을 향하게 그리고 조준 각도로 회전)
        r = self.attack_range
        size = r * 2 + 10
        c = size // 2
        self.base_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.base_image, (150, 200, 255, 45), (c, c), r)
        pygame.draw.circle(self.base_image, (190, 225, 255, 120), (c, c), r, 2)
        for width, color, shrink in ((14, (120, 190, 255, 200), 0), (7, (230, 245, 255, 255), 6)):
            pygame.draw.arc(self.base_image, color, (c - r + shrink, c - r + shrink, (r - shrink) * 2, (r - shrink) * 2),
                            math.radians(-70), math.radians(70), width)

        # pygame 회전은 반시계 방향이 + (예전에는 -각도로 돌려서 위아래가 뒤집혀 보였음)
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.knockback_power = 1200
        self.hit_zombies = set()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.created_time

        # 지정된 시간이 지나면 제거
        if elapsed >= self.duration:
            self.kill()
            return

        # 투명도 계산 (0 ~ 255)
        alpha = int(255 * (1 - elapsed / self.duration))

        # 회전된 이미지에 투명도 적용
        rotated_image = pygame.transform.rotate(self.base_image, self.angle)
        rotated_image.set_alpha(alpha)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_rect(self):
        return self.rect


# ===== 좀비 특수 공격 이펙트 =====

# 가시좀비 가시 투사체
class SpikeProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage=2.0):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = 8

        # 방향 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0

        # 가시 모양 생성 (더 예쁜 디자인)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        # 외부 붉은 마름모
        pygame.draw.polygon(self.image, (220, 40, 40), [(8, 0), (15, 8), (8, 16), (1, 8)])
        # 내부 밝은 붉은색
        pygame.draw.polygon(self.image, (255, 100, 100), [(8, 2), (13, 8), (8, 14), (3, 8)])
        # 중앙 밝은 점
        pygame.draw.circle(self.image, (255, 200, 200), (8, 8), 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.created_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3초 후 사라짐

    def update(self):
        # 실수 좌표로 이동 (rect 정수 반올림으로 궤적이 틀어지는 문제 방지)
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (round(self.x), round(self.y))

        # 시간 만료 체크
        if pygame.time.get_ticks() - self.created_time > self.lifetime:
            self.kill()


# 독좀비 독 장판
_pool_images = {}
POOL_FADE_STEPS = 16


def _poison_pool_image(radius, level):
    """독 장판 이미지 (원래 디자인 그대로) - 사라지는 투명도를 16단계로 미리 구워 둔 것을 같이 씀
    (예전: 장판마다 매 프레임 이미지 복사 + 전체 투명도 적용 → 독 좀비가 많아 장판이 100개 넘게 겹치면 프레임이 크게 떨어졌음)"""
    key = (radius, level)
    image = _pool_images.get(key)
    if image is None:
        base = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(base, (50, 180, 50, 120), (radius, radius), radius)                 # 외부 진한 초록
        pygame.draw.circle(base, (100, 230, 100, 160), (radius, radius), max(1, radius - 15))  # 중간 밝은 초록
        pygame.draw.circle(base, (150, 255, 150, 200), (radius, radius), max(1, radius - 30))  # 내부 가장 밝은 초록
        for i in range(8):                                                                       # 독액 방울
            angle = i * math.pi / 4
            px = int(radius + math.cos(angle) * (radius - 20))
            py = int(radius + math.sin(angle) * (radius - 20))
            pygame.draw.circle(base, (100, 250, 100, 150), (px, py), 5)
        fade = int(150 * level / (POOL_FADE_STEPS - 1))       # 원래 set_alpha(150 × 남은 비율)과 같은 효과
        base.fill((255, 255, 255, fade), special_flags=pygame.BLEND_RGBA_MULT)
        image = _pool_images[key] = base.convert_alpha()
    return image


class PoisonPool(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=80, duration=5000):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.damage_per_tick = 0.3
        self.damage_cooldown = 30  # 0.5초마다 데미지
        self.created_time = pygame.time.get_ticks()
        self.duration = duration  # 5초

        # 독 장판 시각화 - 같은 크기는 한 장을 같이 씀
        # (픽셀마다 투명도가 다른 큰 이미지는 그리기가 매우 느려서, 단색 + 전체 투명도 방식으로 바꿈.
        #  독 좀비가 많으면 장판이 100개 넘게 겹쳐 프레임이 크게 떨어졌음)
        self.radius_px = radius
        self.base_image = _poison_pool_image(radius, POOL_FADE_STEPS - 1)

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # 시간 경과에 따른 투명도 감소
        elapsed = pygame.time.get_ticks() - self.created_time
        remaining = max(0, self.duration - elapsed)
        progress = 1 - (remaining / self.duration)  # 0 ~ 1

        # 투명도 적용 (서서히 사라짐)
        level = max(0, min(POOL_FADE_STEPS - 1, round((1 - progress) * (POOL_FADE_STEPS - 1))))
        self.image = _poison_pool_image(self.radius_px, level)   # 미리 만든 이미지를 같이 씀 (복사 없음)

        if elapsed > self.duration:
            self.kill()


# 얼음좀비 얼음 투사체 (속도 저하)
class IceProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage=0.5):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = 8

        # 방향 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0

        # 얼음 덩어리 생성 (더 예쁜 디자인)
        self.image = pygame.Surface((18, 18), pygame.SRCALPHA)
        # 외부 밝은 파랑
        pygame.draw.polygon(self.image, (100, 200, 255), [(9, 1), (16, 5), (16, 13), (9, 17), (2, 13), (2, 5)])
        # 내부 더 밝은 파랑
        pygame.draw.polygon(self.image, (180, 230, 255), [(9, 3), (14, 6), (14, 12), (9, 15), (4, 12), (4, 6)])
        # 중앙 강한 빛
        pygame.draw.circle(self.image, (200, 240, 255), (9, 9), 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.created_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3초 후 사라짐
        self.slow_effect = 0.1  # 속도 90% 감소 (10%만 이동)

    def update(self):
        # 실수 좌표로 이동 (rect 정수 반올림으로 궤적이 틀어지는 문제 방지)
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (round(self.x), round(self.y))

        # 시간 만료 체크
        if pygame.time.get_ticks() - self.created_time > self.lifetime:
            self.kill()


# 무거운좀비 돌진 이펙트
class ChargeEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, radius=40):
        super().__init__()
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.radius = radius
        self.created_time = pygame.time.get_ticks()
        self.duration = 200  # 200ms

        # 돌진 이펙트 (강력한 에너지 오라)
        self.base_image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # 외부 주황
        pygame.draw.circle(self.base_image, (255, 165, 0, 120), (radius, radius), radius)
        # 중간 밝은 노랑
        pygame.draw.circle(self.base_image, (255, 220, 100, 180), (radius, radius), radius - 10)
        # 내부 매우 밝은 노랑
        pygame.draw.circle(self.base_image, (255, 255, 150, 220), (radius, radius), radius - 20)
        # 외부 광선
        for i in range(8):
            angle = i * math.pi / 4
            x1 = int(radius + math.cos(angle) * (radius - 5))
            y1 = int(radius + math.sin(angle) * (radius - 5))
            x2 = int(radius + math.cos(angle) * (radius + 10))
            y2 = int(radius + math.sin(angle) * (radius + 10))
            pygame.draw.line(self.base_image, (255, 200, 0, 150), (x1, y1), (x2, y2), 2)

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time

        if elapsed >= self.duration:
            self.kill()
            return

        # 투명도 감소
        alpha = int(200 * (1 - elapsed / self.duration))
        self.image = self.base_image.copy()
        self.image.set_alpha(alpha)


# 닌자 투사체
class NinjaProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage=1.5):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = 10

        # 방향 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0

        # 검은 별 모양 투사체 (더 예쁜 디자인)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        # 외부 검정 별
        pygame.draw.polygon(self.image, (20, 20, 20), [(8, 0), (10, 5), (16, 7), (11, 10), (12, 16), (8, 13), (4, 16), (5, 10), (0, 7), (6, 5)])
        # 내부 어두운 회색
        pygame.draw.polygon(self.image, (80, 80, 120), [(8, 2), (10, 6), (14, 8), (10, 10), (11, 15), (8, 12), (5, 15), (6, 10), (2, 8), (6, 6)])
        # 중앙 빛
        pygame.draw.circle(self.image, (150, 150, 200), (8, 8), 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.created_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3초 후 사라짐

    def update(self):
        # 실수 좌표로 이동 (rect 정수 반올림으로 궤적이 틀어지는 문제 방지)
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (round(self.x), round(self.y))

        # 시간 만료 체크
        if pygame.time.get_ticks() - self.created_time > self.lifetime:
            self.kill()


# 바람 좀비 죽음 이펙트 (약한 광역 + 밀치기)
class WindBlastEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=200, damage=0.5, knockback=15):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.knockback = knockback
        self.created_time = pygame.time.get_ticks()
        self.duration = 300  # 300ms

        # 바람 이펙트 시각화 (청백색 회오리)
        self.base_image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # 외부 회오리
        for i in range(1, 4):
            pygame.draw.circle(self.base_image, (150, 220, 255, 80 - i*20), (radius, radius), int(radius * i / 3), 2)
        # 중심 밝은 파랑
        pygame.draw.circle(self.base_image, (200, 240, 255, 150), (radius, radius), 20)
        # 회오리 선 효과
        for i in range(0, 360, 45):
            rad = math.radians(i)
            x1 = int(radius + math.cos(rad) * 30)
            y1 = int(radius + math.sin(rad) * 30)
            x2 = int(radius + math.cos(rad) * 60)
            y2 = int(radius + math.sin(rad) * 60)
            pygame.draw.line(self.base_image, (180, 230, 255, 120), (x1, y1), (x2, y2), 2)

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time

        if elapsed >= self.duration:
            self.kill()
            return

        # 투명도 감소
        alpha = int(100 * (1 - elapsed / self.duration))
        self.image = self.base_image.copy()
        self.image.set_alpha(alpha)


# 불꽃 좀비 죽음 이펙트 (강한 광역 대미지)
class FlameExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=180, damage=2.0):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.created_time = pygame.time.get_ticks()
        self.duration = 500  # 500ms

        # 불꽃 폭발 이펙트 (강렬한 주황-노랑)
        self.base_image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # 외부 진주황
        pygame.draw.circle(self.base_image, (255, 100, 0, 150), (radius, radius), radius)
        # 중간 주황
        pygame.draw.circle(self.base_image, (255, 160, 50, 180), (radius, radius), radius - 20)
        # 내부 밝은 노랑
        pygame.draw.circle(self.base_image, (255, 220, 100, 220), (radius, radius), radius - 40)
        # 중심 흰색
        pygame.draw.circle(self.base_image, (255, 255, 200, 255), (radius, radius), radius - 60)

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time

        if elapsed >= self.duration:
            self.kill()
            return

        # 투명도 감소
        alpha = int(200 * (1 - elapsed / self.duration))
        self.image = self.base_image.copy()
        self.image.set_alpha(alpha)


# 신의 신성한 폭발 이펙트 (매우 강함)
class HolyExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=250, damage=5.0):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.created_time = pygame.time.get_ticks()
        self.duration = 800  # 800ms

        # 신성한 빛 이펙트 (흰색, 노랑, 금색)
        self.base_image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # 가장 바깥 검은색 림
        pygame.draw.circle(self.base_image, (0, 0, 0, 50), (radius, radius), radius)

        # 첫 번째 층 - 노란 빛
        pygame.draw.circle(self.base_image, (255, 255, 0, 180), (radius, radius), radius - 10)

        # 두 번째 층 - 밝은 흰색
        pygame.draw.circle(self.base_image, (255, 255, 255, 220), (radius, radius), radius - 50)

        # 세 번째 층 - 금색
        pygame.draw.circle(self.base_image, (255, 215, 0, 200), (radius, radius), radius - 80)

        # 중심 극도로 밝은 흰색
        pygame.draw.circle(self.base_image, (255, 255, 220, 255), (radius, radius), radius - 120)

        # 신성한 빛살
        for i in range(0, 360, 30):
            rad = math.radians(i)
            x1 = int(radius + math.cos(rad) * (radius - 30))
            y1 = int(radius + math.sin(rad) * (radius - 30))
            x2 = int(radius + math.cos(rad) * (radius + 20))
            y2 = int(radius + math.sin(rad) * (radius + 20))
            pygame.draw.line(self.base_image, (255, 255, 100, 200), (x1, y1), (x2, y2), 3)

        # 외부 장식 원들
        for i in range(1, 4):
            pygame.draw.circle(self.base_image, (255, 215, 0, 100), (radius, radius), int(radius * 0.8 * i / 3), 2)

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time

        if elapsed >= self.duration:
            self.kill()
            return

        # 깜빡이는 효과 (신성한 느낌)
        flicker = abs(math.sin(elapsed / 100)) * 50
        alpha = int(250 * (1 - elapsed / self.duration) + flicker)
        alpha = min(255, max(0, alpha))
        self.image = self.base_image.copy()
        self.image.set_alpha(alpha)


# 리바이어던 쓰나미 이펙트 (가로/세로 공격)
class TsunamiEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="horizontal", range_dist=400, damage=15.0):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction  # "horizontal" 또는 "vertical"
        self.range_dist = range_dist
        self.damage = damage
        self.has_hit_player = False  # 쓰나미 1회당 플레이어에게 한 번만 피해
        self.created_time = pygame.time.get_ticks()
        self.duration = 1200  # 1.2초 지속

        # 쓰나미 이미지 생성 (파란색 물결)
        if direction == "horizontal":
            # 가로 쓰나미 (좌우로 퍼지는 물결)
            self.image = pygame.Surface((range_dist * 2, 100), pygame.SRCALPHA)
            center_x = range_dist
            center_y = 50

            # 물결 모양 그리기
            for i in range(0, int(range_dist * 2), 30):
                pygame.draw.circle(self.image, (0, 150, 255, 150), (i, center_y), 40)
                pygame.draw.circle(self.image, (0, 200, 255, 100), (i, center_y), 30)
            pygame.draw.line(self.image, (100, 200, 255, 200), (0, center_y), (range_dist * 2, center_y), 8)

        else:  # vertical
            # 세로 쓰나미 (상하로 퍼지는 물결)
            self.image = pygame.Surface((100, range_dist * 2), pygame.SRCALPHA)
            center_x = 50
            center_y = range_dist

            # 물결 모양 그리기
            for i in range(0, int(range_dist * 2), 30):
                pygame.draw.circle(self.image, (0, 150, 255, 150), (center_x, i), 40)
                pygame.draw.circle(self.image, (0, 200, 255, 100), (center_x, i), 30)
            pygame.draw.line(self.image, (100, 200, 255, 200), (center_x, 0), (center_x, range_dist * 2), 8)

        self.rect = self.image.get_rect()
        if direction == "horizontal":
            self.rect.center = (x, y)
        else:
            self.rect.center = (x, y)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time

        if elapsed >= self.duration:
            self.kill()
            return

        # 투명도 감소
        progress = elapsed / self.duration
        alpha = int(200 * (1 - progress * 0.8))

        # 투명도 적용
        self.image.set_alpha(alpha)


# 나무 방망이 스킬 공격 이펙트 (원형 파동)
class MeleePoundEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=200):
        super().__init__()
        self.x = x
        self.y = y
        self.max_radius = radius
        self.duration = 400  # 400ms
        self.created_time = pygame.time.get_ticks()

        self.image = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time
        progress = elapsed / self.duration

        if progress >= 1.0:
            self.kill()
            return

        # 현재 반경 계산
        current_radius = self.max_radius * progress
        alpha = int(255 * (1 - progress))  # 페이드 아웃

        # 새로운 이미지 생성
        size = int(self.max_radius * 2 + 20)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        # 주황색으로 원형 파동 그리기
        center = size // 2
        # 바깥쪽 원 (밝은 주황)
        pygame.draw.circle(self.image, (255, 165, 0, alpha), (center, center), int(current_radius), 3)
        # 안쪽 원 (어두운 주황)
        pygame.draw.circle(self.image, (255, 100, 0, alpha // 2), (center, center), int(current_radius * 0.7), 2)
        # 중심 점 (밝음)
        pygame.draw.circle(self.image, (255, 200, 100, alpha), (center, center), 5)

        # 방사형 선 (힘의 파동 느낌)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = center + math.cos(rad) * current_radius * 0.5
            y1 = center + math.sin(rad) * current_radius * 0.5
            x2 = center + math.cos(rad) * current_radius
            y2 = center + math.sin(rad) * current_radius
            pygame.draw.line(self.image, (255, 150, 0, alpha), (x1, y1), (x2, y2), 2)

        self.rect = self.image.get_rect(center=(self.x, self.y))


_resurrection_frames = {}


# 부활 이펙트 (기사/방패/갑옷/철/기사단장 좀비가 부활할 때)
class ResurrectionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(100, 150, 200)):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.duration = 500  # 500ms
        self.created_time = pygame.time.get_ticks()
        self.max_radius = 150

        self.image = pygame.Surface((300, 300), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time
        progress = elapsed / self.duration

        if progress >= 1.0:
            self.kill()
            return

        # 30단계로 나눠 한 번만 그려 두고 같이 씀 (예전에는 300x300 이미지를 매 프레임 새로 그렸음)
        step = int(progress * 30)
        key = (tuple(self.color), step)
        image = _resurrection_frames.get(key)
        if image is None:
            progress = step / 30
            # 현재 반경 계산
            current_radius = self.max_radius * progress
            alpha = int(255 * (1 - progress))  # 페이드 아웃

            size = 300
            image = pygame.Surface((size, size), pygame.SRCALPHA)
            center = size // 2

            # 밝은 파란 빛 방사형 효과
            r, g, b = self.color
            # 색상값이 255를 넘으면 pygame이 "invalid color argument"로 크래시하므로 범위 제한
            light = lambda value, add: min(255, value + add)

            # 동심원 (여러 원 겹치기)
            pygame.draw.circle(image, (r, g, b, alpha), (center, center), int(current_radius), 4)
            pygame.draw.circle(image, (light(r, 50), light(g, 50), light(b, 50), alpha//2), (center, center), int(current_radius * 0.7), 2)
            pygame.draw.circle(image, (255, 255, 255, alpha), (center, center), int(current_radius * 0.4), 2)

            # 중심 빛
            pygame.draw.circle(image, (255, 255, 255, alpha), (center, center), 8)

            # 방사형 빛줄기 (8개)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = center
                y1 = center
                x2 = center + math.cos(rad) * current_radius
                y2 = center + math.sin(rad) * current_radius
                pygame.draw.line(image, (light(r, 100), light(g, 100), light(b, 100), alpha), (x1, y1), (x2, y2), 3)
            _resurrection_frames[key] = image
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))


# 소환 이펙트 (임프, 기사, 천사 등의 소환 시각 효과)
class SpawnEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(200, 50, 100), duration_ms=300):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration_ms  # ms
        self.created_time = pygame.time.get_ticks()
        self.max_radius = 60

        self.image = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        elapsed = pygame.time.get_ticks() - self.created_time
        progress = elapsed / self.duration

        if progress >= 1.0:
            self.kill()
            return

        # 현재 반경 계산
        current_radius = self.max_radius * progress
        alpha = int(255 * (1 - progress * 0.8))  # 약간 더 천천히 페이드 아웃

        size = 200
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        r, g, b = self.color

        # 중심에서 바깥쪽으로 확산하는 효과
        # 밝은 색 원
        pygame.draw.circle(self.image, (r, g, b, alpha), (center, center), int(current_radius), 4)
        pygame.draw.circle(self.image, (min(r+100, 255), min(g+100, 255), min(b+100, 255), alpha//2),
                          (center, center), int(current_radius * 0.6), 2)

        # 중심 밝은 점
        pygame.draw.circle(self.image, (255, 255, 255, alpha), (center, center), max(int(current_radius * 0.2), 3))

        # 나선형 파티클 (8개)
        for i in range(8):
            angle = (i * 45) + (progress * 120)  # 회전하는 효과
            rad = math.radians(angle)
            particle_x = int(center + math.cos(rad) * current_radius)
            particle_y = int(center + math.sin(rad) * current_radius)
            pygame.draw.circle(self.image, (min(r+50, 255), min(g+50, 255), min(b+50, 255), alpha), (particle_x, particle_y), 3)

        self.rect = self.image.get_rect(center=(self.x, self.y))





# 근접 무기 (나무 방망이)
class Melee(pygame.sprite.Sprite):
    # 무기별 휘두르기 방식: swing(빠르게 휘두르고 감속) / heavy(천천히 들었다 내려찍기) / thrust(앞으로 찌르기)
    SWING_STYLES = {"melee": "swing", "katana": "swing", "axe": "heavy", "hammer": "heavy", "spear": "thrust", "gloves": "thrust"}
    TRAIL_COLORS = {"melee": (230, 170, 90), "katana": (200, 225, 255), "axe": (255, 110, 110),
                    "hammer": (230, 230, 230), "spear": (120, 200, 255), "gloves": (255, 160, 200)}
    # 공격이 맞는 부채꼴의 반각(도): 조준 방향 ± 이 각도, 반경 attack_range (그려지는 범위와 동일)
    HIT_HALF_ARCS = {"melee": 80, "katana": 90, "axe": 70, "hammer": 75, "spear": 30, "gloves": 45}
    # 이 거리 안에 붙은 좀비는 방향과 상관없이 맞음 (몸에 붙은 좀비를 못 때리는 일 방지)
    CLOSE_HIT_RADIUS = 45

    def __init__(self, x, y, direction_x, direction_y, damage=40, weapon_type="melee", owner=None):
        super().__init__()
        self.owner = owner  # 휘두르는 동안 플레이어를 따라감
        self.weapon_type = weapon_type
        self.damage = damage
        self.knockback_power = 800  # 넉백 힘
        self.created_time = pygame.time.get_ticks()
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.base_angle = math.degrees(math.atan2(-direction_y, direction_x))
        self.player_x = x  # 플레이어 위치 저장
        self.player_y = y

        # 무기별 공격 형태 및 원본 이미지 저장
        if weapon_type == "melee":
            # 나무 방망이 - 개선된 디자인
            self.base_image = pygame.Surface((100, 25), pygame.SRCALPHA)
            # 나무 타일 패턴
            pygame.draw.rect(self.base_image, (139, 69, 19), (0, 8, 100, 10))
            pygame.draw.rect(self.base_image, (100, 50, 10), (10, 8, 3, 10))
            pygame.draw.rect(self.base_image, (100, 50, 10), (25, 8, 3, 10))
            pygame.draw.rect(self.base_image, (100, 50, 10), (40, 8, 3, 10))
            pygame.draw.rect(self.base_image, (100, 50, 10), (55, 8, 3, 10))
            pygame.draw.rect(self.base_image, (100, 50, 10), (70, 8, 3, 10))
            pygame.draw.rect(self.base_image, (100, 50, 10), (85, 8, 3, 10))
            # 손잡이 (검은색)
            pygame.draw.rect(self.base_image, (0, 0, 0), (0, 10, 12, 6))
            self.duration = 25
            self.knockback_power = 1000
            self.swing_angle = 140  # 더 큰 스윙
            self.attack_range = 110  # 공격 범위
        elif weapon_type == "katana":
            # 카타나 - 우아한 칼 모양
            self.base_image = pygame.Surface((150, 25), pygame.SRCALPHA)
            pygame.draw.polygon(self.base_image, (200, 200, 220), [(0, 12), (130, 8), (150, 12), (130, 16), (0, 12)])
            pygame.draw.line(self.base_image, (100, 100, 100), (0, 12), (130, 10), 2)
            pygame.draw.rect(self.base_image, (139, 69, 19), (0, 10, 15, 4))
            self.duration = 20
            self.knockback_power = 850
            self.swing_angle = 150
            self.attack_range = 120  # 더 긴 범위
        elif weapon_type == "axe":
            # 도끼 - 나무 손잡이 + 넓은 날
            self.base_image = pygame.Surface((110, 64), pygame.SRCALPHA)
            pygame.draw.rect(self.base_image, (110, 70, 35), (0, 28, 92, 9), border_radius=3)       # 손잡이
            pygame.draw.polygon(self.base_image, (150, 150, 165), [(72, 8), (108, 0), (110, 64), (72, 56), (80, 32)])  # 날
            pygame.draw.line(self.base_image, (235, 235, 245), (108, 2), (109, 62), 3)              # 날 끝 반짝임
            pygame.draw.polygon(self.base_image, (139, 35, 69), [(70, 22), (82, 22), (82, 42), (70, 42)])  # 고정 띠
            self.duration = 30
            self.knockback_power = 1500
            self.swing_angle = 100
            self.attack_range = 125
        elif weapon_type == "spear":
            # 창 - 짙은 푸른 자루 + 잎 모양 강철 날 (물보라 창)
            self.base_image = draw_spear_art(160, 6).copy()
            self.duration = 28
            self.knockback_power = 600
            self.swing_angle = 80
            self.attack_range = 165  # 가장 긴 범위
        elif weapon_type == "hammer":
            # 해머 - 긴 손잡이 + 묵직한 쇠머리
            self.base_image = pygame.Surface((112, 70), pygame.SRCALPHA)
            pygame.draw.rect(self.base_image, (90, 60, 35), (0, 30, 84, 10), border_radius=3)       # 손잡이
            pygame.draw.rect(self.base_image, (175, 175, 185), (76, 4, 36, 62), border_radius=5)    # 머리
            pygame.draw.rect(self.base_image, (120, 120, 130), (76, 4, 36, 62), 3, border_radius=5)
            pygame.draw.rect(self.base_image, (225, 225, 235), (82, 10, 6, 50), border_radius=2)    # 하이라이트
            self.duration = 28
            self.knockback_power = 1800  # 가장 강한 넉백
            self.swing_angle = 110
            self.attack_range = 155
        elif weapon_type == "gloves":
            # 글로브 - 주먹 (손목 띠 + 둥근 장갑)
            self.base_image = pygame.Surface((54, 44), pygame.SRCALPHA)
            pygame.draw.rect(self.base_image, (200, 60, 110), (0, 12, 18, 20), border_radius=4)      # 손목
            pygame.draw.circle(self.base_image, (255, 120, 170), (34, 22), 20)                       # 주먹
            pygame.draw.circle(self.base_image, (190, 50, 100), (34, 22), 20, 3)
            pygame.draw.arc(self.base_image, (255, 210, 225), (22, 8, 22, 16), 0.3, 2.6, 3)          # 반짝임
            self.duration = 15
            self.knockback_power = 700
            self.swing_angle = 90
            self.attack_range = 100  # 근접 중 짧은 편
        else:
            # 기본값
            self.base_image = pygame.Surface((80, 20))
            self.base_image.fill((139, 69, 19))
            self.duration = 30
            self.swing_angle = 120
            self.attack_range = 100

        # 무기별 공격 거리 설정 (플레이어 앞쪽 오프셋)
        attack_offset = {
            "melee": 60,
            "katana": 75,
            "axe": 70,
            "spear": 95,
            "hammer": 70,
            "gloves": 45
        }
        self.offset_distance = attack_offset.get(weapon_type, 60)

        # 회전해도 네모난 모서리가 생기지 않게 투명 배경으로
        self.base_image = self.base_image.convert_alpha()
        self.style = self.SWING_STYLES.get(weapon_type, "swing")
        self.trail_color = self.TRAIL_COLORS.get(weapon_type, (230, 230, 230))
        self.weapon_length = max(self.base_image.get_size())
        self.hit_half_arc = self.HIT_HALF_ARCS.get(weapon_type, 70)
        # 무기 끝이 정확히 공격 범위(attack_range)에 닿도록 위치/휘두르는 각도를 맞춤
        if self.style == "thrust":
            self.offset_distance = max(20, (self.attack_range - self.weapon_length / 2) / 1.35)
        else:
            self.offset_distance = max(20, self.attack_range - self.weapon_length / 2)
            self.swing_angle = self.hit_half_arc * 2
        self.canvas_half = int(self.attack_range + 16)
        self.impact_done = False

        self.has_hit = set()  # 이미 공격한 좀비들을 추적
        self._render(0.0)

    def _render(self, progress):
        """플레이어를 중심으로 한 캔버스에 무기 + 휘두른 궤적(잔상)을 그림 (그리기 전용)"""
        if self.owner is not None:
            self.player_x, self.player_y = self.owner.rect.center
        if self.style == "thrust":
            # 찌르기: 앞으로 쭉 뻗었다가 돌아옴
            extend = math.sin(min(1.0, progress) * math.pi)
            angle = self.base_angle
            reach = self.offset_distance * (0.55 + 0.8 * extend)
            start_angle = angle
        else:
            if self.style == "heavy":
                eased = progress ** 2.2              # 천천히 들었다가 빠르게 내려침
            else:
                eased = 1 - (1 - progress) ** 3      # 빠르게 휘두르고 끝에서 감속
            start_angle = self.base_angle + self.swing_angle / 2
            angle = start_angle - self.swing_angle * eased
            reach = self.offset_distance
        half = self.canvas_half
        canvas = pygame.Surface((half * 2, half * 2), pygame.SRCALPHA)
        # 실제로 맞는 범위(부채꼴)를 옅게 표시
        area_alpha = int(45 * (1 - progress))
        if area_alpha > 0:
            r, g, b = self.trail_color
            points = [(half, half)]
            steps = max(2, int(self.hit_half_arc * 2 / 8))
            for i in range(steps + 1):
                a = math.radians(self.base_angle - self.hit_half_arc + self.hit_half_arc * 2 * i / steps)
                points.append((half + math.cos(a) * self.attack_range, half - math.sin(a) * self.attack_range))
            pygame.draw.polygon(canvas, (r, g, b, area_alpha), points)
            pygame.draw.circle(canvas, (r, g, b, area_alpha), (half, half), self.CLOSE_HIT_RADIUS)
        fade = int(130 * (1 - progress))
        if fade > 0:
            r, g, b = self.trail_color
            if self.style == "thrust":
                rad = math.radians(angle)
                tip = reach + self.weapon_length * 0.5
                p1 = (half + math.cos(rad) * reach * 0.3, half - math.sin(rad) * reach * 0.3)
                p2 = (half + math.cos(rad) * tip, half - math.sin(rad) * tip)
                pygame.draw.line(canvas, (r, g, b, fade), p1, p2, 10)
            else:
                # 시작 각도부터 현재 각도까지 부채꼴 잔상
                outer = reach + self.weapon_length * 0.5
                inner = max(12, reach - self.weapon_length * 0.25)
                steps = max(2, int(abs(start_angle - angle) / 6) + 1)
                arc_out, arc_in = [], []
                for i in range(steps + 1):
                    a = math.radians(start_angle + (angle - start_angle) * i / steps)
                    arc_out.append((half + math.cos(a) * outer, half - math.sin(a) * outer))
                    arc_in.append((half + math.cos(a) * inner, half - math.sin(a) * inner))
                if len(arc_out) >= 2:
                    pygame.draw.polygon(canvas, (r, g, b, fade), arc_out + arc_in[::-1])
        rotated = pygame.transform.rotate(self.base_image, angle)
        rad = math.radians(angle)
        wx = half + math.cos(rad) * reach
        wy = half - math.sin(rad) * reach
        canvas.blit(rotated, rotated.get_rect(center=(int(wx), int(wy))))
        self.image = canvas
        self.rect = canvas.get_rect(center=(int(self.player_x), int(self.player_y)))

        # 무거운 무기는 내려찍는 순간 땅이 울림
        if self.style == "heavy" and not self.impact_done and progress > 0.8:
            self.impact_done = True
            tip = reach + self.weapon_length * 0.4
            fx.add_shake(3.5)
            fx.burst(self.player_x + math.cos(rad) * tip, self.player_y - math.sin(rad) * tip,
                     (170, 150, 120), 10, speed=(1.0, 3.5), size=(2, 4), life=(10, 20), drag=0.85)

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.created_time
        progress = elapsed_time / (self.duration * 1000 / 60)  # 0 ~ 1

        if progress >= 1.0:
            self.kill()
            return
        self._render(progress)


# 능력 선택 메뉴
# ===== 게임 화면 HUD =====
# 좀비 종류별 이름 / 체력 바 색 (예전에는 매 프레임 좀비마다 사전을 새로 만들었음)
ZOMBIE_DISPLAY_NAMES = {
    # 일반 계열
    "normal": "일반좀비", "spike": "가시좀비", "armored": "갑옷좀비",
    "heavy": "무거운좀비", "poison": "독좀비", "ice": "얼음좀비",
    # 탱크 계열
    "tank": "탱크", "knight": "기사좀비", "resurrected_knight": "기사좀비(갑옷)", "shield": "방패좀비",
    "stone": "돌좀비", "iron": "철좀비", "wall": "벽좀비",
    # 빠른 계열
    "fast": "빠른좀비", "runner": "주자좀비", "ninja": "닌자좀비",
    "spark": "번개좀비", "wind": "바람좀비", "shadow": "그림자좀비",
    # 폭탄 계열
    "bomber": "폭탄좀비", "mine": "지뢰좀비", "flame": "불좀비",
    "acid": "산성좀비", "toxic": "독가스좀비", "nuclear": "핵좀비",
    # 보스 계열
    "boss": "보스", "gangster": "갱스터", "paladin": "기사단장", "demon": "악마좀비", "angel": "천사좀비",
    "dragon": "용좀비", "king": "왕좀비", "god": "신좀비",
    # 다른 좀비들
    "imp": "임프",
    # 거대 계열
    "colossus": "거대좀비", "titan": "타이탄", "giant": "거인",
    "behemoth": "베헤모스", "leviathan": "리바이어던", "elder": "엘더",
    # 새 좀비
    "slime": "분열좀비", "sniper_z": "저격좀비", "howler": "함성좀비",
}
ZOMBIE_BAR_COLORS = {
    "normal": (200, 0, 0), "spike": (200, 50, 50), "armored": (100, 100, 150),
    "heavy": (150, 100, 50), "poison": (0, 200, 50), "ice": (100, 200, 255),
    "tank": (200, 100, 0), "knight": (150, 150, 200), "shield": (180, 100, 50),
    "stone": (120, 120, 130), "iron": (80, 80, 100), "wall": (100, 60, 20),
    "fast": (255, 150, 0), "runner": (255, 120, 0), "ninja": (50, 50, 100),
    "spark": (255, 200, 0), "wind": (150, 200, 200), "shadow": (80, 40, 100),
    "bomber": (180, 50, 200), "mine": (100, 0, 100), "flame": (255, 100, 0),
    "acid": (150, 200, 0), "toxic": (100, 200, 50), "nuclear": (200, 100, 0),
    "boss": (255, 215, 0), "demon": (200, 0, 100), "angel": (255, 255, 200),
    "dragon": (150, 0, 150), "king": (255, 200, 100), "god": (255, 255, 255),
    "gangster": (150, 150, 150), "paladin": (200, 200, 150), "imp": (200, 50, 100),
    "apostle": (255, 255, 200),
    "colossus": (100, 100, 100), "titan": (100, 50, 0), "giant": (150, 100, 50),
    "behemoth": (80, 80, 80), "leviathan": (0, 100, 150), "elder": (100, 150, 100),
    "slime": (90, 220, 90), "sniper_z": (120, 170, 120), "howler": (240, 150, 50),
}
ABILITY_LABELS = {"speed": ("속도형", CYAN), "tank": ("탱커형", (110, 160, 255)), "damage": ("공격형", YELLOW)}


def zombie_display_name(zombie):
    return zombie.custom_name if hasattr(zombie, "custom_name") else ZOMBIE_DISPLAY_NAMES.get(zombie.zombie_type, "좀비")


def draw_zombie_labels(surface, camera, zombies):
    """좀비 머리 위: 이름 + 체력 숫자 한 줄, 그 아래 둥근 체력 바 (화면 밖 좀비는 건너뜀)"""
    width, height = surface.get_size()
    for zombie in zombies:
        sx, sy = camera.apply(zombie.rect.centerx, zombie.rect.centery)
        if sx < -120 or sx > width + 120 or sy < -120 or sy > height + 120:
            continue
        bar_w = max(30, zombie.size)
        top = sy - zombie.size // 2 - 15
        ratio = max(0, min(1, zombie.health / max(zombie.max_health, 1)))
        hp = int(max(0, zombie.health))
        key = (zombie_display_name(zombie), hp, int(bar_w * ratio), bar_w, zombie.zombie_type)
        cached = zombie.__dict__.get("_label_cache")
        if cached is None or cached[0] != key:
            color = ui_bright(ZOMBIE_BAR_COLORS.get(zombie.zombie_type, RED), 150)
            text, tw, th = _render_cached(font_tiny, f"{key[0]} {hp}", color, True)
            lw = max(tw + 2, bar_w + 2)
            label = pygame.Surface((lw, th + 9), pygame.SRCALPHA)
            bar_x = lw // 2 - bar_w // 2
            pygame.draw.rect(label, (12, 12, 16), (bar_x - 1, th + 1, bar_w + 2, 8), border_radius=3)
            if ratio > 0:
                pygame.draw.rect(label, color, (bar_x, th + 2, max(2, int(bar_w * ratio)), 6), border_radius=3)
            label.blit(text, (lw // 2 - tw // 2, 0))
            cached = zombie._label_cache = (key, label)
        label = cached[1]
        surface.blit(label, (int(sx) - label.get_width() // 2, int(top) - 2 - (label.get_height() - 9)))


def get_player_buffs(player):
    """(표시 글자, 키, 남은 프레임, 색) 목록"""
    buffs = []
    if player.damage_buff_time > 0:
        buffs.append(("공격력 +30%", "damage", player.damage_buff_time, ITEM_COLORS["damage"]))
    if player.speed_buff_time > 0:
        buffs.append(("이동속도 +30%", "speed", player.speed_buff_time, ITEM_COLORS["speed"]))
    if player.katana_chain > 0:
        bonus = int(round(get_katana_chain_bonus(player) * player.katana_chain * 100))
        buffs.append((f"연참 x{player.katana_chain} (다음 일섬 +{bonus}%)", "chain", player.katana_chain_timer, (150, 230, 255)))
    if player.rush_time > 0:
        buffs.append(("러시 (공격 속도 3배)", "rush", player.rush_time, (255, 160, 200)))
    if player.invuln_time > 20:   # 부활 무적 등 (일섬 직후 0.2초 무적은 너무 짧아서 표시 안 함)
        buffs.append(("무적", "invuln", player.invuln_time, (150, 230, 255)))
    if player.shock_time > 0:
        buffs.append(("감전 - 공격 불가", "shock", player.shock_time, (255, 240, 90)))
    if player.corrode_time > 0:
        buffs.append(("부식 - 받는 피해 +30%", "corrode", player.corrode_time, (170, 220, 60)))
    return buffs


def draw_player_status(surface, player, x=14, y=14):
    """좌상단 패널: 레벨 / 체력 / 경험치 / 무기 / 스킬 쿨타임 / 버프 (1인·멀티 공용)"""
    buffs = get_player_buffs(player)
    maxes = player.__dict__.setdefault("_ui_buff_max", {})
    w = 350
    h = 150 + len(buffs) * 24 + (4 if buffs else 0)
    ui_panel(surface, (x, y, w, h), alpha=175)

    badge = pygame.Rect(x + 12, y + 12, 54, 54)
    pygame.draw.rect(surface, (50, 46, 42), badge, border_radius=12)
    pygame.draw.rect(surface, UI_ACCENT, badge, 2, border_radius=12)
    ui_text(surface, "LV", font_tiny, UI_SUB, (badge.centerx, badge.y + 2), "midtop", shadow=False)
    ui_text(surface, player.level, font_hud, UI_TEXT, (badge.centerx, badge.bottom - 3), "midbottom")

    ratio = max(0, min(1, player.health / max(player.max_health, 1)))
    hp_color = UI_GOOD if ratio > 0.5 else (255, 200, 60) if ratio > 0.25 else UI_DANGER
    bx, bw = x + 78, w - 90
    ui_bar(surface, (bx, y + 12, bw, 26), ratio, hp_color, label=f"{int(max(0, player.health))} / {int(player.max_health)}")
    ui_bar(surface, (bx, y + 44, bw, 10), player.exp / max(player.exp_to_level, 1), UI_EXP, back=(36, 40, 48), radius=5)
    ui_text(surface, f"EXP {int(player.exp)}/{int(player.exp_to_level)}", font_tiny, UI_SUB, (bx, y + 56), shadow=False)
    if player.ability in ABILITY_LABELS:
        name, color = ABILITY_LABELS[player.ability]
        ui_text(surface, name, font_tiny, color, (x + w - 12, y + 56), "topright", shadow=False)
    pygame.draw.line(surface, UI_BORDER, (x + 12, y + 80), (x + w - 12, y + 80))

    ui_text(surface, player.weapon.name, font_hud, ui_bright(player.weapon.color), (x + 14, y + 86))
    attacks_per_second = player.weapon.fire_rate * player.weapon.attack_speed
    ui_text(surface, f"피해 {get_weapon_damage(player):.0f} · 초당 {attacks_per_second:.1f}회", font_tiny, UI_SUB,
            (x + w - 12, y + 90), "topright", shadow=False)

    now = pygame.time.get_ticks()
    weapon_type = player.weapon.weapon_type
    remain = max(0, player.skill_cooldowns[weapon_type] - now)
    total = max(1, SKILL_COOLDOWNS.get(weapon_type, 10000) * (1 - player.skill_cooldown_reduction))
    skill_rect = (x + 12, y + 116, w - 24, 22)
    if remain <= 0:
        pulse = 0.5 + 0.5 * math.sin(now / 180)
        ui_bar(surface, skill_rect, 1, (int(70 + 50 * pulse), 210, int(110 + 40 * pulse)), back=(20, 40, 28),
               label="우클릭 스킬 준비 완료!", font=font_hud, label_color=(10, 40, 20))
    else:
        ui_bar(surface, skill_rect, 1 - remain / total, (106, 155, 204), back=(44, 41, 38),
               label=f"우클릭 스킬 {remain / 1000:.1f}초", font=font_tiny)

    by = y + 146
    active = set()
    for label, key, frames, color in buffs:
        active.add(key)
        maxes[key] = max(maxes.get(key, 0), frames)
        ui_text(surface, f"{label}  {frames / FPS:.1f}초", font_tiny, ui_bright(color), (x + 14, by), shadow=False)
        ui_bar(surface, (x + w - 84, by + 6, 72, 8), frames / max(maxes[key], 1), ui_bright(color, 150), back=(30, 30, 40), radius=4)
        by += 24
    for key in list(maxes):
        if key not in active:
            del maxes[key]


def draw_wave_panel(surface, wave, wave_progress=None, wave_interval=60000, subtitle=None):
    """화면 위 가운데: 웨이브 번호 + 다음 웨이브까지 남은 시간"""
    pw = 260
    panel = ui_panel(surface, (surface.get_width() // 2 - pw // 2, 12, pw, 90 if wave_progress is not None else 58), alpha=175)
    ui_text(surface, f"WAVE {wave}", font_hud_big, UI_ACCENT, (panel.centerx, panel.y + 4), "midtop")
    if wave_progress is not None:
        wave_progress = max(0.0, min(1.0, wave_progress))
        ui_bar(surface, (panel.x + 18, panel.y + 52, pw - 36, 8), wave_progress, (220, 90, 80), back=(40, 22, 26), radius=4)
        left = max(0, wave_interval * (1 - wave_progress) / 1000)
        ui_text(surface, subtitle or f"다음 웨이브까지 {left:.0f}초", font_tiny, UI_SUB, (panel.centerx, panel.y + 64), "midtop", shadow=False)
    return panel


def draw_boss_bar(surface, zombies, y):
    """보스/거대 좀비가 있으면 가장 강한 개체의 체력을 화면 위에 크게"""
    boss = max((z for z in zombies if z.zombie_type in GUARANTEED_DROP_TYPES and z.health > 0),
               key=lambda z: z.max_health, default=None)
    if boss is None:
        return
    bw = min(560, surface.get_width() - 820)
    if bw < 200:
        bw = min(560, surface.get_width() - 40)
        y += 150
    rect = pygame.Rect(surface.get_width() // 2 - bw // 2, y + 24, bw, 16)
    color = ui_bright(ZOMBIE_BAR_COLORS.get(boss.zombie_type, RED), 160)
    ui_text(surface, zombie_display_name(boss), font_hud, color, (rect.centerx, rect.y - 2), "midbottom")
    ui_bar(surface, rect, boss.health / max(boss.max_health, 1), (210, 50, 70), back=(40, 14, 20), radius=6)
    ui_text(surface, f"{int(boss.health)} / {int(boss.max_health)}", font_tiny, UI_TEXT, rect.center, "center")


def draw_controls_bar(surface, text):
    """화면 아래: 아이템 안내 (왼쪽) + 조작법 (가운데)"""
    width, height = surface.get_size()
    legend_x, legend_y = 16, height - 34
    for item_type in ("health", "damage", "speed"):
        pygame.draw.rect(surface, ITEM_COLORS[item_type], (legend_x, legend_y + 3, 14, 14), border_radius=4)
        rect = ui_text(surface, Item.EFFECT_TEXTS[item_type], font_tiny, UI_SUB, (legend_x + 20, legend_y))
        legend_x = rect.right + 18
    ui_text(surface, text, font_tiny, UI_DIM, (max(width // 2, legend_x + 20 + font_tiny.size(text)[0] // 2), height - 30), "midtop")


def draw_hud(surface, player, score, wave, wave_progress, wave_interval, zombies, show_stack):
    width, height = surface.get_size()
    draw_player_status(surface, player)
    wave_box = draw_wave_panel(surface, wave, wave_progress, wave_interval)
    draw_boss_bar(surface, zombies, wave_box.bottom + 6)

    # 오른쪽 위: 점수 + 강화 레벨
    melee = player.weapon.weapon_type in MELEE_WEAPONS
    pw = 280
    panel = ui_panel(surface, (width - pw - 14, 14, pw, 130 + (24 if melee else 0)), alpha=175)
    ui_text(surface, "점수", font_tiny, UI_SUB, (panel.x + 14, panel.y + 18), shadow=False)
    ui_text(surface, f"{score:,}", font_hud_big, UI_TEXT, (panel.right - 14, panel.y + 6), "topright")
    stats = [("체력", player.levels["health"], (255, 110, 110)), ("데미지", player.levels["damage"], (255, 220, 90)),
             ("속도", player.levels["speed"], (110, 230, 255)), ("재생", player.levels["regen"], (120, 230, 140))]
    cell_w = (pw - 34) // 2
    for i, (label, level, color) in enumerate(stats):
        cell = pygame.Rect(panel.x + 12 + (i % 2) * (cell_w + 10), panel.y + 54 + (i // 2) * 34, cell_w, 28)
        pygame.draw.rect(surface, (46, 43, 39), cell, border_radius=8)
        ui_text(surface, label, font_tiny, color, (cell.x + 10, cell.centery), "midleft", shadow=False)
        ui_text(surface, f"Lv {level}", font_hud, UI_TEXT, (cell.right - 10, cell.centery), "midright", shadow=False)
    if melee:
        ui_text(surface, f"근접 강화 Lv.{player.weapon_upgrades[player.weapon.weapon_type]['damage']}", font_tiny,
                ui_bright(player.weapon.color), (panel.x + 14, panel.y + 128), shadow=False)

    # TAB: 획득한 업그레이드 목록
    if show_stack:
        names = [get_upgrade_entry_name(entry) for entry in player.obtained_upgrades]
        box = pygame.Rect(width - 314, panel.bottom + 10, 300, height - panel.bottom - 70)
        ui_panel(surface, box, alpha=210)
        ui_text(surface, f"획득한 업그레이드 ({len(names)})", font_hud, UI_ACCENT, (box.x + 14, box.y + 10))
        max_items = max(1, (box.h - 60) // 24)
        for i, name in enumerate(names[-max_items:] if len(names) > max_items else names):
            ui_text(surface, f"• {name}", font_tiny, UI_TEXT, (box.x + 16, box.y + 44 + i * 24), shadow=False)
        if len(names) > max_items:
            ui_text(surface, f"(최근 {max_items}개 · 전체는 ESC → 능력 확인)", font_tiny, UI_ACCENT, (box.x + 16, box.bottom - 26), shadow=False)

    draw_controls_bar(surface, "WASD 이동 · 좌클릭 공격 · 우클릭 스킬 · TAB 업그레이드 목록 · ESC 일시정지")
    ui_text(surface, f"FPS {clock.get_fps():.0f}", font_tiny, UI_SUB, (width - 14, height - 52), "topright")


def draw_game_over(surface, title, stats, hint):
    """게임 오버 패널: 제목 + 기록 칸 + 안내"""
    ui_overlay(surface, 190)
    chip_w, gap = 140, 12
    panel = pygame.Rect(0, 0, max(520, len(stats) * (chip_w + gap) + 48), 290)
    panel.center = (surface.get_width() // 2, surface.get_height() // 2)
    ui_panel(surface, panel, alpha=240, border=(150, 50, 50), radius=16, width=2)
    ui_text(surface, title, font_title, UI_DANGER, (panel.centerx, panel.y + 26), "midtop")
    x = panel.centerx - (len(stats) * chip_w + (len(stats) - 1) * gap) // 2
    for label, value in stats:
        chip = ui_panel(surface, (x, panel.y + 120, chip_w, 70), alpha=230, fill=(42, 39, 36), radius=10)
        ui_text(surface, label, font_tiny, UI_SUB, (chip.centerx, chip.y + 8), "midtop", shadow=False)
        ui_text(surface, f"{value:,}" if isinstance(value, int) else value, font_hud, UI_TEXT, (chip.centerx, chip.y + 32), "midtop", shadow=False)
        x += chip_w + gap
    pulse = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() / 250)
    ui_text(surface, hint, font_desc, (int(100 * pulse), int(230 * pulse), int(130 * pulse)), (panel.centerx, panel.bottom - 60), "midtop")


def _card_row(count, card_w, card_h, y, gap=28, margin=40):
    """화면 가운데 정렬된 카드 한 줄의 위치들 (화면이 좁으면 카드 폭을 줄임)"""
    card_w = min(card_w, (SCREEN_WIDTH - margin * 2 - gap * (count - 1)) // count)
    x0 = SCREEN_WIDTH // 2 - (count * card_w + (count - 1) * gap) // 2
    return [pygame.Rect(x0 + i * (card_w + gap), int(y), card_w, card_h) for i in range(count)]


def select_ability():
    abilities = [
        {"name": "속도형", "up": "이동속도 +50%", "down": "체력 -20%", "tip": "치고 빠지기, 원거리 무기와 잘 맞음", "type": "speed", "color": (110, 185, 205)},
        {"name": "탱커형", "up": "체력 +50%", "down": "이동속도 -30%", "tip": "버티면서 근접 무기로 싸우기 좋음", "type": "tank", "color": (135, 150, 225)},
        {"name": "공격형", "up": "데미지 +60%", "down": "체력 -10%", "tip": "빠르게 처치해서 위험을 줄임", "type": "damage", "color": (232, 180, 90)},
    ]
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    while True:
        ui_background(screen)
        ui_title(screen, "능력을 선택하세요", SCREEN_HEIGHT * 0.14, "게임 내내 유지되는 기본 성향")
        rects = _card_row(3, 300, 210, SCREEN_HEIGHT // 2 - 105, gap=36)
        mouse_pos = pygame.mouse.get_pos()
        for i, (ability, rect) in enumerate(zip(abilities, rects)):
            hover = rect.collidepoint(mouse_pos)
            card = ui_card(screen, rect, ability["color"], hover, ability["name"], badge=f"[{i + 1}]", title_font=font_small,
                           title_color=ui_bright(ability["color"]))
            y = card.y + 70
            for text, color in ((ability["up"], UI_GOOD), (ability["down"], UI_DANGER)):
                pygame.draw.circle(screen, color, (card.x + 26, y + 12), 4)
                ui_text(screen, text, font_medium, color, (card.x + 38, y - 4), shadow=False)
                y += 38
            for line in ui_wrap(ability["tip"], font_tiny, card.w - 40):
                y = ui_text(screen, line, font_tiny, UI_SUB, (card.x + 20, y + 6), shadow=False).bottom - 4
        ui_text(screen, "클릭 또는 1 / 2 / 3 키로 선택", font_desc, UI_SUB, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70), "midtop", shadow=False)

        for event in pygame.event.get():
            ui_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                return abilities[event.key - pygame.K_1]["type"]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ability, rect in zip(abilities, rects):
                    if rect.collidepoint(event.pos):
                        return ability["type"]

        pygame.display.flip()
        clock.tick(60)


# 무기 선택 메뉴
def select_weapon():
    weapons = [
        {"name": "글록", "desc": "균형 잡힌 권총", "skill": "항공 폭격", "type": "glock", "color": YELLOW},
        {"name": "샷건", "desc": "근거리 3발 산탄", "skill": "용의 숨결", "type": "shotgun", "color": (230, 130, 30)},
        {"name": "저격총", "desc": "강한 한 발, 관통", "skill": "도탄 사격", "type": "sniper", "color": (200, 205, 230)},
        {"name": "기관총", "desc": "꾹 눌러 연사", "skill": "포탑 설치", "type": "machinegun", "color": (255, 130, 70)},
        {"name": "플라즈마", "desc": "착탄 시 작은 폭발", "skill": "블랙홀", "type": "plasma", "color": CYAN},
        {"name": "로켓", "desc": "느리지만 큰 폭발", "skill": "미사일 폭격", "type": "rocket", "color": (255, 80, 60)},
        {"name": "나무 방망이", "desc": "기본 근접", "skill": "홈런", "type": "melee", "color": (210, 140, 70)},
        {"name": "카타나", "desc": "빠른 베기", "skill": "일섬 (돌진)", "type": "katana", "color": (255, 215, 0)},
        {"name": "도끼", "desc": "강한 한 방, 넉백", "skill": "대회전 베기 (흡혈)", "type": "axe", "color": (230, 90, 120)},
        {"name": "창", "desc": "속도 비례 데미지, 달리면 돌진", "skill": "물보라", "type": "spear", "color": (200, 200, 70)},
        {"name": "해머", "desc": "묵직한 한 방, 최강 넉백", "skill": "대지 강타 (기절)", "type": "hammer", "color": (205, 205, 215)},
        {"name": "글로브", "desc": "초고속, 짧은 사거리", "skill": "러시 (공속 3배)", "type": "gloves", "color": (255, 170, 200)},
    ]
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    card_h = 172
    while True:
        ui_background(screen)
        top = ui_title(screen, "무기를 선택하세요", 24, "게임 시작 후에는 바꿀 수 없음 · 우클릭으로 무기 전용 스킬 사용")
        first = max(top + 46, (SCREEN_HEIGHT - (card_h * 2 + 58)) // 2 - 20)
        rows_y = [first, first + card_h + 58]
        rects = _card_row(6, 210, card_h, rows_y[0], gap=16) + _card_row(6, 210, card_h, rows_y[1], gap=16)
        for label, y, rect in (("원거리", rows_y[0], rects[0]), ("근접", rows_y[1], rects[6])):
            ui_text(screen, label, font_hud, UI_ACCENT, (rect.x, y - 30))
            pygame.draw.line(screen, UI_BORDER, (rect.x + 60, y - 18), (rects[5].right, y - 18))
        mouse_pos = pygame.mouse.get_pos()
        for weapon, rect in zip(weapons, rects):
            stats = WEAPON_STATS[weapon["type"]]
            hover = rect.collidepoint(mouse_pos)
            card = ui_card(screen, rect, weapon["color"], hover, weapon["name"], [weapon["desc"]], title_color=ui_bright(weapon["color"]))
            ui_text(screen, f"피해 {stats['dmg']} · 초당 {stats['rate']}회", font_tiny, UI_TEXT, (card.x + 20, card.bottom - 50), shadow=False)
            ui_text(screen, f"스킬: {weapon['skill']}", font_tiny, (120, 230, 255), (card.x + 20, card.bottom - 28), shadow=False)

        for event in pygame.event.get():
            ui_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for weapon, rect in zip(weapons, rects):
                    if rect.collidepoint(event.pos):
                        return weapon["type"]

        pygame.display.flip()
        clock.tick(60)


# 일시정지 메뉴
def show_pause_menu(player):
    """게임 일시정지 메뉴 표시 (뒤에 멈춘 게임 화면이 비쳐 보임)"""
    background = ui_snapshot()
    buttons = [
        {"name": "돌아가기", "desc": "게임 계속하기 (ESC)", "type": "resume", "color": (128, 196, 132)},
        {"name": "능력 확인", "desc": "획득한 능력 보기", "type": "abilities", "color": (106, 155, 204)},
        {"name": "저장하고 나가기", "desc": "다음에 실행하면 이어하기", "type": "save_exit", "color": (232, 180, 90)},
        {"name": "처음으로", "desc": "저장하지 않고 능력 선택화면으로", "type": "exit", "color": (228, 92, 78)},
    ]
    btn_w, btn_h, gap = 380, 76, 14
    panel = pygame.Rect(0, 0, btn_w + 60, 150 + len(buttons) * (btn_h + gap))
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    rects = [pygame.Rect(panel.x + 30, panel.y + 130 + i * (btn_h + gap), btn_w, btn_h) for i in range(len(buttons))]
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)

    while True:
        screen.blit(background, (0, 0))
        ui_overlay(screen, 175)
        ui_panel(screen, panel, alpha=235, radius=16)
        ui_text(screen, "일시정지", font_large, UI_TEXT, (panel.centerx, panel.y + 22), "midtop")
        ui_text(screen, f"LV.{player.level} · {player.weapon.name} · 체력 {int(player.health)}/{int(player.max_health)}",
                font_desc, UI_SUB, (panel.centerx, panel.y + 86), "midtop", shadow=False)
        mouse_pos = pygame.mouse.get_pos()
        for button, rect in zip(buttons, rects):
            ui_button(screen, rect, button["name"], button["color"], rect.collidepoint(mouse_pos), button["desc"])

        for event in pygame.event.get():
            ui_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"      # ESC를 다시 누르면 일시정지 해제
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button, rect in zip(buttons, rects):
                    if rect.collidepoint(event.pos):
                        if button["type"] == "abilities":
                            show_obtained_upgrades(player, background)   # 보고 나면 다시 일시정지 메뉴로
                        else:
                            # "exit": 게임을 처음부터 다시 시작 (main()을 재귀 호출하지 않고 호출한 쪽에서 재시작 처리)
                            return button["type"]

        pygame.display.flip()
        clock.tick(60)


def get_upgrade_entry_type(upgrade_entry):
    if isinstance(upgrade_entry, dict):
        return upgrade_entry.get("type", "")
    return upgrade_entry


def get_upgrade_entry_name(upgrade_entry):
    if isinstance(upgrade_entry, dict):
        if "name" in upgrade_entry:
            return upgrade_entry["name"]
        return get_upgrade_name(upgrade_entry.get("type", ""))
    return get_upgrade_name(upgrade_entry)


def get_upgrade_entry_value(upgrade_entry, default_value=0):
    if isinstance(upgrade_entry, dict) and "value" in upgrade_entry:
        return upgrade_entry["value"]
    return default_value


def build_cumulative_upgrade_lines(player):
    counts = {}
    weapon_damage_bonus = 0
    melee_damage_bonus = 0

    melee_default_values = {
        "melee": 4,
        "katana": 3,
        "axe": 8,
        "spear": 4,
        "hammer": 10,
        "gloves": 2,
    }

    for entry in player.obtained_upgrades:
        upgrade_type = get_upgrade_entry_type(entry)
        if not upgrade_type:
            continue

        counts[upgrade_type] = counts.get(upgrade_type, 0) + 1

        if upgrade_type == "weapon_damage":
            weapon_damage_bonus += get_upgrade_entry_value(entry, 2)
        elif upgrade_type.startswith("melee_damage_"):
            weapon_name = upgrade_type.replace("melee_damage_", "")
            melee_damage_bonus += get_upgrade_entry_value(entry, melee_default_values.get(weapon_name, 3))

    def fmt_num(value):
        if isinstance(value, float):
            if abs(value - int(value)) < 0.0001:
                return str(int(value))
            return f"{value:.1f}"
        return str(value)

    lines = []

    max_health_bonus = counts.get("health", 0) * 8 + counts.get("health_big", 0) * 12
    speed_bonus = counts.get("speed", 0) * 0.3 + counts.get("speed_big", 0) * 0.5
    base_damage_mult = (1.08 ** counts.get("base_damage", 0)) * (1.15 ** counts.get("base_damage_big", 0))
    regen_bonus = counts.get("regen", 0) * 0.3 + counts.get("regen_big", 0) * 0.5

    if max_health_bonus > 0:
        lines.append(f"최대 체력: +{max_health_bonus}")
    if speed_bonus > 0:
        lines.append(f"이동 속도: +{fmt_num(speed_bonus)}")
    if base_damage_mult > 1:
        lines.append(f"공격력: +{(base_damage_mult - 1) * 100:.0f}%")
    if regen_bonus > 0:
        lines.append(f"재생: +{fmt_num(regen_bonus)}/초")

    if counts.get("exp_boost", 0) > 0:
        lines.append(f"경험치 보너스: +{counts.get('exp_boost', 0) * 20}%")

    crit_percent = player.levels.get("crit", 0) * 5
    dodge_percent = player.levels.get("dodge", 0) * 5
    if crit_percent > 0:
        lines.append(f"치명타 확률: +{crit_percent}%")
    if dodge_percent > 0:
        lines.append(f"회피율: +{dodge_percent}%")

    cooldown_percent = int(round(player.skill_cooldown_reduction * 100))
    if cooldown_percent > 0:
        lines.append(f"스킬 쿨타임 감소: {cooldown_percent}%")

    if weapon_damage_bonus > 0:
        lines.append(f"무기 공격력(직접 강화): +{weapon_damage_bonus}")
    if melee_damage_bonus > 0:
        lines.append(f"근접 무기 공격력(전용 강화): +{melee_damage_bonus}")

    if counts.get("glock_skill_burst", 0) > 0:
        lines.append(f"항공 폭격 범위: 길이 +{counts['glock_skill_burst'] * GLOCK_STRIKE_RANGE_LENGTH}px, 폭 +{counts['glock_skill_burst'] * GLOCK_STRIKE_RANGE_WIDTH}px")
    if counts.get("shotgun_skill_pellets", 0) > 0:
        lines.append(f"샷건 추가 탄환: +{counts['shotgun_skill_pellets']}발")
    if counts.get("sniper_skill_critdmg", 0) > 0:
        lines.append(f"치명타 피해: {int(CRIT_BASE_MULT * 100)}% → {int(get_crit_multiplier(player) * 100)}%")
    if counts.get("sniper_skill_pierces", 0) > 0:
        lines.append(f"도탄 사격 튕김: +{counts['sniper_skill_pierces'] * SNIPER_RICOCHET_UPGRADE}회")
    if counts.get("machinegun_skill_burst", 0) > 0:
        lines.append(f"포탑 지속: +{counts['machinegun_skill_burst']}초")

    if counts.get("katana_skill_strikes", 0) > 0:
        lines.append(f"일섬 거리: +{counts['katana_skill_strikes'] * 40}px")
    if counts.get("melee_damage_katana", 0) > 0:
        lines.append(f"일섬 추가 데미지 (카타나 강화): +{counts['melee_damage_katana'] * 10}%")
    if counts.get("katana_skill_ougi", 0) > 0:
        lines.append(f"오의 연섬: 일섬 피해 {int(KATANA_OUGI_RATIO * 100)}% → 고정 피해 (최소 대상 최대 체력 {int(KATANA_OUGI_HP_RATIO * 100)}%)")
    if counts.get("katana_skill_chain", 0) > 0:
        lines.append(f"연참 스택당 데미지: +{5 + counts['katana_skill_chain'] * 3}%")
    if counts.get("gloves_skill_strikes", 0) > 0:
        lines.append(f"러시 시간: +{counts['gloves_skill_strikes'] * 0.5:.1f}초")
    if counts.get("spear_skill_pierces", 0) > 0:
        lines.append(f"물보라 범위: +{counts['spear_skill_pierces'] * 30}px")

    if counts.get("melee_skill_range", 0) > 0:
        lines.append(f"홈런 범위: +{counts['melee_skill_range'] * 12}px")
    if counts.get("axe_skill_range", 0) > 0:
        lines.append(f"대회전 베기 범위: +{counts['axe_skill_range'] * 25}px")
    if counts.get("hammer_skill_range", 0) > 0:
        lines.append(f"대지 강타 범위: +{counts['hammer_skill_range'] * 20}px")
    if counts.get("plasma_skill_range", 0) > 0:
        lines.append(f"블랙홀 범위: +{counts['plasma_skill_range'] * 15}px")
    if counts.get("rocket_skill_count", 0) > 0:
        lines.append(f"로켓 폭발 범위 증가: +{counts['rocket_skill_count'] * 15}px")

    if counts.get("attack_speed", 0) > 0:
        lines.append(f"공격 쿨 감소 획득: {counts['attack_speed']}회")
    if player.pierce_level > 0:
        lines.append(f"투사체 관통: +{player.pierce_level}마리")

    return lines


def show_obtained_upgrades(player, background=None):
    """현재까지 획득한 능력(순서) + 누적 효과를 탭으로 표시"""
    background = background or ui_snapshot()
    active_tab = "history"
    scroll_offsets = {"history": 0, "summary": 0}

    history_list = [get_upgrade_entry_name(entry) for entry in player.obtained_upgrades] or ["아직 획득한 능력이 없습니다."]
    summary_list = build_cumulative_upgrade_lines(player) or ["아직 누적된 능력이 없습니다."]

    item_height = 40
    panel = pygame.Rect(0, 0, min(900, SCREEN_WIDTH - 60), SCREEN_HEIGHT - 80)
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    tab_w, tab_h = 200, 42
    history_tab_rect = pygame.Rect(panel.centerx - tab_w - 8, panel.y + 92, tab_w, tab_h)
    summary_tab_rect = pygame.Rect(panel.centerx + 8, panel.y + 92, tab_w, tab_h)
    scroll_area = pygame.Rect(panel.x + 24, panel.y + 150, panel.w - 48, panel.h - 210)
    visible_height = scroll_area.h

    while True:
        current_list = history_list if active_tab == "history" else summary_list
        total_height = len(current_list) * item_height
        max_scroll = max(0, total_height - visible_height)
        scroll_offsets[active_tab] = max(0, min(max_scroll, scroll_offsets[active_tab]))

        screen.blit(background, (0, 0))
        ui_overlay(screen, 190)
        ui_panel(screen, panel, alpha=240, radius=16)
        ui_text(screen, "능력 확인", font_large, UI_TEXT, (panel.centerx, panel.y + 20), "midtop")

        for tab, rect, label in (("history", history_tab_rect, f"획득 순서 ({len(player.obtained_upgrades)})"),
                                 ("summary", summary_tab_rect, "누적 효과")):
            selected = active_tab == tab
            pygame.draw.rect(screen, UI_ACCENT if selected else (46, 43, 39), rect, border_radius=21)
            pygame.draw.rect(screen, (240, 170, 140) if selected else UI_BORDER, rect, 1, border_radius=21)
            ui_text(screen, label, font_desc, UI_TEXT if selected else UI_SUB, rect.center, "center", shadow=False)

        # 스크롤 목록 (영역 밖은 잘라냄)
        screen.set_clip(scroll_area)
        for i, line in enumerate(current_list):
            y_pos = scroll_area.y + i * item_height - scroll_offsets[active_tab]
            if y_pos < scroll_area.top - item_height or y_pos > scroll_area.bottom:
                continue
            row = pygame.Rect(scroll_area.x, y_pos, scroll_area.w - 16, item_height - 4)
            if i % 2 == 0:
                pygame.draw.rect(screen, (42, 39, 36), row, border_radius=8)
            if active_tab == "history":
                ui_text(screen, f"{i + 1}", font_hud, UI_ACCENT, (row.x + 30, row.centery), "center", shadow=False)
                ui_text(screen, line, font_medium, UI_TEXT, (row.x + 60, row.centery), "midleft", shadow=False)
            else:
                pygame.draw.circle(screen, UI_GOOD, (row.x + 18, row.centery), 4)
                ui_text(screen, line, font_medium, UI_TEXT, (row.x + 34, row.centery), "midleft", shadow=False)
        screen.set_clip(None)

        # 스크롤 바
        if max_scroll > 0 and total_height > 0:
            bar_h = max(30, visible_height * visible_height / total_height)
            bar_y = scroll_area.y + (scroll_offsets[active_tab] / max_scroll) * (visible_height - bar_h)
            pygame.draw.rect(screen, (60, 56, 51), (scroll_area.right - 8, scroll_area.y, 8, visible_height), border_radius=4)
            pygame.draw.rect(screen, UI_ACCENT, (scroll_area.right - 8, bar_y, 8, bar_h), border_radius=4)

        ui_text(screen, "탭 클릭: 화면 전환 · 마우스 휠/화살표: 스크롤 · ESC: 닫기", font_tiny, UI_SUB,
                (panel.centerx, panel.bottom - 36), "midtop", shadow=False)

        for event in pygame.event.get():
            ui_quit_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    scroll_offsets[active_tab] = max(0, scroll_offsets[active_tab] - 50)
                elif event.key == pygame.K_DOWN:
                    scroll_offsets[active_tab] = min(max_scroll, scroll_offsets[active_tab] + 50)
                elif event.key == pygame.K_TAB:
                    active_tab = "summary" if active_tab == "history" else "history"
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offsets[active_tab] = max(0, min(max_scroll, scroll_offsets[active_tab] - event.y * 30))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if history_tab_rect.collidepoint(event.pos):
                    active_tab = "history"
                elif summary_tab_rect.collidepoint(event.pos):
                    active_tab = "summary"

        pygame.display.flip()
        clock.tick(60)


def is_upgrade_at_limit(player, upgrade_type):
    """업그레이드가 최대치(또는 1회성 획득 완료)인지 판별"""
    # 명시적 횟수 제한
    if upgrade_type == "crit":
        return player.levels.get("crit", 0) >= 16  # 최대 80%
    if upgrade_type == "sniper_skill_critdmg":
        return player.skill_upgrades["sniper"].get("crit_damage", 0) >= SNIPER_CRIT_DAMAGE_MAX
    if upgrade_type == "dodge":
        return player.levels.get("dodge", 0) >= 20  # 최대 100%

    # 공통 쿨감 제한 (5%/10% 옵션 공유)
    if upgrade_type in ("skill_cooldown_reduction", "skill_cooldown_reduction_big"):
        return player.skill_cooldown_reduction >= 0.5

    # 무기와 맞지 않는 업그레이드는 나오지 않게
    weapon_type = player.weapon.weapon_type if player.weapon else None
    if weapon_type in MELEE_WEAPONS and upgrade_type in ("skill_piercing", "skill_infinity_ammo"):
        return True   # 근접 무기는 총알/탄약을 쓰지 않음
    if weapon_type == "rocket" and upgrade_type == "skill_piercing":
        return True   # 로켓은 처음 맞는 곳에서 폭발하므로 관통 의미 없음
    if upgrade_type == "knockback" and weapon_type not in MELEE_WEAPONS and weapon_type != "rocket":
        return True   # 넉백은 근접 무기와 로켓 폭발에만 있음

    # 오의 연섬: 카타나 레벨 6부터, 한 번만
    if upgrade_type == "katana_skill_ougi":
        return player.level < KATANA_OUGI_MIN_LEVEL or player.skill_upgrades["katana"].get("ougi", 0) >= 1

    # 관통은 레벨식 (최대 MAX_PIERCE_LEVEL)
    if upgrade_type == "skill_piercing":
        return player.pierce_level >= MAX_PIERCE_LEVEL

    # 1회성 스킬은 이미 보유 중이면 재등장 금지
    if upgrade_type in player.skills and player.skills.get(upgrade_type, False):
        return True

    # 공격 간격이 충분히 짧아지면(50ms 이하) 공격 속도 옵션은 더 이상 노출하지 않음
    # (창의 "투사체 속도" 옵션은 공격 속도가 아니므로 제외)
    is_attack_speed_upgrade = (
        upgrade_type in ("attack_speed", "weapon_firerate")
        or (upgrade_type.startswith("melee_skill_speed_") and upgrade_type != "melee_skill_speed_spear")
    )
    if is_attack_speed_upgrade and player.weapon:
        return player.weapon.fire_rate * player.weapon.attack_speed >= 20

    return False


def filter_upgrades_by_limit(player, upgrades):
    return [upgrade for upgrade in upgrades if not is_upgrade_at_limit(player, upgrade["type"])]


# 업그레이드 선택 메뉴
def build_upgrade_choices(player):
    """레벨업 업그레이드 후보 3개를 고름 (화면 없이 - 멀티에서도 사용)"""
    # 기본 보상 옵션들
    all_upgrades = [
        # 체력 관련
        {"name": "체력 +8", "desc": "최대 체력 증가", "type": "health", "color": RED},
        {"name": "체력 +12", "desc": "최대 체력 증가", "type": "health_big", "color": (255, 100, 100)},
        {"name": "체력 회복", "desc": "현재 체력 20% 회복", "type": "heal", "color": GREEN},
        {"name": "완전 회복", "desc": "체력을 완전히 회복", "type": "heal_full", "color": (0, 255, 100)},

        # 이동 관련
        {"name": "이동속도 +0.3", "desc": "이동 속도 증가", "type": "speed", "color": CYAN},
        {"name": "이동속도 +0.5", "desc": "이동 속도 증가", "type": "speed_big", "color": (0, 255, 255)},

        # 공격 관련
        {"name": "공격력 +8%", "desc": "무기 공격력 8% 증가", "type": "base_damage", "color": (255, 165, 0)},
        {"name": "공격력 +15%", "desc": "무기 공격력 15% 증가", "type": "base_damage_big", "color": (255, 100, 0)},

        # 넉백 관련
        {"name": "넉백 강화", "desc": "적 넉백 강도 +10%", "type": "knockback", "color": (200, 100, 255)},

        # 특수 효과
        {"name": "재생 능력", "desc": "초당 체력 0.3 회복", "type": "regen", "color": (100, 255, 100)},
        {"name": "재생 강화", "desc": "초당 체력 0.5 회복", "type": "regen_big", "color": (150, 255, 150)},

        # 경험치 관련
        {"name": "경험치 +20%", "desc": "좀비 처치 시 경험치 20% 추가", "type": "exp_boost", "color": (255, 255, 100)},

        # 특이 능력
        {"name": "치명타", "desc": f"치명타 확률 +5% ({get_crit_multiplier(player):.2f}배 데미지)", "type": "crit", "color": (255, 50, 50)},
        {"name": "회피", "desc": "5% 확률로 피해 회피", "type": "dodge", "color": (100, 200, 255)},

        # 무기별 추가 보상
        {"name": "공격 쿨 감소", "desc": "모든 무기 공격 속도 +5%", "type": "attack_speed", "color": (255, 200, 100)},

        # 우클릭 스킬 관련 (새로 추가)
        {"name": "스킬 쿨타임 -5%", "desc": "우클릭 스킬 쿨타임 5% 단축", "type": "skill_cooldown_reduction", "color": (150, 100, 255)},
        {"name": "스킬 쿨타임 -10%", "desc": "우클릭 스킬 쿨타임 10% 단축", "type": "skill_cooldown_reduction_big", "color": (180, 100, 255)},
    ]
    all_upgrades = filter_upgrades_by_limit(player, all_upgrades)

    # 스킬 옵션들 (레벨에 따라 추가)
    skill_options = [
        {"name": "무한탄약 (30초)", "desc": "일시적으로 탄약 무한 사용", "type": "skill_infinity_ammo", "color": (255, 215, 0), "min_level": 2},
        {"name": "투사체 관통 +1", "desc": f"총알이 1마리 더 관통 (현재 {player.pierce_level})", "type": "skill_piercing", "color": (100, 150, 255), "min_level": 3},
        {"name": "화염탄", "desc": "총알에 불이 붙어 화염 피해", "type": "skill_fire_bullets", "color": (255, 100, 0), "min_level": 2},
        {"name": "얼음탄", "desc": "좀비를 느리게 하는 총알", "type": "skill_ice_bullets", "color": (100, 200, 255), "min_level": 2},
        {"name": "전기탄", "desc": "인접한 좀비들에게 전기 전달", "type": "skill_electric_bullets", "color": (255, 255, 0), "min_level": 3},
        {"name": "자동조준", "desc": "가까운 적을 자동으로 조준", "type": "skill_auto_aim", "color": (150, 255, 100), "min_level": 4},
        {"name": "방어막", "desc": "플레이어 주변 방어막 생성", "type": "skill_shield", "color": (200, 200, 100), "min_level": 3},
        {"name": "순간이동", "desc": "마우스 위치로 즉시 이동", "type": "skill_teleport", "color": (200, 100, 255), "min_level": 4},
        {"name": "시간감속", "desc": "주변 좀비를 느리게 함", "type": "skill_slowdown", "color": (100, 255, 255), "min_level": 5},
        {"name": "폭발 공격", "desc": f"공격 시 작은 폭발 (주변 {int((EXPLOSION_SKILL_RATIO_MELEE if player.weapon.weapon_type in MELEE_WEAPONS else EXPLOSION_SKILL_RATIO) * 100)}%)",
         "type": "skill_explosion", "color": (255, 150, 0), "min_level": 4},
    ]

    # 플레이어 레벨 및 최대치에 따라 스킬 필터링
    available_skills = [
        s for s in skill_options
        if player.level >= s["min_level"] and not is_upgrade_at_limit(player, s["type"])
    ]

    # 무기 업그레이드 추가
    weapon_type = player.weapon.weapon_type

    # 무기별 특화 업그레이드
    if weapon_type == "melee":
        weapon_upgrades = [
            {"name": "홈런 범위 +12px", "desc": "홈런 범위 확대", "type": "melee_skill_range", "color": (150, 200, 150)},
            {"name": f"{player.weapon.name} 데미지 +4", "desc": "공격력 증가", "type": f"melee_damage_{weapon_type}", "color": player.weapon.color, "value": 4},
            {"name": "공격 속도 +8%", "desc": "더 빠른 공격", "type": f"melee_skill_speed_{weapon_type}", "color": (200, 150, 150)},
        ]
    elif weapon_type == "katana":
        weapon_upgrades = [
            {"name": "일섬 거리 +40px", "desc": "더 멀리 돌진", "type": "katana_skill_strikes", "color": (255, 200, 100)},
            {"name": "연참 데미지 +3%", "desc": "연참 스택당 데미지 증가", "type": "katana_skill_chain", "color": (150, 230, 255)},
            {"name": "오의 연섬 (패시브)", "desc": "일섬 피해 25%가 고정 피해로 (최소 대상 최대 체력 6%, 방어 무시)",
             "type": "katana_skill_ougi", "color": (230, 70, 70)},
            {"name": f"{player.weapon.name} 데미지 +3", "desc": "공격력 증가 + 일섬 데미지 +10%", "type": f"melee_damage_{weapon_type}", "color": player.weapon.color, "value": 3},
            {"name": "공격 속도 +12%", "desc": "더 빠른 공격", "type": f"melee_skill_speed_{weapon_type}", "color": (200, 150, 150)},
        ]
    elif weapon_type == "axe":
        weapon_upgrades = [
            {"name": "대회전 범위 +25px", "desc": "대회전 베기 범위 확대", "type": "axe_skill_range", "color": (150, 100, 200)},
            {"name": f"{player.weapon.name} 데미지 +8", "desc": "공격력 증가", "type": f"melee_damage_{weapon_type}", "color": player.weapon.color, "value": 8},
            {"name": "대회전 넉백 +12%", "desc": "대회전 베기 넉백 강화", "type": "axe_skill_knockback", "color": (200, 100, 200)},
        ]
    elif weapon_type == "spear":
        weapon_upgrades = [
            {"name": "물보라 범위 +30px", "desc": "물보라가 더 넓게 퍼짐", "type": "spear_skill_pierces", "color": (100, 150, 200)},
            {"name": f"{player.weapon.name} 데미지 +4", "desc": "공격력 증가", "type": f"melee_damage_{weapon_type}", "color": player.weapon.color, "value": 4},
            {"name": "물보라 둔화 +8%", "desc": "물보라에 맞은 좀비가 더 느려짐", "type": f"melee_skill_speed_{weapon_type}", "color": (150, 150, 200)},
        ]
    elif weapon_type == "hammer":
        weapon_upgrades = [
            {"name": "대지 강타 범위 +20px", "desc": "강타 범위 확대", "type": "hammer_skill_range", "color": (200, 200, 100)},
            {"name": f"{player.weapon.name} 데미지 +10", "desc": "공격력 증가", "type": f"melee_damage_{weapon_type}", "color": player.weapon.color, "value": 10},
            {"name": "대지 강타 피해 +10%", "desc": "강타 피해 증가", "type": "hammer_skill_damage", "color": (200, 150, 100)},
        ]
    elif weapon_type == "gloves":
        weapon_upgrades = [
            {"name": "러시 시간 +0.5초", "desc": "더 오래 러시", "type": "gloves_skill_strikes", "color": (200, 150, 200)},
            {"name": f"{player.weapon.name} 데미지 +2", "desc": "공격력 증가", "type": f"melee_damage_{weapon_type}", "color": player.weapon.color, "value": 2},
            {"name": "공격 속도 +10%", "desc": "더 빠른 펀치", "type": f"melee_skill_speed_{weapon_type}", "color": (200, 150, 150)},
        ]
    elif weapon_type == "glock":
        weapon_upgrades = [
            {"name": "폭격 범위 증가", "desc": "항공 폭격 길이 +100px, 폭 +15px", "type": "glock_skill_burst", "color": (255, 200, 100)},
            {"name": "데미지 +2", "desc": "공격력 증가", "type": "weapon_damage", "color": RED, "value": 2},
        ]
    elif weapon_type == "shotgun":
        weapon_upgrades = [
            {"name": "기본 발사 탄환 +1발", "desc": "3발 → 4발", "type": "shotgun_skill_pellets", "color": (255, 150, 100)},
            {"name": "화염 데미지 +8%", "desc": "용의 숨결 강화", "type": "shotgun_skill_damage", "color": (255, 100, 100)},
        ]
    elif weapon_type == "sniper":
        weapon_upgrades = [
            {"name": "도탄 +3회", "desc": "도탄 사격이 3번 더 튕김", "type": "sniper_skill_pierces", "color": (100, 150, 255)},
            {"name": "치명타 데미지 +25%", "desc": f"치명타 피해 {int(get_crit_multiplier(player) * 100)}% → {int((get_crit_multiplier(player) + SNIPER_CRIT_DAMAGE_UPGRADE) * 100)}%",
             "type": "sniper_skill_critdmg", "color": (255, 90, 90)},
            {"name": "데미지 +8", "desc": "공격력 증가", "type": "weapon_damage", "color": RED, "value": 8},
        ]
    elif weapon_type == "machinegun":
        weapon_upgrades = [
            {"name": "포탑 지속 +1초", "desc": "포탑이 더 오래 유지", "type": "machinegun_skill_burst", "color": (150, 150, 200)},
            {"name": "데미지 +1", "desc": "공격력 증가", "type": "weapon_damage", "color": RED, "value": 1},
        ]
    elif weapon_type == "plasma":
        weapon_upgrades = [
            {"name": "블랙홀 범위 +15px", "desc": "블랙홀 범위 확대", "type": "plasma_skill_range", "color": (100, 255, 255)},
            {"name": "블랙홀 데미지 +8%", "desc": "블랙홀 강화", "type": "plasma_skill_damage", "color": (100, 200, 255)},
        ]
    elif weapon_type == "rocket":
        weapon_upgrades = [
            {"name": "로켓 범위 +15px", "desc": "폭발 범위 확대", "type": "rocket_skill_count", "color": (255, 100, 100)},
            {"name": "폭격 데미지 +5%", "desc": "미사일 폭격 강화", "type": "rocket_skill_damage", "color": (255, 150, 100)},
        ]
    else:
        weapon_upgrades = []

    weapon_upgrades = filter_upgrades_by_limit(player, weapon_upgrades)

    all_upgrades.extend(weapon_upgrades)

    # 최소 레벨을 만족한 스킬은 즉시 후보에 추가
    if available_skills:
        all_upgrades.extend(available_skills)

    # 후보가 모두 제한에 걸린 경우, 선택이 멈추지 않도록 안전 후보 추가
    if not all_upgrades:
        all_upgrades = [{"name": "체력 회복", "desc": "선택 가능한 능력이 없어 자동 제공", "type": "heal", "color": GREEN}]

    # 중복 획득 가능 - 필터링 제거
    # 랜덤 선택 (3개 표시)
    return random.sample(all_upgrades, min(3, len(all_upgrades)))


def show_upgrade_menu(player, camera):
    selected_upgrades = build_upgrade_choices(player)
    background = ui_snapshot()     # 멈춘 게임 화면을 뒤에 보여줌

    # 공격하느라 연타하던 클릭이 메뉴가 뜨자마자 아무 업그레이드나 골라버리지 않도록
    # 남아 있는 클릭을 비우고 잠깐(0.3초) 입력을 막음
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    menu_open_time = pygame.time.get_ticks()
    keys = (pygame.K_1, pygame.K_2, pygame.K_3)

    while True:
        elapsed = pygame.time.get_ticks() - menu_open_time
        screen.blit(background, (0, 0))
        ui_overlay(screen, 170)

        # 카드가 아래에서 살짝 떠오르며 나타남
        rise = max(0, 40 - elapsed // 5)
        top = ui_title(screen, "레벨 업!", SCREEN_HEIGHT // 2 - 230, f"LV.{player.level} · 한 가지를 선택하세요", color=UI_ACCENT)
        rects = _card_row(len(selected_upgrades), 300, 140, max(top + 40, SCREEN_HEIGHT // 2 - 85) + rise, gap=30)
        mouse_pos = pygame.mouse.get_pos()
        for i, (upgrade, rect) in enumerate(zip(selected_upgrades, rects)):
            ui_card(screen, rect, upgrade["color"], rect.collidepoint(mouse_pos), upgrade["name"], [upgrade["desc"]],
                    badge=f"[{i + 1}]", title_color=ui_bright(upgrade["color"]))
        ui_text(screen, f"획득한 업그레이드 {len(player.obtained_upgrades)}개 · 클릭 또는 1 / 2 / 3 키", font_desc, UI_SUB,
                (SCREEN_WIDTH // 2, rects[0].bottom + 40), "midtop", shadow=False)

        for event in pygame.event.get():
            ui_quit_event(event)
            if elapsed < 300:
                continue
            if event.type == pygame.KEYDOWN and event.key in keys[:len(selected_upgrades)]:
                return selected_upgrades[keys.index(event.key)]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for upgrade, rect in zip(selected_upgrades, rects):
                    if rect.collidepoint(event.pos):
                        return upgrade

        pygame.display.flip()
        clock.tick(60)


# 메인 게임 루프
def apply_upgrade(player, selected_upgrade):
    """고른 업그레이드를 플레이어에게 적용 (1인/멀티 공용)"""
    # 획득한 업그레이드에 추가
    upgrade_record = {
        "type": selected_upgrade["type"],
        "name": selected_upgrade.get("name", get_upgrade_name(selected_upgrade["type"]))
    }
    if "value" in selected_upgrade:
        upgrade_record["value"] = selected_upgrade["value"]
    player.obtained_upgrades.append(upgrade_record)

    if selected_upgrade["type"] == "health":
        player.max_health += 8
        player.health = min(player.health + 8, player.max_health)
        player.levels["health"] += 1
    elif selected_upgrade["type"] == "health_big":
        player.max_health += 12
        player.health = min(player.health + 12, player.max_health)
        player.levels["health"] += 1
    elif selected_upgrade["type"] == "speed":
        player.speed += 0.3
        player.levels["speed"] += 1
    elif selected_upgrade["type"] == "speed_big":
        player.speed += 0.5
        player.levels["speed"] += 1
    elif selected_upgrade["type"] == "heal":
        player.health = min(player.health * 1.2, player.max_health)
    elif selected_upgrade["type"] == "heal_full":
        player.health = player.max_health
    elif selected_upgrade["type"] == "base_damage":
        # 무기 공격력 +8% (무기마다 기본 데미지가 달라서 고정값 대신 비율로)
        player.weapon.damage *= 1.08
        player.levels["damage"] += 1
    elif selected_upgrade["type"] == "base_damage_big":
        player.weapon.damage *= 1.15
        player.levels["damage"] += 1
    elif selected_upgrade["type"] == "knockback":
        # 넉백 강화 (1회당 +10%, get_knockback_multiplier에서 반영)
        # 예전에는 levels["damage"]만 올라가고 넉백에는 아무 효과가 없었음
        player.levels["knockback"] = player.levels.get("knockback", 0) + 1
    elif selected_upgrade["type"] == "regen":
        player.regen += 0.3
        player.levels["regen"] += 1
    elif selected_upgrade["type"] == "regen_big":
        player.regen += 0.5
        player.levels["regen"] += 1
    elif selected_upgrade["type"] == "exp_boost":
        # 미래에 경험치 부스트 플래그 추가 가능
        player.levels["exp_boost"] = player.levels.get("exp_boost", 0) + 1
    elif selected_upgrade["type"] == "crit":
        player.levels["crit"] = min(16, player.levels.get("crit", 0) + 1)
    elif selected_upgrade["type"] == "dodge":
        player.levels["dodge"] = min(20, player.levels.get("dodge", 0) + 1)
    elif selected_upgrade["type"] == "attack_speed":
        # fire_rate는 클수록 빠름 (공격 간격 = 1000 / fire_rate / attack_speed ms)
        # 예전에는 0.95를 곱해서 오히려 공격이 5%씩 느려졌음
        player.weapon.fire_rate *= 1.05  # 5% 빠르게
    # 무기 타입별 근접 무기 데미지
    elif selected_upgrade["type"].startswith("melee_damage_"):
        weapon_name = selected_upgrade["type"].replace("melee_damage_", "")
        player.weapon.damage += selected_upgrade.get("value", 3)
        player.weapon_upgrades[weapon_name]["damage"] += 1
    # 무기 타입별 근접 무기 공격 속도
    # (예전에는 아무 곳에서도 쓰지 않는 값만 올라가서 효과가 없었음)
    elif selected_upgrade["type"].startswith("melee_skill_speed_"):
        weapon_name = selected_upgrade["type"].replace("melee_skill_speed_", "")
        speed_rate = MELEE_SPEED_UPGRADE_RATES.get(weapon_name, 0.08)
        if weapon_name == "spear":
            # 창: 관통 찌르기 투사체 속도 증가
            player.skill_upgrades["spear"]["speed"] += speed_rate
        else:
            player.weapon.attack_speed *= 1 + speed_rate
    elif selected_upgrade["type"] == "weapon_firerate":
        player.weapon.fire_rate *= 1.05  # 5% 빠르게
        # 근접 무기에는 "fire_rate" 항목이 없어서 KeyError가 나던 문제 방지
        weapon_upgrade_levels = player.weapon_upgrades[player.weapon.weapon_type]
        weapon_upgrade_levels["fire_rate"] = weapon_upgrade_levels.get("fire_rate", 0) + 1
    elif selected_upgrade["type"] == "weapon_damage":
        player.weapon.damage += selected_upgrade.get("value", 2)
        player.weapon_upgrades[player.weapon.weapon_type]["damage"] += 1

    # 스킬 적용
    elif selected_upgrade["type"] == "skill_infinity_ammo":
        player.skills["skill_infinity_ammo"] = True
        player.infinity_ammo_time = 30 * 60  # 30초
    elif selected_upgrade["type"] == "skill_piercing":
        # 레벨식 관통: 찍을 때마다 1마리씩 더 관통
        player.pierce_level = min(MAX_PIERCE_LEVEL, player.pierce_level + 1)
    elif selected_upgrade["type"] == "skill_fire_bullets":
        player.skills["skill_fire_bullets"] = True
    elif selected_upgrade["type"] == "skill_ice_bullets":
        player.skills["skill_ice_bullets"] = True
    elif selected_upgrade["type"] == "skill_electric_bullets":
        player.skills["skill_electric_bullets"] = True
    elif selected_upgrade["type"] == "skill_auto_aim":
        player.skills["skill_auto_aim"] = True
    elif selected_upgrade["type"] == "skill_shield":
        player.skills["skill_shield"] = True
        player.shield_active = True
    elif selected_upgrade["type"] == "skill_teleport":
        player.skills["skill_teleport"] = True
    elif selected_upgrade["type"] == "skill_slowdown":
        player.skills["skill_slowdown"] = True
    elif selected_upgrade["type"] == "skill_explosion":
        player.skills["skill_explosion"] = True

    # 스킬 쿨타임 감소
    elif selected_upgrade["type"] == "skill_cooldown_reduction":
        player.skill_cooldown_reduction = min(0.5, player.skill_cooldown_reduction + 0.05)  # 최대 50% 감소
    elif selected_upgrade["type"] == "skill_cooldown_reduction_big":
        player.skill_cooldown_reduction = min(0.5, player.skill_cooldown_reduction + 0.1)  # 최대 50% 감소

    # 무기별 스킬 업그레이드
    elif selected_upgrade["type"] == "melee_skill_range":
        player.skill_upgrades["melee"]["range"] += 12
    elif selected_upgrade["type"] == "katana_skill_strikes":
        player.skill_upgrades["katana"]["strikes"] += 1
    elif selected_upgrade["type"] == "katana_skill_ougi":
        player.skill_upgrades["katana"]["ougi"] = 1
    elif selected_upgrade["type"] == "katana_skill_chain":
        player.skill_upgrades["katana"]["chain"] = player.skill_upgrades["katana"].get("chain", 0) + 1
    elif selected_upgrade["type"] == "axe_skill_range":
        player.skill_upgrades["axe"]["range"] += 25
    elif selected_upgrade["type"] == "axe_skill_knockback":
        player.skill_upgrades["axe"]["knockback"] += 1  # 1회당 +12%
    elif selected_upgrade["type"] == "spear_skill_pierces":
        player.skill_upgrades["spear"]["pierces"] += 1
    elif selected_upgrade["type"] == "spear_skill_speed":
        player.skill_upgrades["spear"]["speed"] += MELEE_SPEED_UPGRADE_RATES["spear"]
    elif selected_upgrade["type"] == "hammer_skill_range":
        player.skill_upgrades["hammer"]["range"] += 20
    elif selected_upgrade["type"] == "hammer_skill_damage":
        player.skill_upgrades["hammer"]["damage"] += 1  # 1회당 +10%
    elif selected_upgrade["type"] == "gloves_skill_strikes":
        player.skill_upgrades["gloves"]["strikes"] += 1
    # 원거리 무기 업그레이드
    elif selected_upgrade["type"] == "glock_skill_burst":
        player.skill_upgrades["glock"]["burst"] += 1
    elif selected_upgrade["type"] == "shotgun_skill_pellets":
        player.skill_upgrades["shotgun"]["pellets"] += 1
    elif selected_upgrade["type"] == "shotgun_skill_damage":
        player.skill_upgrades["shotgun"]["damage"] += 1  # 1회당 +8%
    elif selected_upgrade["type"] == "sniper_skill_critdmg":
        player.skill_upgrades["sniper"]["crit_damage"] = player.skill_upgrades["sniper"].get("crit_damage", 0) + 1
    elif selected_upgrade["type"] == "sniper_skill_pierces":
        player.skill_upgrades["sniper"]["pierces"] += 1
    elif selected_upgrade["type"] == "machinegun_skill_burst":
        player.skill_upgrades["machinegun"]["burst"] += 2
    elif selected_upgrade["type"] == "plasma_skill_range":
        player.skill_upgrades["plasma"]["range"] += 15
    elif selected_upgrade["type"] == "plasma_skill_damage":
        player.skill_upgrades["plasma"]["damage"] += 1  # 1회당 +8%
    elif selected_upgrade["type"] == "rocket_skill_count":
        # "로켓 범위 +15px": 폭발 범위 증가 (예전에는 로켓 발사 수가 15발씩 늘어났음)
        player.skill_upgrades["rocket"]["explosion"] += 15
    elif selected_upgrade["type"] == "rocket_skill_damage":
        player.skill_upgrades["rocket"]["damage"] += 1  # 1회당 +5%


def get_upgrade_name(upgrade_type):
    """업그레이드 타입을 한국 이름으로 변환"""
    upgrade_names = {
        # 기본 업그레이드
        "health": "체력 +8",
        "health_big": "체력 +12",
        "heal": "체력 회복",
        "heal_full": "완전 회복",
        "speed": "이동속도 +0.3",
        "speed_big": "이동속도 +0.5",
        "base_damage": "공격력 +8%",
        "base_damage_big": "공격력 +15%",
        "knockback": "넉백 강화",
        "regen": "재생 +0.3",
        "regen_big": "재생 +0.5",
        "exp_boost": "경험치 +20%",
        "crit": "치명타",
        "dodge": "회피",
        "attack_speed": "공격 속도 +5%",
        "skill_cooldown_reduction": "스킬 쿨 -5%",
        "skill_cooldown_reduction_big": "스킬 쿨 -10%",
        # 스킬
        "skill_infinity_ammo": "무한탄약 (30초)",
        "skill_piercing": "투사체 관통 +1",
        "skill_fire_bullets": "화염탄",
        "skill_ice_bullets": "얼음탄",
        "skill_electric_bullets": "전기탄",
        "skill_auto_aim": "자동조준",
        "skill_shield": "방어막",
        "skill_teleport": "순간이동",
        "skill_slowdown": "시간감속",
        "skill_explosion": "폭발 공격",
        # 무기 기본 업그레이드
        "weapon_damage": "데미지 +",
        "weapon_firerate": "발사 속도 +",
        # 근접 무기 스킬
        "melee_skill_range": "홈런 범위 +12px",
        "melee_damage_melee": "나무 방망이 데미지 +4",
        "melee_skill_speed_melee": "나무 방망이 속도 +8%",
        "katana_skill_strikes": "일섬 거리 +40px",
        "katana_skill_chain": "연참 데미지 +3%",
        "katana_skill_ougi": "오의 연섬",
        "melee_damage_katana": "카타나 데미지 +3",
        "melee_skill_speed_katana": "카타나 속도 +12%",
        "axe_skill_range": "대회전 범위 +25px",
        "melee_damage_axe": "도끼 데미지 +8",
        "axe_skill_knockback": "대회전 넉백 +12%",
        "spear_skill_pierces": "물보라 범위 +30px",
        "melee_damage_spear": "창 데미지 +4",
        "melee_skill_speed_spear": "물보라 둔화 +8%",
        "hammer_skill_range": "대지 강타 범위 +20px",
        "melee_damage_hammer": "해머 데미지 +10",
        "hammer_skill_damage": "대지 강타 피해 +10%",
        "gloves_skill_strikes": "러시 시간 +0.5초",
        "melee_damage_gloves": "글로브 데미지 +2",
        "melee_skill_speed_gloves": "글로브 속도 +10%",
        # 원거리 무기 스킬
        "glock_skill_burst": "폭격 범위 증가",
        "shotgun_skill_pellets": "기본 발사 탄환 +1발",
        "shotgun_skill_damage": "화염 데미지 +8%",
        "sniper_skill_pierces": "도탄 +3회",
        "sniper_skill_critdmg": "치명타 데미지 +25%",
        "machinegun_skill_burst": "포탑 지속 +1초",
        "plasma_skill_range": "블랙홀 범위 +15px",
        "plasma_skill_damage": "블랙홀 데미지 +8%",
        "rocket_skill_count": "로켓 범위 +15px",
        "rocket_skill_damage": "폭격 데미지 +5%",
    }
    return upgrade_names.get(upgrade_type, upgrade_type)


def get_max_zombies(wave):
    """필드에 동시에 있을 수 있는 일반 등장 좀비 수 (웨이브마다 +2)"""
    return 5 + wave * 2


def get_spawn_interval(wave):
    """일반 좀비가 하나씩 나오는 간격(프레임): 웨이브가 오를수록 짧아짐 (최소 0.33초)"""
    return max(20, 60 - wave * 3)


def get_summon_count(base, wave, per_waves):
    """보스 소환 1회당 소환 수: 기본 수 + per_waves 웨이브마다 1마리씩 증가"""
    return base + wave // per_waves


def get_zombie_type_by_wave(wave):
    """웨이브에 따라 좀비 타입을 선택 (점진적으로 강한 좀비 추가)"""
    normal_types = ["normal", "spike", "armored", "heavy", "poison", "ice", "slime"]
    tank_types = ["tank", "knight", "shield", "stone", "iron", "wall", "howler"]
    fast_types = ["fast", "runner", "ninja", "spark", "wind", "shadow", "sniper_z"]
    bomber_types = ["bomber", "mine", "flame", "acid", "toxic", "nuclear"]
    boss_types = ["boss", "paladin", "demon", "angel", "dragon", "king", "god"]  # 기사단장 추가
    giant_types = ["colossus", "titan", "giant", "behemoth", "leviathan", "elder"]

    rand = random.random()

    # 웨이브별로 점진적으로 특수 좀비 추가
    if wave <= 3:
        # 웨이브 1-3: 일반 좀비만 (100%)
        return random.choice(normal_types)

    elif wave <= 5:
        # 웨이브 4-5: 일반 85% + 탱크/빠른 15%
        if rand < 0.85:
            return random.choice(normal_types)
        elif rand < 0.93:
            return random.choice(tank_types)
        else:
            return random.choice(fast_types)

    elif wave <= 7:
        # 웨이브 6-7: 일반 60% + 탱크 15% + 빠른 15% + 폭탄 10%
        if rand < 0.60:
            return random.choice(normal_types)
        elif rand < 0.75:
            return random.choice(tank_types)
        elif rand < 0.90:
            return random.choice(fast_types)
        else:
            return random.choice(bomber_types)

    elif wave <= 9:
        # 웨이브 8-9: 일반 40% + 탱크 15% + 빠른 15% + 폭탄 15% + 보스 15%
        if rand < 0.40:
            return random.choice(normal_types)
        elif rand < 0.55:
            return random.choice(tank_types)
        elif rand < 0.70:
            return random.choice(fast_types)
        elif rand < 0.85:
            return random.choice(bomber_types)
        else:
            return random.choice(boss_types)

    else:
        # 웨이브 10+: 모든 타입 (거대 제한)
        if rand < 0.25:
            return random.choice(normal_types)
        elif rand < 0.40:
            return random.choice(tank_types)
        elif rand < 0.55:
            return random.choice(fast_types)
        elif rand < 0.70:
            return random.choice(bomber_types)
        elif rand < 0.85:
            return random.choice(boss_types)
        else:
            return random.choice(giant_types)


# ===== 저장 / 이어하기 =====
# 저장 파일은 게임(실행 파일)과 같은 폴더에 만들어짐
SAVE_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
SAVE_PATH = os.path.join(SAVE_DIR, "zombie_save.json")
SAVE_VERSION = 1
# 저장하는 플레이어 정보 (능력치/업그레이드/스킬 상태)
PLAYER_SAVE_FIELDS = [
    "ability", "health", "max_health", "speed", "damage", "exp", "exp_to_level", "level", "regen",
    "levels", "skills", "pierce_level", "skill_upgrades", "weapon_upgrades", "obtained_upgrades",
    "shield_active", "skill_cooldown_reduction", "infinity_ammo_time", "teleport_cooldown_max",
]
WEAPON_SAVE_FIELDS = ["weapon_type", "damage", "fire_rate", "attack_speed"]


def save_game(player, score, wave, wave_elapsed_ms):
    """현재 진행 상황 저장 (좀비 배치는 저장하지 않고, 이어하면 새로 나옴)"""
    data = {
        "version": SAVE_VERSION,
        "player": {field: getattr(player, field) for field in PLAYER_SAVE_FIELDS},
        "weapon": {field: getattr(player.weapon, field) for field in WEAPON_SAVE_FIELDS},
        "score": score,
        "wave": wave,
        "wave_elapsed_ms": max(0, int(wave_elapsed_ms)),
    }
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        return True
    except OSError:
        return False


def load_save():
    """저장 파일 읽기 (없거나 깨졌으면 None)"""
    try:
        with open(SAVE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("version") != SAVE_VERSION or data["weapon"]["weapon_type"] not in WEAPON_STATS:
            return None
        return data
    except (OSError, ValueError, KeyError, TypeError):
        return None


def delete_save():
    try:
        os.remove(SAVE_PATH)
    except OSError:
        pass


def show_continue_menu(data):
    """저장된 게임이 있으면 이어하기 / 새 게임 선택"""
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    weapon_type = data["weapon"]["weapon_type"]
    chips = [("무기", WEAPON_STATS[weapon_type]["name"]), ("레벨", data["player"]["level"]),
             ("웨이브", data["wave"]), ("점수", data["score"])]
    buttons = [("continue", "이어하기", "저장한 곳부터 계속", (128, 196, 132)),
               ("new", "새 게임", "저장을 지우고 처음부터", (228, 92, 78))]
    btn_w, btn_h = 380, 80
    while True:
        ui_background(screen)
        top = ui_title(screen, "저장된 게임이 있습니다", SCREEN_HEIGHT // 2 - 230)
        chip_w, gap = 150, 12
        x = SCREEN_WIDTH // 2 - (len(chips) * chip_w + (len(chips) - 1) * gap) // 2
        for label, value in chips:
            rect = ui_panel(screen, (x, top + 26, chip_w, 64), alpha=220, radius=10)
            ui_text(screen, label, font_tiny, UI_SUB, (rect.centerx, rect.y + 6), "midtop", shadow=False)
            ui_text(screen, value, font_hud, UI_TEXT, (rect.centerx, rect.y + 28), "midtop", shadow=False)
            x += chip_w + gap
        mouse_pos = pygame.mouse.get_pos()
        rects = []
        for i, (kind, name, desc, color) in enumerate(buttons):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, top + 130 + i * (btn_h + 18), btn_w, btn_h)
            rects.append((kind, rect))
            ui_button(screen, rect, name, color, rect.collidepoint(mouse_pos), desc)
        for event in pygame.event.get():
            ui_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for kind, rect in rects:
                    if rect.collidepoint(event.pos):
                        return kind
        pygame.display.flip()
        clock.tick(60)


def main():
    # 저장된 게임이 있으면 이어하기 / 새 게임 선택
    save_data = load_save()
    if save_data is not None and show_continue_menu(save_data) != "continue":
        save_data = None
    delete_save()  # 불러온 저장(또는 버린 저장)은 지움 - 다시 저장하려면 '저장하고 나가기'

    if save_data is not None:
        # 이어하기: 저장한 능력치/무기/업그레이드 그대로 복원
        saved_player = save_data["player"]
        player = Player(0, 0, saved_player["ability"])
        player.weapon = Weapon(save_data["weapon"]["weapon_type"])
        for field, value in saved_player.items():
            if field in PLAYER_SAVE_FIELDS:
                setattr(player, field, value)
        for field, value in save_data["weapon"].items():
            setattr(player.weapon, field, value)
    else:
        # 능력 선택
        selected_ability = select_ability()

        # 무기 선택
        selected_weapon = select_weapon()

        # 플레이어를 원점에 생성
        player = Player(0, 0, selected_ability)
        player.weapon = Weapon(selected_weapon)
        # 공격형 능력: "데미지 +60%"가 실제 무기 공격력에 반영되도록 (예전에는 거의 쓰이지 않는 player.damage만 올랐음)
        if selected_ability == "damage":
            player.weapon.damage *= 1.6
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    zombies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    items = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    # 초기 좀비 생성 (플레이어로부터 거리 계산)
    for _ in range(5):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(300, 800)
        x = player.rect.centerx + math.cos(angle) * distance
        y = player.rect.centery + math.sin(angle) * distance
        zombie = Zombie(x, y)
        zombies.add(zombie)
        all_sprites.add(zombie)

    score = 0
    wave = 1
    fx.reset()  # 이전 게임의 파티클/글자/흔들림 정리
    last_player_health = player.health  # 피격 연출용
    wave_timer_start = pygame.time.get_ticks()  # 웨이브 타이머 시작
    if save_data is not None:
        # 이어하기: 점수/웨이브/웨이브 진행 시간 복원
        score = save_data["score"]
        wave = save_data["wave"]
        wave_timer_start -= save_data["wave_elapsed_ms"]
        fx.add_text(player.rect.centerx, player.rect.top - 30, "이어하기!", (120, 255, 120), big=True, life=80)
    wave_interval = 60000  # 60초 (밀리초)
    zombie_spawn_counter = 0
    max_zombies = get_max_zombies(wave)  # 소환 로직이 먼저 참조하므로 루프 전에 초기화
    game_over = False
    game_over_time = 0
    show_stack = False  # 업그레이드 스택 표시 여부

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # 마우스 클릭으로 총알 발사 (왼쪽 클릭) 또는 우클릭 스킬
                mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
                mouse_world_x = mouse_screen_x + camera.x
                mouse_world_y = mouse_screen_y + camera.y

                if player.skills.get("skill_auto_aim", False):
                    auto_target = get_auto_aim_target(player, zombies, 600)
                    if auto_target:
                        mouse_world_x, mouse_world_y = auto_target

                if event.button == 1:  # 왼쪽 클릭 - 무기 발사
                    # 무기 발사
                    can_fire = player.shock_time <= 0 and player.weapon.fire()
                    if player.skills.get("skill_infinity_ammo", False) and player.infinity_ammo_time > 0 and player.shock_time <= 0:
                        can_fire = True
                        player.weapon.last_shot_time = pygame.time.get_ticks()
                    if can_fire:
                        if player.weapon.weapon_type in MELEE_WEAPONS:
                            # 근접 무기 - 범위 공격
                            dx = mouse_world_x - player.rect.centerx
                            dy = mouse_world_y - player.rect.centery
                            distance = math.sqrt(dx**2 + dy**2)
                            if distance > 0:
                                direction_x = dx / distance
                                direction_y = dy / distance
                            else:
                                direction_x = player.last_direction_x
                                direction_y = player.last_direction_y

                            # 근접 무기 전용 데미지 강화는 weapon.damage에 이미 더해지므로 추가 배율은 없음
                            # (예전에는 "+4"에 더해 강화 1회당 +30% 배율까지 중복 적용돼서 근접만 과도하게 강해졌음)
                            melee_damage = get_weapon_damage(player)
                            melee = Melee(player.rect.centerx, player.rect.centery, direction_x, direction_y, melee_damage, player.weapon.weapon_type, owner=player)
                            bullets.add(melee)
                            all_sprites.add(melee)

                            # 범위 내의 모든 좀비에 즉시 데미지 적용
                            melee_hit = False
                            first_hit_zombie, first_hit_distance = None, 0
                            knockback_mult = get_knockback_multiplier(player)
                            for zombie in zombies:
                                if zombie.health <= 0:
                                    continue
                                distance_to_zombie = math.sqrt(
                                    (zombie.rect.centerx - player.rect.centerx)**2 +
                                    (zombie.rect.centery - player.rect.centery)**2
                                )
                                # 조준 방향 부채꼴 안 (또는 몸에 붙은 좀비)만 맞음 - 화면에 그려지는 범위와 같음
                                in_range = distance_to_zombie < Melee.CLOSE_HIT_RADIUS
                                if not in_range and distance_to_zombie < melee.attack_range:
                                    zombie_angle = math.degrees(math.atan2(-(zombie.rect.centery - player.rect.centery),
                                                                           zombie.rect.centerx - player.rect.centerx))
                                    angle_diff = abs((zombie_angle - melee.base_angle + 180) % 360 - 180)
                                    in_range = angle_diff <= melee.hit_half_arc
                                if in_range:
                                    if not melee_hit or distance_to_zombie < first_hit_distance:
                                        first_hit_zombie, first_hit_distance = zombie, distance_to_zombie
                                    melee_hit = True
                                    melee.has_hit.add(zombie)   # 휘두르는 동안 다시 맞지 않게
                                    # 갑옷/방패 감소 적용 (예전에는 근접 기본 공격만 감소를 무시했음)
                                    zombie.health -= roll_crit_damage(player, melee_damage, zombie) * get_damage_multiplier(zombie)
                                    fx.hit_spark(zombie.rect.centerx, zombie.rect.centery, FX_WEAPON_COLORS.get(player.weapon.weapon_type, WHITE))

                                    if player.skills.get("skill_fire_bullets", False):
                                        zombie.burn_time = max(zombie.burn_time, 180)
                                        zombie.burn_damage_cooldown = 0
                                        fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "fire")
                                    if player.skills.get("skill_ice_bullets", False):
                                        zombie.slow_time = max(zombie.slow_time, 120)
                                        zombie.slow_multiplier = min(zombie.slow_multiplier, 0.6)
                                        fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "ice")
                                    if player.skills.get("skill_electric_bullets", False):
                                        zombie.electric_fx = 30
                                        chain_targets = []
                                        for other_zombie in list(zombies):
                                            if other_zombie is zombie or other_zombie not in zombies:
                                                continue
                                            dx = other_zombie.rect.centerx - zombie.rect.centerx
                                            dy = other_zombie.rect.centery - zombie.rect.centery
                                            dist = math.sqrt(dx * dx + dy * dy)
                                            if dist < 150:
                                                chain_targets.append((dist, other_zombie))
                                        chain_targets.sort(key=lambda entry: entry[0])
                                        for _, target in chain_targets[:2]:
                                            damage_multiplier = get_damage_multiplier(target)
                                            target.health -= melee_damage * 0.4 * damage_multiplier
                                            fx.lightning(zombie.rect.centerx, zombie.rect.centery, target.rect.centerx, target.rect.centery)
                                            fx.element_hit(target.rect.centerx, target.rect.centery, "electric")
                                            target.electric_fx = 30

                                    # 넉백 적용
                                    zombie_dx = zombie.rect.centerx - player.rect.centerx
                                    zombie_dy = zombie.rect.centery - player.rect.centery
                                    zombie_dist = math.sqrt(zombie_dx**2 + zombie_dy**2)

                                    if zombie_dist > 0:
                                        knockback_vel_x = (zombie_dx / zombie_dist) * melee.knockback_power / 100 * knockback_mult
                                        knockback_vel_y = (zombie_dy / zombie_dist) * melee.knockback_power / 100 * knockback_mult
                                        zombie.knockback_vel_x = knockback_vel_x
                                        zombie.knockback_vel_y = knockback_vel_y
                                    # 사망 처리(점수/경험치/사망 효과)는 아래 "좀비 죽음 처리"에서 한 번에 함

                            if melee_hit and player.skills.get("skill_explosion", False) and player.explosion_cooldown <= 0:
                                player.explosion_cooldown = EXPLOSION_SKILL_COOLDOWN
                                explosion_radius = 80
                                # 플레이어 주변이 아니라 가장 가까이 맞은 좀비 위치에서 폭발
                                boom_x, boom_y = first_hit_zombie.rect.center
                                explosion = Explosion(boom_x, boom_y, explosion_radius)
                                explosions.add(explosion)
                                all_sprites.add(explosion)

                                for other_zombie in list(zombies):
                                    if other_zombie not in zombies or other_zombie is first_hit_zombie:
                                        continue
                                    dist = math.sqrt((other_zombie.rect.centerx - boom_x)**2 +
                                                   (other_zombie.rect.centery - boom_y)**2)
                                    if dist < explosion_radius:
                                        damage_multiplier = get_damage_multiplier(other_zombie)
                                        other_zombie.health -= melee_damage * EXPLOSION_SKILL_RATIO_MELEE * damage_multiplier

                        elif player.weapon.weapon_type == "shotgun":
                            # 여러 방향으로 발사 (pellets 개수만큼)
                            pellets_count = 3 + player.skill_upgrades["shotgun"]["pellets"]
                            spread_angle = 0.6 / (pellets_count - 1) if pellets_count > 1 else 0
                            for i in range(pellets_count):
                                angle_offset = -0.3 + i * spread_angle if pellets_count > 1 else 0
                                dx = mouse_world_x - player.rect.centerx
                                dy = mouse_world_y - player.rect.centery
                                angle = math.atan2(dy, dx) + angle_offset
                                target_x = player.rect.centerx + math.cos(angle) * 500
                                target_y = player.rect.centery + math.sin(angle) * 500
                                bullet = Bullet(player.rect.centerx, player.rect.centery, target_x, target_y, get_weapon_damage(player), "shotgun", "shotgun")
                                bullet.speed = player.weapon.bullet_speed
                                bullet.max_range = player.weapon.max_range  # 근거리 전용
                                bullets.add(bullet)
                                all_sprites.add(bullet)
                            fire_muzzle_flash(player, mouse_world_x, mouse_world_y, kick=2.5)

                        elif player.weapon.weapon_type == "rocket":
                            rocket = Bullet(player.rect.centerx, player.rect.centery, mouse_world_x, mouse_world_y, get_weapon_damage(player), "rocket", "rocket")
                            rocket.speed = player.weapon.bullet_speed
                            bullets.add(rocket)
                            all_sprites.add(rocket)
                            fire_muzzle_flash(player, mouse_world_x, mouse_world_y, kick=3.0)

                        else:
                            # 일반 총알 (글록, 저격총, 기관총, 플라즈마)
                            bullet_type = "plasma" if player.weapon.weapon_type == "plasma" else "normal"
                            bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_world_x, mouse_world_y, get_weapon_damage(player), bullet_type, player.weapon.weapon_type)
                            bullet.speed = player.weapon.bullet_speed
                            bullet.pierce = player.weapon.pierce              # 저격총: 기본 2마리 관통
                            bullet.splash_radius = player.weapon.splash_radius  # 플라즈마: 착탄 폭발
                            bullet.splash_ratio = player.weapon.splash_ratio
                            bullet.max_range = player.weapon.max_range
                            bullets.add(bullet)
                            all_sprites.add(bullet)
                            fire_muzzle_flash(player, mouse_world_x, mouse_world_y,
                                              kick=2.0 if player.weapon.weapon_type == "sniper" else 0)

                elif event.button == 3:  # 우클릭 - 무기 스킬
                    execute_weapon_skill(player.weapon.weapon_type, player, mouse_world_x, mouse_world_y,
                                       zombies, bullets, all_sprites, explosions)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB and not game_over:
                    # TAB 키로 업그레이드 스택 토글
                    show_stack = not show_stack
                elif event.key == pygame.K_e and not game_over:
                    if player.skills.get("skill_teleport", False) and player.teleport_cooldown <= 0:
                        mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
                        player.rect.centerx = mouse_screen_x + camera.x
                        player.rect.centery = mouse_screen_y + camera.y
                        player.teleport_cooldown = player.teleport_cooldown_max
                elif event.key == pygame.K_SPACE:
                    if game_over:
                        return "restart"  # 게임 재시작 (main()을 재귀 호출하지 않고 바깥 루프에서 다시 시작)
                elif event.key == pygame.K_ESCAPE:
                    if not game_over:
                        # 게임 재생 중이면 일시정지 메뉴 표시
                        pause_start = pygame.time.get_ticks()
                        pause_result = show_pause_menu(player)
                        if pause_result == "exit":
                            return "restart"  # 나가기: 능력 선택 화면부터 다시 시작
                        if pause_result == "save_exit":
                            # 저장하고 게임 종료 (메뉴를 보는 동안 흐른 시간은 웨이브 진행에 넣지 않음)
                            save_game(player, score, wave, pause_start - wave_timer_start)
                            return "quit"
                        # 일시정지 동안 웨이브 타이머/스킬 쿨타임이 흐르지 않도록 보정
                        paused_ms = pygame.time.get_ticks() - pause_start
                        wave_timer_start += paused_ms
                        compensate_paused_time(player, paused_ms)
                    else:
                        # 게임 오버 화면에서는 ESC로 종료
                        running = False

        if not game_over:
            # 플레이어 이동
            player.update()

            # 카메라 업데이트 (플레이어가 움직인 뒤에 맞춰야 화면이 한 프레임 늦게 따라오지 않음)
            camera.update(player.rect.centerx, player.rect.centery)

            if player.skills.get("skill_infinity_ammo", False) and player.infinity_ammo_time > 0:
                player.infinity_ammo_time -= 1
                if player.infinity_ammo_time <= 0:
                    player.skills["skill_infinity_ammo"] = False

            if player.teleport_cooldown > 0:
                player.teleport_cooldown -= 1

            if player.explosion_cooldown > 0:
                player.explosion_cooldown -= 1
            if player.shock_time > 0:
                player.shock_time -= 1
                if fx.frame % 4 == 0:  # 감전 불꽃
                    fx.burst(player.rect.centerx, player.rect.centery, (255, 240, 90), 2,
                             speed=(1.5, 3.5), size=(1.5, 2.5), life=(5, 10), drag=0.8)
            if player.corrode_time > 0:
                player.corrode_time -= 1
            if player.invuln_time > 0:
                player.invuln_time -= 1
            tick_katana_chain(player)

            # 글로브 러시
            if player.rush_time > 0:
                player.rush_time -= 1
                player.weapon.rush_mult = 3.0
                if fx.frame % 3 == 0:
                    fx.burst(player.rect.centerx, player.rect.centery, (255, 160, 200), 2,
                             speed=(1.5, 3.5), size=(2, 3), life=(8, 14), drag=0.85)
            else:
                player.weapon.rush_mult = 1.0

            # 아이템 버프 시간 감소
            if player.damage_buff_time > 0:
                player.damage_buff_time -= 1
            if player.speed_buff_time > 0:
                player.speed_buff_time -= 1

            # 재생 능력 적용
            if player.regen > 0:
                player.health = min(player.health + player.regen / 60, player.max_health)

            # 경험치 확인 및 레벨업
            levels_gained = 0
            while player.exp >= player.exp_to_level:
                player.exp -= player.exp_to_level
                player.level += 1
                player.exp_to_level = int(100 * (1.1 ** player.level))
                levels_gained += 1

            # 오른 레벨 수만큼 업그레이드 메뉴 표시 (한 번에 여러 레벨이 올라도 보상이 누락되지 않음)
            if levels_gained > 0:
                fx.ring(player.rect.centerx, player.rect.centery, (255, 230, 90), 140, count=36, size=4)
                fx.add_text(player.rect.centerx, player.rect.top - 30, "LEVEL UP!", (255, 230, 90), big=True, life=70)
            for _ in range(levels_gained):
                menu_start = pygame.time.get_ticks()
                selected_upgrade = show_upgrade_menu(player, camera)
                # 메뉴를 보는 동안 웨이브 타이머/스킬 쿨타임이 흐르지 않도록 보정
                paused_ms = pygame.time.get_ticks() - menu_start
                wave_timer_start += paused_ms
                compensate_paused_time(player, paused_ms)

                # 선택된 업그레이드 적용
                if selected_upgrade:
                    apply_upgrade(player, selected_upgrade)

            # 기관총 연발 처리 (마우스 꾹 누르고 있을 때)
            if not game_over:
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:  # 왼쪽 마우스 버튼 누르고 있음
                    if player.weapon.weapon_type == "machinegun":
                        # 기관총 연발
                        mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
                        mouse_world_x = mouse_screen_x + camera.x
                        mouse_world_y = mouse_screen_y + camera.y

                        if player.skills.get("skill_auto_aim", False):
                            auto_target = get_auto_aim_target(player, zombies, 600)
                            if auto_target:
                                mouse_world_x, mouse_world_y = auto_target

                        # 무기의 fire() 메서드로 발사 가능 여부 확인
                        can_fire = player.shock_time <= 0 and player.weapon.fire()
                        if player.skills.get("skill_infinity_ammo", False) and player.infinity_ammo_time > 0 and player.shock_time <= 0:
                            can_fire = True
                            player.weapon.last_shot_time = pygame.time.get_ticks()
                        if can_fire:
                            bullet_type = "normal"
                            bullet = Bullet(player.rect.centerx, player.rect.centery, mouse_world_x, mouse_world_y, get_weapon_damage(player), bullet_type, "machinegun")
                            bullet.speed = player.weapon.bullet_speed
                            bullets.add(bullet)
                            all_sprites.add(bullet)
                            fire_muzzle_flash(player, mouse_world_x, mouse_world_y)

            if player.skills.get("skill_slowdown", False):
                for zombie in zombies:
                    dx = zombie.rect.centerx - player.rect.centerx
                    dy = zombie.rect.centery - player.rect.centery
                    if dx * dx + dy * dy < 250 * 250:
                        zombie.slow_time = max(zombie.slow_time, 30)
                        zombie.slow_multiplier = min(zombie.slow_multiplier, 0.6)

            # 좀비 이동
            for zombie in zombies:
                zombie.update(player, bullets, all_sprites, explosions)
            spear_charge(player, zombies)   # 창을 들고 달리면 정면 좀비에게 피해 + 넉백

            # 오라 능력 (매 프레임 다시 계산)
            #  - 벽좀비 / 수호의 천사: 주변 좀비가 받는 피해 감소
            #  - 질풍의 천사: 주변 좀비 이동속도 +30%
            #  - 엘더 / 치유의 천사: 주기적으로 주변 좀비 회복
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

            # 지속형 스킬 (대회전 베기 / 항공 폭격 / 포탑 / 블랙홀 / 미사일 폭격)
            for skill in list(player.active_skills):
                if not skill.update(player, zombies, bullets, all_sprites, explosions):
                    player.active_skills.remove(skill)

            # 플레이어에게서 너무 멀어진 좀비(느린 거대 좀비 등)는 플레이어 근처로 다시 데려옴
            # (예전에는 멀리 남겨진 좀비가 최대 좀비 수를 차지해서 새 좀비가 더 이상 나오지 않았음)
            for zombie in zombies:
                dx = zombie.rect.centerx - player.rect.centerx
                dy = zombie.rect.centery - player.rect.centery
                if dx * dx + dy * dy > ZOMBIE_LEASH_DISTANCE * ZOMBIE_LEASH_DISTANCE:
                    angle = random.uniform(0, 2 * math.pi)
                    zombie.rect.center = (round(player.rect.centerx + math.cos(angle) * ZOMBIE_RESPAWN_DISTANCE),
                                          round(player.rect.centery + math.sin(angle) * ZOMBIE_RESPAWN_DISTANCE))

            # 악마 좀비 임프 소환
            for zombie in list(zombies):
                if zombie.zombie_type == "demon" and zombie in zombies:
                    if hasattr(zombie, 'imp_spawn_cooldown') and len(zombies) < max_zombies + 3:
                        zombie.imp_spawn_cooldown += 1
                        if zombie.imp_spawn_cooldown >= zombie.imp_spawn_interval:
                            # 임프 소환 (웨이브가 오를수록 한 번에 더 많이: 1 + 4웨이브마다 1마리)
                            for _ in range(get_summon_count(1, wave, 4)):
                                imp_angle = random.uniform(0, 2 * math.pi)
                                imp_x = zombie.rect.centerx + math.cos(imp_angle) * zombie.imp_spawn_radius
                                imp_y = zombie.rect.centery + math.sin(imp_angle) * zombie.imp_spawn_radius

                                imp = Zombie(imp_x, imp_y, zombie_type="imp", wave=wave, parent_zombie=zombie)
                                zombies.add(imp)
                                all_sprites.add(imp)

                                # 소환 이펙트
                                try:
                                    spawn_effect = SpawnEffect(imp_x, imp_y, (200, 50, 100), 300)
                                    all_sprites.add(spawn_effect)
                                except:
                                    pass

                            zombie.imp_spawn_cooldown = 0

                # 보스 갱스터 소환
                elif zombie.zombie_type == "boss" and zombie in zombies:
                    if hasattr(zombie, 'gangster_spawn_cooldown') and len(zombies) < max_zombies + 5:
                        zombie.gangster_spawn_cooldown += 1
                        if zombie.gangster_spawn_cooldown >= zombie.gangster_spawn_interval:
                            # 갱스터 대량 소환
                            # 웨이브가 오를수록 한 번에 더 많이 (2 + 4웨이브마다 1마리)
                            for _ in range(get_summon_count(zombie.gangster_spawn_count, wave, 4)):
                                gangster_angle = random.uniform(0, 2 * math.pi)
                                gangster_x = zombie.rect.centerx + math.cos(gangster_angle) * zombie.gangster_spawn_radius
                                gangster_y = zombie.rect.centery + math.sin(gangster_angle) * zombie.gangster_spawn_radius

                                gangster = Zombie(gangster_x, gangster_y, zombie_type="gangster", wave=wave, parent_zombie=zombie)
                                zombies.add(gangster)
                                all_sprites.add(gangster)

                                # 소환 이펙트
                                try:
                                    spawn_effect = SpawnEffect(gangster_x, gangster_y, (100, 100, 100), 300)
                                    all_sprites.add(spawn_effect)
                                except:
                                    pass

                            zombie.gangster_spawn_cooldown = 0

                # 기사단장 기사 소환
                elif zombie.zombie_type == "paladin" and zombie in zombies:
                    if hasattr(zombie, 'knight_spawn_cooldown') and len(zombies) < max_zombies + 5:
                        zombie.knight_spawn_cooldown += 1
                        if zombie.knight_spawn_cooldown >= zombie.knight_spawn_interval:
                            # 기사 소환 (웨이브가 오를수록 한 번에 더 많이: 1 + 6웨이브마다 1마리)
                            for _ in range(get_summon_count(1, wave, 6)):
                                knight_angle = random.uniform(0, 2 * math.pi)
                                knight_x = zombie.rect.centerx + math.cos(knight_angle) * zombie.knight_spawn_radius
                                knight_y = zombie.rect.centery + math.sin(knight_angle) * zombie.knight_spawn_radius

                                knight = Zombie(knight_x, knight_y, zombie_type="knight", wave=wave, parent_zombie=zombie)
                                zombies.add(knight)
                                all_sprites.add(knight)

                                # 소환 이펙트
                                try:
                                    spawn_effect = SpawnEffect(knight_x, knight_y, (150, 150, 200), 300)
                                    all_sprites.add(spawn_effect)
                                except:
                                    pass

                            zombie.knight_spawn_cooldown = 0

                # 신 천사 소환
                elif zombie.zombie_type == "god" and zombie in zombies:
                    if hasattr(zombie, 'apostle_spawn_cooldown') and len(zombies) < max_zombies + 10:
                        zombie.apostle_spawn_cooldown += 1
                        if zombie.apostle_spawn_cooldown >= zombie.apostle_spawn_interval:
                            # 12사도 12명 동시 소환
                            apostle_names = ["베드로", "안드레아", "야고보", "요한", "빌립", "바르톨로메오",
                                            "도마", "마태오", "야고보", "다대오", "시몬", "맛디아"]

                            for i, apostle_name in enumerate(apostle_names):
                                angle = (i / 12) * 2 * math.pi
                                apostle_x = zombie.rect.centerx + math.cos(angle) * 150
                                apostle_y = zombie.rect.centery + math.sin(angle) * 150

                                # 12사도 생성 (천사 능력치)
                                apostle = Zombie(apostle_x, apostle_y, zombie_type="apostle", wave=wave, parent_zombie=zombie)
                                apostle.custom_name = apostle_name

                                zombies.add(apostle)
                                all_sprites.add(apostle)

                                # 소환 이펙트
                                try:
                                    spawn_effect = SpawnEffect(apostle_x, apostle_y, (255, 255, 200), 200)
                                    all_sprites.add(spawn_effect)
                                except:
                                    pass

                            # 12천사 동시 소환 (각자 다른 능력, 사도보다 바깥쪽 원)
                            for i in range(len(ANGEL_ROLES)):
                                angle = (i + 0.5) / len(ANGEL_ROLES) * 2 * math.pi
                                angel_x = zombie.rect.centerx + math.cos(angle) * 260
                                angel_y = zombie.rect.centery + math.sin(angle) * 260
                                angel = make_role_angel(angel_x, angel_y, i, wave, zombie)
                                zombies.add(angel)
                                all_sprites.add(angel)
                                all_sprites.add(SpawnEffect(angel_x, angel_y, ANGEL_ROLES[i][2], 300))

                            zombie.apostle_spawn_cooldown = 0

                # 왕 일반 좀비 대량 소환
                elif zombie.zombie_type == "king" and zombie in zombies:
                    if hasattr(zombie, 'minion_spawn_cooldown') and len(zombies) < max_zombies + 10:
                        zombie.minion_spawn_cooldown += 1
                        if zombie.minion_spawn_cooldown >= zombie.minion_spawn_interval:
                            # 일반 좀비 대량 소환
                            # 웨이브가 오를수록 한 번에 더 많이 (3 + 3웨이브마다 1마리)
                            for _ in range(get_summon_count(zombie.minion_spawn_count, wave, 3)):
                                minion_angle = random.uniform(0, 2 * math.pi)
                                minion_x = zombie.rect.centerx + math.cos(minion_angle) * zombie.minion_spawn_radius
                                minion_y = zombie.rect.centery + math.sin(minion_angle) * zombie.minion_spawn_radius

                                minion = Zombie(minion_x, minion_y, zombie_type="normal", wave=wave, parent_zombie=zombie)
                                zombies.add(minion)
                                all_sprites.add(minion)

                                # 소환 이펙트
                                try:
                                    spawn_effect = SpawnEffect(minion_x, minion_y, (200, 0, 0), 300)
                                    all_sprites.add(spawn_effect)
                                except:
                                    pass

                            zombie.minion_spawn_cooldown = 0

            # 그룹별 업데이트 (중복 업데이트 방지)
            bullets.update()
            for melee_attack in [b for b in bullets if isinstance(b, Melee)]:
                melee_sweep(melee_attack, zombies)   # 휘두르는 도중 들어온 좀비도 맞음
            items.update()
            explosions.update()

            # 그룹에 속하지 않는 보조 이펙트만 업데이트
            for sprite in all_sprites:
                if sprite == player or isinstance(sprite, Zombie):
                    continue
                if sprite in bullets or sprite in items or sprite in explosions:
                    continue
                sprite.update()

            # 총알-좀비 충돌
            # (사망 처리는 아래 "좀비 죽음 처리"에서 한 번에 하므로, 여기서는 체력만 깎음)
            for zombie in list(zombies):
                if zombie not in zombies or zombie.health <= 0:  # 이미 죽은 좀비는 스킵
                    continue

                hit_bullets = pygame.sprite.spritecollide(zombie, bullets, False)
                for bullet in hit_bullets:
                    if zombie.health <= 0:  # 총알 여러 개가 동시에 맞은 경우, 죽은 뒤 남은 총알은 아낌
                        break

                    # 특수 투사체들은 무시 (따로 처리됨)
                    if isinstance(bullet, (SpikeProjectile, IceProjectile, NinjaProjectile, PoisonPool, WindBlastEffect, FlameExplosionEffect)):
                        continue
                    # 좀비(갱스터/용)가 쏜 총알은 좀비에게 맞지 않음
                    # (예전에는 쏘자마자 쏜 좀비 자신에게 맞고 사라져서 플레이어에게 한 번도 닿지 않았음)
                    if isinstance(bullet, Bullet) and bullet.is_enemy:
                        continue

                    # 데미지 감소 처리 (갑옷, 방패 등)
                    damage_multiplier = get_damage_multiplier(zombie)

                    # 적 총알은 위에서 걸렀으므로 남은 Bullet은 모두 플레이어 총알
                    # (예전에는 무기 이름 목록으로 판별해서 글로브 스킬/글록 스킬 총알이 빠져 있었음)
                    is_player_bullet = isinstance(bullet, Bullet)
                    if is_player_bullet and (zombie in bullet.hit_targets or zombie in bullet.dodged):
                        continue  # 이미 맞혔거나 회피한 좀비는 다시 맞지 않음
                    # 그림자좀비: 총알을 25% 확률로 회피
                    if (is_player_bullet and zombie.zombie_type == "shadow" and bullet.bullet_type != "rocket"
                            and random.random() < 0.25):
                        bullet.dodged.add(zombie)
                        fx.add_text(zombie.rect.centerx, zombie.rect.top - 8, "회피", (180, 140, 255))
                        continue

                    if isinstance(bullet, Melee):
                        # Melee는 이미 범위 공격으로 처리되었으므로 sprite collision 무시
                        continue

                    elif isinstance(bullet, Laser):
                        zombie.health -= (bullet.damage if hasattr(bullet, 'damage') else player.damage * 2) * damage_multiplier
                        bullet.kill()
                    elif hasattr(bullet, 'bullet_type') and bullet.bullet_type == "rocket":
                        zombie.health -= roll_crit_damage(player, bullet.damage, zombie) * damage_multiplier
                        bullet.kill()
                        fx.hit_spark(bullet.rect.centerx, bullet.rect.centery, FX_WEAPON_COLORS["rocket"])

                        # 로켓 폭발 생성 (기준표 폭발 반경 + "로켓 범위 +15px" 업그레이드)
                        rocket_radius = WEAPON_STATS["rocket"]["splash_radius"] + player.skill_upgrades["rocket"]["explosion"]
                        rocket_splash_ratio = WEAPON_STATS["rocket"]["splash_ratio"]
                        rocket_knockback_mult = get_knockback_multiplier(player)
                        explosion = Explosion(bullet.rect.centerx, bullet.rect.centery, rocket_radius)
                        explosions.add(explosion)
                        all_sprites.add(explosion)

                        # 폭발 범위 내 좀비에 피해 + 넉백
                        for other_zombie in list(zombies):
                            if other_zombie not in zombies:  # 이미 제거됨
                                continue

                            # 다른 좀비도 armor 체크
                            other_damage_mult = get_damage_multiplier(other_zombie)

                            dist = math.sqrt((other_zombie.rect.centerx - bullet.rect.centerx)**2 +
                                           (other_zombie.rect.centery - bullet.rect.centery)**2)
                            if dist < rocket_radius:
                                # 직격당한 좀비는 위에서 이미 피해를 받았으므로 폭발 피해는 주변 좀비에게만
                                # (예전에는 직격 대상이 직격 + 폭발 70%를 중복으로 받았음)
                                if other_zombie is not zombie:
                                    other_zombie.health -= bullet.damage * rocket_splash_ratio * other_damage_mult

                                # 폭발로 인한 넉백
                                dx = other_zombie.rect.centerx - bullet.rect.centerx
                                dy = other_zombie.rect.centery - bullet.rect.centery
                                if dist > 0:
                                    knockback_vel_x = (dx / dist) * 500 / 100 * rocket_knockback_mult
                                    knockback_vel_y = (dy / dist) * 500 / 100 * rocket_knockback_mult
                                    other_zombie.knockback_vel_x = knockback_vel_x
                                    other_zombie.knockback_vel_y = knockback_vel_y
                    else:
                        zombie.health -= roll_crit_damage(player, bullet.damage, zombie) * damage_multiplier
                        fx.hit_spark(bullet.rect.centerx, bullet.rect.centery, FX_WEAPON_COLORS.get(bullet.weapon_type, YELLOW))

                        # 착탄 폭발 (플라즈마): 맞은 좀비 주변에 폭발 피해
                        if is_player_bullet and bullet.splash_radius > 0:
                            splash = Explosion(bullet.rect.centerx, bullet.rect.centery, bullet.splash_radius)
                            explosions.add(splash)
                            all_sprites.add(splash)
                            for other_zombie in list(zombies):
                                if other_zombie is zombie or other_zombie.health <= 0:
                                    continue
                                dist = math.hypot(other_zombie.rect.centerx - bullet.rect.centerx,
                                                  other_zombie.rect.centery - bullet.rect.centery)
                                if dist < bullet.splash_radius:
                                    other_zombie.health -= bullet.damage * bullet.splash_ratio * get_damage_multiplier(other_zombie)

                        if is_player_bullet:
                            if player.skills.get("skill_fire_bullets", False):
                                zombie.burn_time = max(zombie.burn_time, 180)
                                zombie.burn_damage_cooldown = 0
                                fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "fire")
                            if player.skills.get("skill_ice_bullets", False):
                                zombie.slow_time = max(zombie.slow_time, 120)
                                zombie.slow_multiplier = min(zombie.slow_multiplier, 0.6)
                                fx.element_hit(zombie.rect.centerx, zombie.rect.centery, "ice")
                            if player.skills.get("skill_electric_bullets", False):
                                zombie.electric_fx = 30
                                chain_targets = []
                                for other_zombie in list(zombies):
                                    if other_zombie is zombie or other_zombie not in zombies:
                                        continue
                                    dx = other_zombie.rect.centerx - zombie.rect.centerx
                                    dy = other_zombie.rect.centery - zombie.rect.centery
                                    dist = math.sqrt(dx * dx + dy * dy)
                                    if dist < 160:
                                        chain_targets.append((dist, other_zombie))
                                chain_targets.sort(key=lambda entry: entry[0])
                                for _, target in chain_targets[:2]:
                                    chain_mult = get_damage_multiplier(target)
                                    target.health -= bullet.damage * 0.4 * chain_mult
                                    fx.lightning(zombie.rect.centerx, zombie.rect.centery, target.rect.centerx, target.rect.centery)
                                    fx.element_hit(target.rect.centerx, target.rect.centery, "electric")
                                    target.electric_fx = 30
                            if player.skills.get("skill_explosion", False) and bullet.bullet_type != "rocket" and player.explosion_cooldown <= 0:
                                player.explosion_cooldown = EXPLOSION_SKILL_COOLDOWN
                                explosion_radius = 70
                                explosion = Explosion(bullet.rect.centerx, bullet.rect.centery, explosion_radius)
                                explosions.add(explosion)
                                all_sprites.add(explosion)
                                for other_zombie in list(zombies):
                                    if other_zombie not in zombies or other_zombie is zombie:
                                        continue
                                    dist = math.sqrt((other_zombie.rect.centerx - bullet.rect.centerx)**2 +
                                                   (other_zombie.rect.centery - bullet.rect.centery)**2)
                                    if dist < explosion_radius:
                                        boom_mult = get_damage_multiplier(other_zombie)
                                        other_zombie.health -= bullet.damage * EXPLOSION_SKILL_RATIO * boom_mult

                        # 관통 (레벨식): 총알 기본 관통 + 플레이어 관통 레벨만큼 더 뚫고 지나감
                        bullet.hit_targets.add(zombie)
                        if len(bullet.hit_targets) > bullet.pierce + player.pierce_level:
                            bullet.kill()

            # 플레이어-아이템 충돌
            hit_items = pygame.sprite.spritecollide(player, items, True)
            for item in hit_items:
                fx.ring(item.rect.centerx, item.rect.centery, ITEM_COLORS[item.item_type], 70, count=18)
                fx.add_text(player.rect.centerx, player.rect.top - 20, item.effect, ITEM_COLORS[item.item_type], life=50)
                if item.item_type == "health":
                    player.health = min(player.health + ITEM_HEAL_AMOUNT, player.max_health)
                elif item.item_type == "damage":
                    # 10초간 공격력 +30% (예전 효과 "player.damage +15"는 거의 어떤 공격에도 쓰이지 않던 값이었음)
                    player.damage_buff_time = ITEM_BUFF_FRAMES
                elif item.item_type == "speed":
                    # 10초간 이동속도 +30% (예전처럼 영구 +2면 몇 개만 먹어도 너무 빨라짐)
                    player.speed_buff_time = ITEM_BUFF_FRAMES
                score += 5

            # 좀비-플레이어 충돌
            hit_zombies = pygame.sprite.spritecollide(player, zombies, False)
            for zombie in hit_zombies:
                # 임프: 닿으면 자폭 (작은 폭발, 점수/경험치 없음)
                if zombie.zombie_type == "imp":
                    if zombie.health > 0:
                        zombie.health = 0
                        zombie.no_reward = True
                        boom = Explosion(zombie.rect.centerx, zombie.rect.centery, 50)
                        explosions.add(boom)
                        all_sprites.add(boom)
                        apply_player_damage(player, 6)
                    continue
                # 스파크: 감전 → 0.6초 동안 공격 불가
                if zombie.zombie_type == "spark":
                    if player.shock_time <= 0:
                        fx.add_text(player.rect.centerx, player.rect.top - 20, "감전!", (255, 240, 90))
                    player.shock_time = max(player.shock_time, 36)
                # 산성: 부식 → 4초 동안 받는 피해 +30%
                if zombie.zombie_type == "acid":
                    player.corrode_time = max(player.corrode_time, 240)

                # 기본 데미지
                base_damage = 0.5

                # ===== 좀비의 특수 능력 처리 =====
                # spike: 가시 - 추가 데미지
                if zombie.zombie_type == "spike":
                    base_damage += zombie.spike_damage

                # poison: 독 - 플레이어에게 독 상태 부여
                if zombie.zombie_type == "poison":
                    player.poison_time = 300  # 5초간 독 상태

                # ice: 얼음 - 플레이어 속도 저하
                if zombie.zombie_type == "ice":
                    if hasattr(zombie, 'slow_effect'):
                        if player.slow_time <= 0:
                            player.slow_time = 60  # 1초간 둔화
                        player.slow_multiplier = min(player.slow_multiplier, zombie.slow_effect)

                # 데미지 적용 (회피 판정은 apply_player_damage 안에서 모든 피해에 공통으로 처리)
                apply_player_damage(player, base_damage)

            # ===== 특수 좀비 투사체 처리 =====
            # 플레이어-특수 투사체 충돌 (단일 루프)
            for bullet in list(bullets):
                try:
                    if not hasattr(bullet, 'rect') or not bullet.rect.colliderect(player.rect):
                        continue

                    if isinstance(bullet, SpikeProjectile):
                        if hasattr(bullet, 'damage'):
                            apply_player_damage(player, bullet.damage)
                        bullet.kill()
                        if player.health <= 0:
                            game_over = True
                            game_over_time = pygame.time.get_ticks()

                    elif isinstance(bullet, IceProjectile):
                        if hasattr(bullet, 'slow_effect'):
                            # 플레이어에 slow 효과 적용
                            if player.slow_time <= 0:
                                player.slow_time = 300  # 5초간 둔화
                            player.slow_multiplier = min(player.slow_multiplier, bullet.slow_effect)
                        bullet.kill()

                    elif isinstance(bullet, NinjaProjectile):
                        if hasattr(bullet, 'damage'):
                            apply_player_damage(player, bullet.damage)
                        bullet.kill()
                        if player.health <= 0:
                            game_over = True
                            game_over_time = pygame.time.get_ticks()

                    elif isinstance(bullet, Bullet) and bullet.is_enemy:
                        # 갱스터 총알 / 용 파이어볼 (예전에는 플레이어에게 피해를 주는 처리 자체가 없었음)
                        apply_player_damage(player, bullet.damage)
                        bullet.kill()
                except:
                    pass

            # 독 장판 / 쓰나미 충돌 처리
            # (예전에는 장판이 겹치면 장판 수만큼 피해가 배로 들어오고, 독 상태와 피해 쿨타임을 같이 써서 더 빨라졌음)
            in_poison_pool = False
            for pool in list(explosions):
                if isinstance(pool, PoisonPool):
                    dx = pool.rect.centerx - player.rect.centerx
                    dy = pool.rect.centery - player.rect.centery
                    if dx * dx + dy * dy < pool.radius * pool.radius:
                        in_poison_pool = True
                elif isinstance(pool, TsunamiEffect):
                    # 리바이어던 쓰나미: 닿으면 1회 피해 (예전에는 충돌 처리가 없어서 피해가 없었음)
                    if not pool.has_hit_player and pool.rect.colliderect(player.rect):
                        apply_player_damage(player, pool.damage)
                        pool.has_hit_player = True

            if in_poison_pool:
                # 플레이어가 독 장판 범위 내 (장판이 여러 개 겹쳐도 한 번만)
                if player.poison_time <= 0:
                    player.poison_time = 300  # 독 상태 시작
                player.pool_damage_cooldown -= 1
                if player.pool_damage_cooldown <= 0:
                    apply_player_damage(player, 0.3 * 2)  # 장판의 독은 더 강함
                    player.pool_damage_cooldown = 15  # 0.25초마다

            # 독 상태 처리
            if player.poison_time > 0:
                player.poison_time -= 1
                player.poison_damage_cooldown -= 1
                if player.poison_damage_cooldown <= 0:
                    apply_player_damage(player, 0.3)  # 주기적 독 데미지
                    player.poison_damage_cooldown = 30  # 0.5초마다

            # 둔화 상태 처리
            if player.slow_time > 0:
                player.slow_time -= 1
            else:
                player.slow_multiplier = 1.0

            # 좀비 생성 (플레이어로부터 거리에 따라)
            zombie_spawn_counter += 1
            max_zombies = get_max_zombies(wave)  # 웨이브가 진행될수록 더 많은 좀비 (웨이브마다 +2)

            if len(zombies) < max_zombies and zombie_spawn_counter > get_spawn_interval(wave):
                angle = random.uniform(0, 2 * math.pi)
                distance = 600
                x = player.rect.centerx + math.cos(angle) * distance
                y = player.rect.centery + math.sin(angle) * distance

                # 웨이브에 따라 점진적으로 좀비 타입 선택
                zombie_type = get_zombie_type_by_wave(wave)

                zombie = Zombie(x, y, zombie_type=zombie_type, wave=wave)
                zombies.add(zombie)
                all_sprites.add(zombie)
                zombie_spawn_counter = 0

            # 60초마다 웨이브 증가
            elapsed_time = pygame.time.get_ticks() - wave_timer_start
            if elapsed_time >= wave_interval:
                wave += 1
                wave_timer_start = pygame.time.get_ticks()  # 타이머 리셋
                boss_spawned = False
                num_zombies = 3 + wave * 2  # 웨이브 시작 시 한꺼번에 나오는 좀비 (웨이브마다 +2)

                for _ in range(num_zombies):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(300, 800)
                    x = player.rect.centerx + math.cos(angle) * distance
                    y = player.rect.centery + math.sin(angle) * distance

                    # 첫 번째 좀비는 보스 또는 고급 좀비 (웨이브 3부터)
                    if wave >= 3 and not boss_spawned:
                        boss_types = ["boss", "paladin", "demon", "angel", "dragon", "king", "god"]  # 기사단장 누락 수정
                        zombie_type = random.choice(boss_types)
                        boss_spawned = True
                    else:
                        # 웨이브에 따라 점진적으로 좀비 타입 선택
                        zombie_type = get_zombie_type_by_wave(wave)

                    zombie = Zombie(x, y, zombie_type=zombie_type, wave=wave)
                    zombies.add(zombie)
                    all_sprites.add(zombie)

            # 결계의 천사: 처음 몇 번의 공격은 막아냄 (이번 프레임에 받은 피해를 되돌림)
            for zombie in zombies:
                if zombie.block_hits > 0 and zombie.health < zombie.last_health:
                    zombie.health = zombie.last_health
                    zombie.block_hits -= 1
                    zombie.custom_name = f"{zombie.base_name} [{zombie.block_hits}]"
                    fx.add_text(zombie.rect.centerx, zombie.rect.top - 8, "막음", (190, 160, 255))
                    fx.ring(zombie.rect.centerx, zombie.rect.centery, (190, 160, 255), 50, count=14)

            # ===== 피격 연출: 이번 프레임에 깎인 체력만큼 데미지 숫자 + 하얀 번쩍임 =====
            # (총알/근접/스킬/폭발 등 피해를 주는 곳이 많아서, 체력 변화로 한 곳에서 처리 - 판정에는 영향 없음)
            for zombie in zombies:
                lost = zombie.last_health - zombie.health
                zombie.last_health = zombie.health
                if zombie.hit_flash > 0:
                    zombie.hit_flash -= 1
                if lost > 0.01:
                    zombie.damage_accum += lost
                    if lost >= 1:
                        zombie.hit_flash = 5
                zombie.damage_text_cooldown -= 1
                # 화상처럼 작은 피해는 모아서 표시, 죽는 순간에는 바로 표시
                if zombie.damage_accum >= 1 and (zombie.damage_text_cooldown <= 0 or zombie.health <= 0):
                    fx.add_damage_text(zombie.rect.centerx, zombie.rect.top - 8, zombie.damage_accum, zombie.crit_marked)
                    zombie.damage_accum = 0.0
                    zombie.crit_marked = False
                    zombie.damage_text_cooldown = 6

            player_lost = last_player_health - player.health
            last_player_health = player.health
            if player_lost > 0.01:
                fx.add_hurt(min(0.6, player_lost / 12))
                player.hurt_flash = max(player.hurt_flash, 8)
                if player_lost >= 6:  # 큰 피해(폭발, 파이어볼 등)는 화면이 흔들림
                    fx.add_shake(min(10, player_lost / 3))

            # ===== 좀비 죽음 처리 =====
            # 총알/근접/스킬/화상/폭발 등 어떤 이유로 죽든 모든 사망을 여기서 한 번에 처리
            # (예전에는 총알·근접으로 죽으면 그 자리에서 바로 kill()해서 폭탄 폭발·얼음 투사체 같은 사망 효과가 안 나왔고,
            #  반대로 화상·폭발·스킬로 죽으면 점수/경험치를 받지 못했음)
            for zombie in list(zombies):
                if zombie not in zombies or zombie.health > 0:
                    continue

                # 점수/경험치 (부활하는 좀비도 처치 1회로 인정, 자폭한 임프는 제외)
                if not zombie.no_reward:
                    score += 10
                    exp_gain = get_exp_reward(player, wave)
                    if getattr(zombie, "dash_kill", False):   # 카타나 일섬으로 처치: 경험치 75%
                        exp_gain = int(exp_gain * KATANA_DASH_EXP_RATIO)
                        zombie.dash_kill = False
                    player.exp += exp_gain

                death_type = zombie.zombie_type
                death_x, death_y = zombie.rect.center

                # kill()이 부활 체인을 처리함: 기사→방패→갑옷→일반, 기사단장→갑옷→일반, 철→돌
                zombie.kill()
                if zombie.alive():
                    # 부활함: 부활 이펙트만 표시하고 사망 효과는 없음
                    all_sprites.add(ResurrectionEffect(death_x, death_y, (100, 150, 200)))
                    fx.burst(death_x, death_y, (150, 200, 255), 14, speed=(1, 4), size=(2, 4), life=(14, 26))
                    zombie.last_health = zombie.health  # 부활로 체력이 오른 것은 피격으로 보지 않음
                    continue

                # 처치 연출: 몸 색 파편 + 쓰러지며 사라짐 (보스/거대 좀비는 화면 흔들림)
                fx.death_burst(death_x, death_y, zombie.image.get_at((zombie.image.get_width() // 2, zombie.image.get_height() // 2))[:3], zombie.size)
                all_sprites.add(DeathFade(zombie))
                if death_type in GUARANTEED_DROP_TYPES:
                    fx.add_shake(9)

                # 아이템 드롭 (완전히 죽었을 때만)
                if not zombie.no_reward:
                    maybe_drop_item(death_type, death_x, death_y, items, all_sprites, summoned=zombie.parent_zombie is not None)

                # ice 좀비: 얼음 투사체 발사
                if death_type == "ice":
                    if player.rect.center != (death_x, death_y):
                        ice_proj = IceProjectile(death_x, death_y, player.rect.centerx, player.rect.centery)
                        bullets.add(ice_proj)
                        all_sprites.add(ice_proj)

                # wind 바람: 광역 이펙트 (약한 데미지 + 밀치기)
                elif death_type == "wind":
                    all_sprites.add(WindBlastEffect(death_x, death_y, 200, 0.5, 15))
                    for other_zombie in list(zombies):
                        dist = math.hypot(other_zombie.rect.centerx - death_x, other_zombie.rect.centery - death_y)
                        if dist < 200:
                            if dist > 0:
                                other_zombie.knockback_vel_x += (other_zombie.rect.centerx - death_x) / dist * 15
                                other_zombie.knockback_vel_y += (other_zombie.rect.centery - death_y) / dist * 15
                            other_zombie.health -= 0.5

                # 폭탄 좀비: 사망 시 폭발
                elif death_type in ["bomber", "mine", "flame", "acid", "toxic", "nuclear"]:
                    bomb_radius = {
                        "bomber": 140,
                        "mine": 170,
                        "flame": 180,
                        "acid": 160,
                        "toxic": 175,
                        "nuclear": 220,
                    }.get(death_type, 150)
                    bomb_damage = {
                        "bomber": 30.0,
                        "mine": 40.0,
                        "flame": 35.0,
                        "acid": 32.0,
                        "toxic": 38.0,
                        "nuclear": 50.0,
                    }.get(death_type, 30.0)

                    # 이제 총알/근접으로 죽여도 항상 폭발하므로, 근접 무기로 잡을 때 너무 가혹하지 않게
                    # 플레이어가 받는 폭발 피해는 절반 (주변 좀비에게는 그대로)
                    trigger_bomb_explosion(zombie, player, zombies, all_sprites, explosions, bomb_radius, bomb_damage,
                                           player_damage=bomb_damage * 0.5)

                    # 불꽃 좀비는 화염 폭발 이펙트도 표시
                    # (예전에는 불꽃 전용 분기가 폭탄 분기 뒤의 elif라서 절대 실행되지 않았음)
                    if death_type == "flame":
                        all_sprites.add(FlameExplosionEffect(death_x, death_y, bomb_radius, 2.0))

                    # 산성 좀비 폭발에 휘말리면 부식 (4초 동안 받는 피해 +30%)
                    if death_type == "acid" and math.hypot(player.rect.centerx - death_x, player.rect.centery - death_y) < bomb_radius:
                        player.corrode_time = max(player.corrode_time, 240)

                    # 독가스 좀비는 죽은 자리에 독 영역을 남김 (게임 설명에는 있었지만 구현이 없었음)
                    if death_type == "toxic":
                        toxic_pool = PoisonPool(death_x, death_y, radius=120, duration=6000)
                        explosions.add(toxic_pool)
                        all_sprites.add(toxic_pool)

                    # 핵 좀비는 주변에 폭탄좀비 5종을 0~3마리씩 소환
                    if death_type == "nuclear":
                        bomb_types = ["bomber", "mine", "flame", "acid", "toxic"]
                        for bomb_type in bomb_types:
                            spawn_count = random.randint(0, 3)
                            for _ in range(spawn_count):
                                bomb_angle = random.uniform(0, 2 * math.pi)
                                bomb_x = death_x + math.cos(bomb_angle) * random.uniform(50, 200)
                                bomb_y = death_y + math.sin(bomb_angle) * random.uniform(50, 200)

                                bomb_zombie = Zombie(bomb_x, bomb_y, zombie_type=bomb_type, wave=zombie.wave, parent_zombie=zombie)
                                zombies.add(bomb_zombie)
                                all_sprites.add(bomb_zombie)
                                all_sprites.add(SpawnEffect(bomb_x, bomb_y, (200, 100, 0), 200))

                # 분열좀비: 2세대까지 작은 분열좀비 2마리로 나뉨 (체력·크기 절반)
                elif death_type == "slime" and zombie.slime_gen < 2:
                    for side in (-1, 1):
                        child = Zombie(death_x + side * 25, death_y, zombie_type="slime", wave=zombie.wave, parent_zombie=zombie)
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
                        child.speed *= 1.2   # 작을수록 조금 빠름
                        zombies.add(child)
                        all_sprites.add(child)
                    fx.burst(death_x, death_y, (120, 255, 120), 16, speed=(1, 4), size=(2, 5), life=(12, 22))

                # 분열의 천사: 임프 3마리로 분열
                elif zombie.angel_role == "split":
                    for i in range(3):
                        imp_angle = i / 3 * math.pi * 2
                        imp_x = death_x + math.cos(imp_angle) * 40
                        imp_y = death_y + math.sin(imp_angle) * 40
                        imp = Zombie(imp_x, imp_y, zombie_type="imp", wave=zombie.wave, parent_zombie=zombie)
                        zombies.add(imp)
                        all_sprites.add(imp)
                        all_sprites.add(SpawnEffect(imp_x, imp_y, (255, 120, 170), 300))

                # 천사 (angel): 약해진 신성한 광역 폭발 (12천사는 각자 능력이 있으므로 제외)
                elif death_type == "angel" and zombie.angel_role is None:
                    all_sprites.add(HolyExplosionEffect(death_x, death_y, 180, 3.0))
                    if math.hypot(player.rect.centerx - death_x, player.rect.centery - death_y) < 180:
                        apply_player_damage(player, 3.0)
                    for other_zombie in list(zombies):
                        if math.hypot(other_zombie.rect.centerx - death_x, other_zombie.rect.centery - death_y) < 180:
                            other_zombie.health -= 3.0

                # god 신: 신성한 광역 폭발
                elif death_type == "god":
                    all_sprites.add(HolyExplosionEffect(death_x, death_y, 250, 5.0))
                    if math.hypot(player.rect.centerx - death_x, player.rect.centery - death_y) < 250:
                        apply_player_damage(player, 5.0)
                    for other_zombie in list(zombies):
                        if math.hypot(other_zombie.rect.centerx - death_x, other_zombie.rect.centery - death_y) < 250:
                            other_zombie.health -= 5.0

                # 타이탄: 30% 확률로 거인 2마리로 부활 (확률 판정은 Zombie.kill()에서 함)
                elif death_type == "titan" and getattr(zombie, "titan_respawn_as_giants", False):
                    for _ in range(2):
                        giant_angle = random.uniform(0, 2 * math.pi)
                        giant_x = death_x + math.cos(giant_angle) * 80
                        giant_y = death_y + math.sin(giant_angle) * 80

                        giant = Zombie(giant_x, giant_y, zombie_type="giant", wave=zombie.wave, parent_zombie=zombie)
                        zombies.add(giant)
                        all_sprites.add(giant)
                        all_sprites.add(SpawnEffect(giant_x, giant_y, (150, 100, 50), 300))

            # 독 상태/폭발/쓰나미 등 어떤 피해로든 체력이 0 이하가 되면 게임 오버
            # (예전에는 독 상태 피해 등 일부 피해로 체력이 0이 돼도 게임 오버가 되지 않았음)
            if player.health <= 0 and not game_over:
                game_over = True
                delete_save()
                game_over_time = pygame.time.get_ticks()

        # 화면 그리기
        fx.elements = [element for element, skill in (("fire", "skill_fire_bullets"), ("ice", "skill_ice_bullets"),
                                                      ("electric", "skill_electric_bullets")) if player.skills.get(skill, False)]
        fx.update()  # 게임 오버 화면에서도 남은 파티클은 끝까지 움직이게
        camera.shake_x, camera.shake_y = fx.shake_offset()
        screen.fill(BLACK)
        camera.draw_background(screen)

        # 모든 객체 그리기 (rect를 수정하지 않고 화면 좌표에만 블릿)
        # 좀비/플레이어는 걷기 모션으로 따로 그리고, 플레이어는 맨 위에 그림
        for sprite in all_sprites:
            if sprite is player:
                continue
            if isinstance(sprite, Zombie):
                draw_zombie_sprite(screen, camera, sprite, player)
                continue
            screen_x, screen_y = camera.apply(sprite.rect.centerx, sprite.rect.centery)
            screen_y += getattr(sprite, "draw_offset_y", 0)  # 아이템 둥실 모션
            iw, ih = sprite.image.get_size()
            if screen_x + iw / 2 < 0 or screen_x - iw / 2 > SCREEN_WIDTH or screen_y + ih / 2 < 0 or screen_y - ih / 2 > SCREEN_HEIGHT:
                continue  # 화면 밖은 그리지 않음
            screen.blit(sprite.image, (int(screen_x - iw / 2), int(screen_y - ih / 2)))
        draw_player_sprite(screen, camera, player)
        fx.draw(screen, camera)

        # 좀비 이름/체력 바
        draw_zombie_labels(screen, camera, zombies)

        # 피격 시 화면 가장자리 붉은 경고
        draw_hurt_overlay(screen, fx.hurt)

        # HUD (체력/경험치/무기/스킬/버프 · 웨이브 · 점수/레벨 · 보스 체력 · 업그레이드 목록)
        wave_progress = (pygame.time.get_ticks() - wave_timer_start) / wave_interval
        draw_hud(screen, player, score, wave, wave_progress, wave_interval, zombies, show_stack)

        # 게임 오버 화면
        if game_over:
            draw_game_over(screen, "게임 오버!", [("점수", score), ("웨이브", wave), ("레벨", player.level), ("무기", player.weapon.name)],
                           "SPACE: 다시 시작 · ESC: 종료")

        pygame.display.flip()

    return "quit"


if __name__ == "__main__":
    try:
        # main()이 "restart"를 돌려주면 능력 선택 화면부터 다시 시작
        # (예전에는 main() 안에서 main()을 재귀 호출해서 재시작할 때마다 이전 게임이 스택에 쌓였음)
        while main() == "restart":
            pass
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
    pygame.quit()
    sys.exit()

