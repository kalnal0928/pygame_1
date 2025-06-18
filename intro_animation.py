import pygame
import os

class IntroAnimation:
    def __init__(self, screen_size, image_paths=None):
        if image_paths is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_paths = [
                "image/player/start.png",
                os.path.join(script_dir, "image/player/start.png"),
                "image/start.png",
                os.path.join(script_dir, "image/start.png")
            ]
        
        self.sprite_sheet = None
        for path in image_paths:
            if os.path.exists(path):
                print(f"시작 애니메이션 이미지 발견: {path}")
                self.sprite_sheet = pygame.image.load(path)
                break
            else:
                print(f"시작 애니메이션 이미지 없음: {path}")
        
        if self.sprite_sheet is None:
            # 기본 애니메이션 생성
            self.frames = self._create_default_frames()
            print("기본 시작 애니메이션 생성")
        else:
            print(f"시작 애니메이션 이미지 크기: {self.sprite_sheet.get_size()}")
            self.frames = self._extract_frames_auto(self.sprite_sheet)
            print(f"시작 애니메이션 {len(self.frames)}개 프레임 로드됨")
        
        self.current_frame = 0
        self.animation_speed = 150  # ms
        self.last_update = 0
        self.finished = False
        self.screen_size = screen_size

    def _create_default_frames(self):
        frames = []
        for i in range(5):
            surface = pygame.Surface((80, 80))
            surface.fill((0, 255 - i * 50, 0))  # 녹색 그라데이션
            frames.append(surface)
        return frames

    def _extract_frames_auto(self, sprite_sheet):
        """자동으로 프레임을 추출하는 메서드"""
        width, height = sprite_sheet.get_size()
        frames = []
        
        # 이미지 분석을 위한 정보 출력
        print(f"스프라이트 시트 크기: {width}x{height}")
        
        # 방법 1: 균등 분할 (기본)
        try:
            # 프레임 개수를 추정 (가로로 배열된 것으로 가정)
            estimated_frames = 8
            frame_width = width // estimated_frames
            frame_height = height
            
            print(f"추정 프레임 크기: {frame_width}x{frame_height}")
            
            for i in range(estimated_frames):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (80, 80))
                frames.append(frame)
                
        except Exception as e:
            print(f"균등 분할 실패: {e}")
            # 방법 2: 전체 이미지를 하나의 프레임으로 사용
            frame = pygame.transform.scale(sprite_sheet, (80, 80))
            frames.append(frame)
        
        return frames

    def update(self, current_time):
        if not self.finished and current_time - self.last_update > self.animation_speed:
            self.current_frame += 1
            self.last_update = current_time
            
            if self.current_frame >= len(self.frames):
                self.finished = True
                return True  # 애니메이션 완료
        
        return False

    def draw(self, surface):
        if self.current_frame < len(self.frames):
            image = self.frames[self.current_frame]
            rect = image.get_rect()
            rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2)
            surface.blit(image, rect)
        
        # 시작 텍스트 표시
        font = pygame.font.Font(None, 36)
        text = font.render("Player Appearing...", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2 + 100)
        surface.blit(text, text_rect)

    def reset(self):
        """애니메이션을 처음부터 다시 시작"""
        self.current_frame = 0
        self.finished = False
        self.last_update = 0 