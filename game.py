import pygame
import os
from player import Player
from intro_animation import IntroAnimation

pygame.init()

background = pygame.display.set_mode((800, 600))        
pygame.display.set_caption("Game Window")

fps = pygame.time.Clock()

# 게임 상태 관리
GAME_STATE_INTRO = 0
GAME_STATE_PLAYING = 1
game_state = GAME_STATE_INTRO

# 시작 애니메이션 객체 생성
intro_animation = IntroAnimation(background.get_size())

# 플레이어 객체 생성
player = Player(background.get_size())

play = True
while play:
    current_time = pygame.time.get_ticks()
    deltaTime = fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False    
    
    # 게임 상태에 따른 처리
    if game_state == GAME_STATE_INTRO:
        # 시작 애니메이션 업데이트
        if intro_animation.update(current_time):
            game_state = GAME_STATE_PLAYING
            print("시작 애니메이션 완료! 게임 시작")
        
        # 화면 그리기 (시작 애니메이션)
        background.fill((0, 0, 0))  # 검은 배경
        intro_animation.draw(background)
    
    elif game_state == GAME_STATE_PLAYING:
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(current_time)
        background.fill((255, 255, 255))  # 배경색을 흰색으로 설정
        player.draw(background)

    pygame.display.update()  # 화면 업데이트

pygame.quit()

def extract_frames_by_color(sprite_sheet, border_color=(255,255,255,255)):
    width, height = sprite_sheet.get_size()
    frames = []
    in_frame = False
    start_x = 0

    for x in range(width):
        column = [sprite_sheet.get_at((x, y)) for y in range(height)]
        is_border = all(pixel[:3] == border_color[:3] for pixel in column)
        if not in_frame and not is_border:
            # 프레임 시작
            in_frame = True
            start_x = x
        elif in_frame and is_border:
            # 프레임 끝
            in_frame = False
            frame_rect = pygame.Rect(start_x, 0, x - start_x, height)
            frame = sprite_sheet.subsurface(frame_rect)
            frames.append(frame)
    # 마지막 프레임 처리
    if in_frame:
        frame_rect = pygame.Rect(start_x, 0, width - start_x, height)
        frame = sprite_sheet.subsurface(frame_rect)
        frames.append(frame)
    return frames

# 사용 예시
sprite_sheet = pygame.image.load("image/sprite_sheet.png").convert_alpha()
frames = extract_frames_by_color(sprite_sheet, border_color=(255,255,255,255))  # 흰색 경계

