import pygame
import os

def combine_huntress_sprites():
    pygame.init()
    pygame.display.set_mode((1, 1))
    
    # Define the sprite order and their files
    sprite_files = [
        "Idle.png",      # idle - 8 frames
        "Run.png",       # run - 8 frames
        "Jump.png",      # jump - 2 frames
        "Attack1.png",   # attack1 - 5 frames
        "Attack2.png",   # attack2 - 5 frames
        "Take hit.png",  # hit - 3 frames
        "Death.png"      # death - 8 frames
    ]
    
    base_path = "assets/images/Huntress/Sprites"
    frame_size = 150  # All sprites are 150 pixels high
    max_frames = 8    # Maximum number of frames in any animation
    
    # Create the combined surface (8 frames wide, 7 animations high)
    combined = pygame.Surface((frame_size * max_frames, frame_size * len(sprite_files)), pygame.SRCALPHA)
    
    # Process each animation
    for y, file in enumerate(sprite_files):
        path = os.path.join(base_path, file)
        sprite = pygame.image.load(path).convert_alpha()
        
        # Calculate number of frames in this animation
        num_frames = sprite.get_width() // frame_size
        print(f"{file}: {num_frames} frames")
        
        # Extract and position each frame
        for x in range(num_frames):
            frame = sprite.subsurface(x * frame_size, 0, frame_size, frame_size)
            combined.blit(frame, (x * frame_size, y * frame_size))
        
        # If this animation has fewer frames than max_frames, repeat the last frame
        last_frame = sprite.subsurface((num_frames - 1) * frame_size, 0, frame_size, frame_size)
        for x in range(num_frames, max_frames):
            combined.blit(last_frame, (x * frame_size, y * frame_size))
    
    # Save the combined sprite sheet
    pygame.image.save(combined, os.path.join(base_path, "huntress.png"))
    print(f"\nCreated sprite sheet: {max_frames * frame_size}x{len(sprite_files) * frame_size}")
    pygame.quit()

if __name__ == "__main__":
    combine_huntress_sprites() 