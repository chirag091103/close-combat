import pygame
import os

def combine_knight_sprites():
    pygame.init()
    pygame.display.set_mode((1, 1))
    
    # Define the sprite order and their files with their frame counts
    sprite_files = [
        ("Idle.png", 11),      # idle - 11 frames
        ("Run.png", 8),        # run - 8 frames
        ("Jump.png", 3),       # jump - 3 frames
        ("Attack1.png", 7),    # attack1 - 7 frames
        ("Attack2.png", 7),    # attack2 - 7 frames
        ("Take Hit.png", 4),   # hit - 4 frames
        ("Death.png", 11)      # death - 11 frames
    ]
    
    base_path = "assets/images/Hero Knight/Sprites"
    
    # First pass: determine the correct frame size
    max_height = 0
    frame_width = 0
    
    print("Analyzing sprite dimensions:")
    for file, frames in sprite_files:
        path = os.path.join(base_path, file)
        sprite = pygame.image.load(path).convert_alpha()
        height = sprite.get_height()
        width = sprite.get_width()
        current_frame_width = width // frames
        print(f"{file}: {width}x{height} ({frames} frames, {current_frame_width}px per frame)")
        max_height = max(max_height, height)
        frame_width = max(frame_width, current_frame_width)
    
    frame_size = max(max_height, frame_width)
    max_frames = 11  # Maximum frames from all animations
    
    print(f"\nUsing frame size: {frame_size}x{frame_size}")
    
    # Create the combined surface (11 frames wide, 7 animations high)
    combined = pygame.Surface((frame_size * max_frames, frame_size * len(sprite_files)), pygame.SRCALPHA)
    
    # Process each animation
    for y, (file, num_frames) in enumerate(sprite_files):
        path = os.path.join(base_path, file)
        sprite = pygame.image.load(path).convert_alpha()
        sprite_width = sprite.get_width()
        sprite_height = sprite.get_height()
        
        # Calculate the width of each frame for this animation
        frame_width = sprite_width // num_frames
        print(f"Processing {file}: {num_frames} frames, {frame_width}px wide each")
        
        # Extract and position each frame
        for x in range(num_frames):
            # Create a temporary surface for the frame
            temp_surface = pygame.Surface((frame_size, frame_size), pygame.SRCALPHA)
            
            # Extract the frame
            frame = sprite.subsurface(x * frame_width, 0, frame_width, sprite_height)
            
            # Calculate position to center the frame in the temp surface
            pos_x = (frame_size - frame_width) // 2
            pos_y = (frame_size - sprite_height) // 2
            
            # Blit the frame onto the temp surface
            temp_surface.blit(frame, (pos_x, pos_y))
            
            # Blit the temp surface onto the combined surface
            combined.blit(temp_surface, (x * frame_size, y * frame_size))
        
        # If this animation has fewer frames than max_frames, repeat the last frame
        for x in range(num_frames, max_frames):
            combined.blit(temp_surface, (x * frame_size, y * frame_size))
    
    # Save the combined sprite sheet
    pygame.image.save(combined, os.path.join(base_path, "hero_knight.png"))
    print(f"\nCreated sprite sheet: {max_frames * frame_size}x{len(sprite_files) * frame_size}")
    pygame.quit()

if __name__ == "__main__":
    combine_knight_sprites() 