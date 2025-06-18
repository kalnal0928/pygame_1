import pygame
import os

pygame.init()

background = pygame.display.set_mode((800, 600))        
pygame.display.set_caption("Game Window")

fps = pygame.time.Clock()

# 스프라이트 시트 로드 및 애니메이션 설정
try:
    # 현재 작업 디렉토리 확인
    print(f"현재 작업 디렉토리: {os.getcwd()}")
    
    # 현재 스크립트 파일의 디렉토리 경로 가져오기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"스크립트 디렉토리: {script_dir}")
    
    # 이미지 파일 경로들 확인 (상대 경로와 절대 경로 모두 시도)
    possible_paths = [
        "image/sprite_sheet.png",
        "image/sprite_sheet.jpg", 
        "image/sprite_sheet.jpeg",
        "sprite_sheet.png",
        os.path.join(script_dir, "image/sprite_sheet.png"),
        os.path.join(script_dir, "image/sprite_sheet.jpg"),
        os.path.join(script_dir, "image/sprite_sheet.jpeg"),
        os.path.join(script_dir, "sprite_sheet.png")
    ]
    
    sprite_sheet = None
    for path in possible_paths:
        if os.path.exists(path):
            print(f"이미지 파일 발견: {path}")
            sprite_sheet = pygame.image.load(path)
            break
        else:
            print(f"파일 없음: {path}")
    
    if sprite_sheet is None:
        raise FileNotFoundError("스프라이트 시트를 찾을 수 없습니다.")
    
    print(f"이미지 크기: {sprite_sheet.get_size()}")
    
    # 스프라이트 시트에서 개별 프레임 추출
    frame_width = sprite_sheet.get_width() // 5  # 가로 5개 프레임
    frame_height = sprite_sheet.get_height() // 2  # 세로 2개 행
    
    print(f"프레임 크기: {frame_width}x{frame_height}")
    
    # 애니메이션 프레임들 저장
    walking_frames = []
    
    # 첫 번째 행 (걷기 애니메이션)
    for i in range(5):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (60, 60))  # 크기 조정
        walking_frames.append(frame)
    
    # 두 번째 행도 추가
    for i in range(5):
        frame = sprite_sheet.subsurface((i * frame_width, frame_height, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (60, 60))
        walking_frames.append(frame)
    
    print(f"총 {len(walking_frames)}개 프레임 로드됨")
    
except Exception as e:
    print(f"이미지 로드 에러: {e}")
    # 이미지가 없으면 기본 사각형 생성
    walking_frames = []
    default_surface = pygame.Surface((60, 60))
    default_surface.fill((255, 0, 0))
    walking_frames.append(default_surface)
    print("기본 빨간 사각형 사용")

# 애니메이션 변수
current_frame = 0
animation_speed = 200  # 밀리초 단위
last_update = 0

# 플레이어 rect 생성
player_rect = walking_frames[0].get_rect()
player_rect.center = (background.get_size()[0] // 2, background.get_size()[1] // 2)

# 이동 상태 추적
is_moving = False

play = True
while play:
    current_time = pygame.time.get_ticks()
    deltaTime = fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False    
    
    # 현재 눌린 키 상태 확인
    keys = pygame.key.get_pressed()
    
    speed = 5  # 이동 속도
    to_x = 0
    to_y = 0
    is_moving = False
    
    if keys[pygame.K_LEFT]:
        to_x = -speed
        is_moving = True
    if keys[pygame.K_RIGHT]:
        to_x = speed
        is_moving = True
    if keys[pygame.K_UP]:
        to_y = -speed
        is_moving = True
    if keys[pygame.K_DOWN]:
        to_y = speed
        is_moving = True

    # rect 위치 업데이트
    player_rect.x += to_x
    player_rect.y += to_y
    
    # 화면 경계 체크
    player_rect.clamp_ip(pygame.Rect(0, 0, 800, 600))
    
    # 애니메이션 업데이트 (움직일 때만)
    if is_moving and current_time - last_update > animation_speed:
        current_frame = (current_frame + 1) % len(walking_frames)
        last_update = current_time
    elif not is_moving:
        current_frame = 0  # 정지 시 첫 번째 프레임
    
    # 화면 그리기
    background.fill((255, 255, 255))  # 배경색을 흰색으로 설정
    
    # 현재 프레임 가져오기
    current_image = walking_frames[current_frame]
    
    # 왼쪽 방향키가 눌렸으면 이미지 좌우 반전
    if keys[pygame.K_LEFT]:
        current_image = pygame.transform.flip(current_image, True, False)
    
    background.blit(current_image, player_rect)  # 현재 프레임 그리기

    pygame.display.update()  # 화면 업데이트

pygame.quit()

