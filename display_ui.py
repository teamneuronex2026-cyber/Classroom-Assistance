import pygame
import sys

# Initialize Pygame for framebuffer display
pygame.init()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classroom Assistant UI")

# Colors
BG_COLOR = (20, 24, 33)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (0, 168, 204)

font = pygame.font.Font(None, 48)

def draw_screen(status_text="Listening..."):
    screen.fill(BG_COLOR)
    
    # Draw status bubble
    pygame.draw.circle(screen, ACCENT_COLOR, (WIDTH // 2, HEIGHT // 2 - 40), 60)
    
    # Render text
    text_surface = font.render(status_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

if __name__ == "__main__":
    draw_screen("Ready...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()