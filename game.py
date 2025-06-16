import pygame

pygame.init()

background = pygame.display.set_mode((800, 600))        

pygame.display.set_caption("Game Window")


play = True
while play:#  무한 반복 코드가 없으면 파이게임 창이 바로 꺼짐
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False    

pygame.quit()  # 게임이 끝나면 pygame을 종료

##### 기본 환경 #####