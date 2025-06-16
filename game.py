import pygame

pygame.init()

background = pygame.display.set_mode((800, 600))        
pygame.display.set_caption("Game Window")

fps = pygame.time.Clock()

# 스프라이트 이미지 로드 (파일이 없으면 기본 사각형으로 대체)
try:
    player_image = pygame.image.load("player.png")  # 이미지 파일 경로
    player_image = pygame.transform.scale(player_image, (50, 50))  # 크기 조정
except:
    # 이미지가 없으면 기본 사각형 생성
    player_image = pygame.Surface((50, 50))
    player_image.fill((255, 0, 0))  # 빨간색

# 스프라이트 rect 생성 (충돌 감지 및 위치 관리용)
player_rect = player_image.get_rect()
player_rect.center = (background.get_size()[0] // 2, background.get_size()[1] // 2)

play = True
while play:
    deltaTime = fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False    
    
    # 현재 눌린 키 상태 확인
    keys = pygame.key.get_pressed()
    
    speed = 5  # 이동 속도
    to_x = 0
    to_y = 0
    
    if keys[pygame.K_LEFT]:
        to_x = -speed
    if keys[pygame.K_RIGHT]:
        to_x = speed
    if keys[pygame.K_UP]:
        to_y = -speed
    if keys[pygame.K_DOWN]:
        to_y = speed

    # rect 위치 업데이트
    player_rect.x += to_x
    player_rect.y += to_y
    
    # 화면 경계 체크
    player_rect.clamp_ip(pygame.Rect(0, 0, 800, 600))
    
    background.fill((255, 255, 255))  # 배경색을 흰색으로 설정
    background.blit(player_image, player_rect)  # 스프라이트 그리기

    pygame.display.update()  # 화면 업데이트

pygame.quit()

