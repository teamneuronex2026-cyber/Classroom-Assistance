import pygame
import math
import sys
import random

# Initialize pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Assistant Face")

# Colors
BLACK = (0, 0, 0)
CYAN_GLOW = (0, 255, 255)
WHITE_CORE = (200, 255, 255)

clock = pygame.time.Clock()

# Animation State Variables
frame_count = 0
is_blinking = False
blink_frame = 0
BLINK_DURATION = 8  # How many frames the blink lasts

# Talking State Simulation
# Change this to True to see the mouth move, or False to make it idle
is_talking = True 

def draw_glowing_eye(surface, center_x, center_y, base_radius, glow_radius, open_ratio=1.0):
    """Draws an eye with a soft neon bloom effect. Supports blinking via open_ratio."""
    # If the eye is fully closed, don't draw anything
    if open_ratio <= 0.1:
        return
        
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    
    # Scale vertical sizes based on the blink open_ratio
    v_glow_radius = int(glow_radius * open_ratio)
    v_base_radius = int(base_radius * open_ratio)
    
    # Make sure radius values remain valid
    if v_glow_radius < 1 or v_base_radius < 1:
        return

    # Layer 1: Outer soft glow
    pygame.draw.ellipse(glow_surf, (0, 255, 255, 30), 
                        (0, glow_radius - v_glow_radius, glow_radius * 2, v_glow_radius * 2))
    
    # Layer 2: Mid-glow
    pygame.draw.ellipse(glow_surf, (0, 255, 255, 90), 
                        (glow_radius - int(glow_radius*0.7), glow_radius - int(v_glow_radius*0.7), 
                         int(glow_radius * 1.4), int(v_glow_radius * 1.4)))
    
    # Layer 3: Solid core eye
    pygame.draw.ellipse(glow_surf, (200, 255, 255, 255), 
                        (glow_radius - base_radius, glow_radius - v_base_radius, 
                         base_radius * 2, v_base_radius * 2))
    
    surface.blit(glow_surf, (center_x - glow_radius, center_y - glow_radius))

def draw_talking_mouth(surface, center_x, center_y, width, frame):
    """Draws a responsive digital soundwave mouth that reacts if speaking."""
    num_bars = 7
    bar_gap = 10
    total_bars_width = (num_bars * 10) + ((num_bars - 1) * bar_gap)
    start_x = center_x - (total_bars_width // 2)

    for i in range(num_bars):
        # Base height when idle
        base_height = 14
        
        # Add dynamic soundwave ripple if talking
        if is_talking:
            # Staggered wave patterns using sine functions relative to frame count
            wave_modifier = math.sin(frame * 0.3 + i * 0.8) * 20
            # Ensure outer bars are slightly shorter for a cleaner digital look
            edge_taper = math.sin((i / (num_bars - 1)) * math.pi)
            height = base_height + abs(int(wave_modifier * edge_taper))
        else:
            height = base_height

        bar_x = start_x + (i * (10 + bar_gap))
        bar_y = center_y - (height // 2)
        
        # Draw the glowing digital bar
        bar_rect = pygame.Rect(bar_x, bar_y, 10, height)
        pygame.draw.rect(surface, CYAN_GLOW, bar_rect, border_radius=5)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # Press SPACE to toggle the talking animation state manually for testing
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_talking = not is_talking

    screen.fill(BLACK)
    frame_count += 1

    # ---- 1. BLINK LOGIC ----
    # Randomly initiate a blink if not already blinking (approx every 3-5 seconds)
    if not is_blinking and random.random() < 0.005:
        is_blinking = True
        blink_frame = 0

    # Calculate eye vertical openness scale
    eye_open_ratio = 1.0
    if is_blinking:
        blink_frame += 1
        half_duration = BLINK_DURATION / 2
        # Progresses down to 0 (closed) and back up to 1 (open)
        eye_open_ratio = abs(blink_frame - half_duration) / half_duration
        
        if blink_frame >= BLINK_DURATION:
            is_blinking = False
            eye_open_ratio = 1.0

    # ---- 2. ANIMATION CALCULATIONS ----
    left_eye_x = WIDTH // 3
    right_eye_x = (WIDTH // 3) * 2
    eye_y = HEIGHT // 2 - 40
    mouth_y = HEIGHT // 2 + 70

    # Gentle breathing pulse for the glow effect
    pulse = math.sin(frame_count * 0.06) * 4
    current_base_radius = 26
    current_glow_radius = int(65 + pulse)

    # ---- 3. RENDER FACE ----
    draw_glowing_eye(screen, left_eye_x, eye_y, current_base_radius, current_glow_radius, eye_open_ratio)
    draw_glowing_eye(screen, right_eye_x, eye_y, current_base_radius, current_glow_radius, eye_open_ratio)
    draw_talking_mouth(screen, WIDTH // 2, mouth_y, 150, frame_count)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
