import pygame
import os

class Player:
    def __init__(self, screen_size, sprite_sheet_paths=None):
        if sprite_sheet_paths is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sprite_sheet_paths = [
                "image/sprite_sheet.png",
                "image/sprite_sheet.jpg",
                "image/sprite_sheet.jpeg",
                "sprite_sheet.png",
                os.path.join(script_dir, "image/sprite_sheet.png"),
                os.path.join(script_dir, "image/sprite_sheet.jpg"),
                os.path.join(script_dir, "image/sprite_sheet.jpeg"),
                os.path.join(script_dir, "sprite_sheet.png")
            ]
        self.sprite_sheet = None
        for path in sprite_sheet_paths:
            if os.path.exists(path):
                self.sprite_sheet = pygame.image.load(path)
                break
        if self.sprite_sheet is None:
            # 기본 빨간 사각형
            self.walking_frames = [self._default_surface()]
        else:
            self.walking_frames = self._extract_frames(self.sprite_sheet)
        self.current_frame = 0
        self.animation_speed = 200  # ms
        self.last_update = 0
        self.is_moving = False
        self.rect = self.walking_frames[0].get_rect()
        self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)
        self.speed = 4
        self.facing_left = False

    def _default_surface(self):
        surface = pygame.Surface((60, 60))
        surface.fill((255, 0, 0))
        return surface

    def _extract_frames(self, sprite_sheet):
        frame_width = sprite_sheet.get_width() // 5
        frame_height = sprite_sheet.get_height() // 2
        frames = []
        for i in range(5):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (60, 60))
            frames.append(frame)
        for i in range(5):
            frame = sprite_sheet.subsurface((i * frame_width, frame_height, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (60, 60))
            frames.append(frame)
        return frames

    def handle_input(self, keys):
        to_x, to_y = 0, 0
        self.is_moving = False
        if keys[pygame.K_LEFT]:
            to_x = -self.speed
            self.is_moving = True
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            to_x = self.speed
            self.is_moving = True
            self.facing_left = False
        if keys[pygame.K_UP]:
            to_y = -self.speed
            self.is_moving = True
        if keys[pygame.K_DOWN]:
            to_y = self.speed
            self.is_moving = True
        self.rect.x += to_x
        self.rect.y += to_y
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

    def update(self, current_time):
        if self.is_moving and current_time - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
            self.last_update = current_time
        elif not self.is_moving:
            self.current_frame = 0

    def draw(self, surface):
        image = self.walking_frames[self.current_frame]
        if self.facing_left:
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, self.rect) 