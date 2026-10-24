import pygame
import math
import sys
import random

# Initialize pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Premium Assistant Face")

# Colors
BLACK = (0, 0, 0)
CYAN_GLOW = (0, 255, 255)

clock = pygame.time.Clock()

# Animation State Variables
frame_count = 0
is_blinking = False
blink_frame = 0
BLINK_DURATION = 10  # Smooth, slightly slower deliberate blink

# Focus/Dilation adjustments for looking around
eye_drift_x = 0
eye_drift_y = 0
next_drift_time = 0

# Talking State Simulation (Toggle with SPACEBAR)
is_talking = True 

def draw_glowing_eye(surface, center_x, center_y, base_radius_x, base_radius_y, glow_radius, open_ratio=1.0):
    """Draws larger, expressive eyes with multi-stage alpha glow compounding."""
    if open_ratio <= 0.05:
        return
        
    # Scale vertical components dynamically for the blink animation
    v_glow_radius = int(glow_radius * open_ratio)
    v_base_radius = int(base_radius_y * open_ratio)
    
    if v_glow_radius < 1 or v_base_radius < 1:
        return

    # Create local surface for transparency layering
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    
    # Layer 1: Massive soft outer bloom
    pygame.draw.ellipse(glow_surf, (0, 255, 255, 20), 
                        (0, glow_radius - v_glow_radius, glow_radius * 2, v_glow_radius * 2))
    
    # Layer 2: Core bloom intensity
    pygame.draw.ellipse(glow_surf, (0, 255, 255, 65), 
                        (glow_radius - int(base_radius_x * 1.5), glow_radius - int(v_base_radius * 1.5), 
                         int(base_radius_x * 3), int(v_base_radius * 3)))
    
    # Layer 3: Solid vibrant digital core
    pygame.draw.ellipse(glow_surf, (220, 255, 255, 255), 
                        (glow_radius - base_radius_x, glow_radius - v_base_radius, 
                         base_radius_x * 2, v_base_radius * 2))
    
    surface.blit(glow_surf, (center_x - glow_radius, center_y - glow_radius))

def draw_talking_mouth(surface, center_x, center_y, frame):
    """Draws an expanded, wider digital equalizer soundwave style mouth."""
    num_bars = 9  # Increased for a much wider look
    bar_width = 12
    bar_gap = 12
    total_bars_width = (num_bars * bar_width) + ((num_bars - 1) * bar_gap)
    start_x = center_x - (total_bars_width // 2)

    for i in range(num_bars):
        base_height = 12
        
        if is_talking:
            # Complex double-sine wave formula to make the voice wave look rich and high-tech
            wave_modifier = (math.sin(frame * 0.25 + i * 0.7) * 25) + (math.cos(frame * 0.15 + i * 0.3) * 15)
            # Taper toward the outer edges so it forms a beautiful oval soundwave shape
            edge_taper = math.sin(((i + 0.5) / num_bars) * math.pi)
            height = base_height + abs(int(wave_modifier * edge_taper))
        else:
            # Subtle breathing idle wave for the mouth
            height = base_height + int(math.sin(frame * 0.05 + i * 0.5) * 3)

        bar_x = start_x + (i * (bar_width + bar_gap))
        bar_y = center_y - (height // 2)
        
        # Core bar drawing
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, height)
        pygame.draw.rect(surface, CYAN_GLOW, bar_rect, border_radius=6)

# Main Loop Setup
running = True

# Create a persistent surface used to blend frame trails (creates the premium motion bloom)
trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.fill(BLACK)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_talking = not is_talking

    # Instead of screen.fill(BLACK), we leave a 75% dark overlay. 
    # This renders beautiful glowing motion trails behind animations.
    fade_overlay = pygame.Surface((WIDTH, HEIGHT))
    fade_overlay.fill((0, 0, 0))
    fade_overlay.set_alpha(75) 
    screen.blit(fade_overlay, (0, 0))
    
    frame_count += 1

    # ---- 1. LOOK AROUND DRIFT LOGIC ----
    if frame_count > next_drift_time:
        if random.random() < 0.3:  # 30% chance to glance slightly somewhere else
            eye_drift_x = random.randint(-12, 12)
            eye_drift_y = random.randint(-6, 6)
            next_drift_time = frame_count + random.randint(60, 180)
        else:
            eye_drift_x, eye_drift_y = 0, 0
            next_drift_time = frame_count + random.randint(120, 300)

    # ---- 2. BLINK LOGIC ----
    if not is_blinking and random.random() < 0.004:
        is_blinking = True
        blink_frame = 0

    eye_open_ratio = 1.0
    if is_blinking:
        blink_frame += 1
        half_duration = BLINK_DURATION / 2
        eye_open_ratio = abs(blink_frame - half_duration) / half_duration
        if blink_frame >= BLINK_DURATION:
            is_blinking = False
            eye_open_ratio = 1.0

    # ---- 3. POSITIONING & SCALE ----
    # Dynamic breathing offsets
    breath_y = math.sin(frame_count * 0.04) * 3
    pulse = math.sin(frame_count * 0.08) * 5

    left_eye_center_x = (WIDTH // 3) + eye_drift_x
    right_eye_center_x = ((WIDTH // 3) * 2) + eye_drift_x
    eye_base_y = (HEIGHT // 2 - 50) + breath_y + eye_drift_y
    mouth_base_y = (HEIGHT // 2 + 85) + (breath_y * 0.5) # Mouth moves slower than eyes for depth

    # Bigger Eye Scale Variables
    BIG_EYE_RADIUS_X = 42  # Considerably widened
    BIG_EYE_RADIUS_Y = 50  # Heightened for prominence
    GLOW_BOUNDS = int(110 + pulse)

    # ---- 4. RENDER ELEMENT PHASES ----
    draw_glowing_eye(screen, left_eye_center_x, eye_base_y, BIG_EYE_RADIUS_X, BIG_EYE_RADIUS_Y, GLOW_BOUNDS, eye_open_ratio)
    draw_glowing_eye(screen, right_eye_center_x, eye_base_y, BIG_EYE_RADIUS_X, BIG_EYE_RADIUS_Y, GLOW_BOUNDS, eye_open_ratio)
    draw_talking_mouth(screen, WIDTH // 2, mouth_base_y, frame_count)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
