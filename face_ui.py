import pygame
import math
import sys

# Initialize pygame
pygame.init()

# 1. Screen Setup (Set to your actual screen size, or use pygame.FULLSCREEN)
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Assistant Face")

# Colors
BLACK = (0, 0, 0)
CYAN_GLOW = (0, 255, 255)

# Clock to manage frame rate
clock = pygame.time.Clock()

def draw_glowing_eye(surface, center_x, center_y, base_radius, glow_radius):
    """Draws an eye with a soft neon bloom effect by layering transparent circles."""
    # Create a temporary surface with alpha channel support for transparency
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    
    # Layer 1: Outer soft glow (highly transparent)
    pygame.draw.circle(glow_surf, (0, 255, 255, 30), (glow_radius, glow_radius), glow_radius)
    
    # Layer 2: Mid-glow
    pygame.draw.circle(glow_surf, (0, 255, 255, 90), (glow_radius, glow_radius), int(glow_radius * 0.7))
    
    # Layer 3: Solid core eye
    pygame.draw.circle(glow_surf, (200, 255, 255, 255), (glow_radius, glow_radius), base_radius)
    
    # Blit the glow surface onto the main screen
    surface.blit(glow_surf, (center_x - glow_radius, center_y - glow_radius))

# Main game loop
running = True
frame_count = 0

while running:
    # Handle closing the window safely
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Clear screen with perfect pitch black
    screen.fill(BLACK)

    # Calculate positions relative to screen size
    left_eye_x = WIDTH // 3
    right_eye_x = (WIDTH // 3) * 2
    eye_y = HEIGHT // 2 - 30

    # Gentle breathing animation using a sine wave
    frame_count += 1
    pulse = math.sin(frame_count * 0.05) * 5  # Varies between -5 and +5
    
    current_base_radius = 25
    current_glow_radius = int(60 + pulse) # The glow grows and shrinks smoothly

    # Draw the face components
    draw_glowing_eye(screen, left_eye_x, eye_y, current_base_radius, current_glow_radius)
    draw_glowing_eye(screen, right_eye_x, eye_y, current_base_radius, current_glow_radius)
    
    # Draw a simple mouth (a horizontal glowing capsule)
    mouth_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 60, 120, 20)
    pygame.draw.rect(screen, CYAN_GLOW, mouth_rect, border_radius=10)

    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate at 60 FPS
    clock.tick(60)

pygame.quit()
sys.exit()
