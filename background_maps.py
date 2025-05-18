import pygame
import os

class BackgroundMap:
    def __init__(self, name, image_path, preview_path, description):
        self.name = name
        self.image_path = image_path
        self.preview_path = preview_path
        self.description = description
        self.image = None
        self.preview = None
        self.ensure_preview_dir()
        self.load_images()

    def ensure_preview_dir(self):
        preview_dir = os.path.dirname(self.preview_path)
        if not os.path.exists(preview_dir):
            os.makedirs(preview_dir)

    def create_preview(self):
        # Load the original image
        original = pygame.image.load(self.image_path).convert_alpha()
        
        # Create a preview-sized surface
        preview = pygame.Surface((400, 225))  # 16:9 ratio
        
        # Scale the original image to preview size
        scaled = pygame.transform.scale(original, (400, 225))
        
        # Draw the scaled image onto the preview surface
        preview.blit(scaled, (0, 0))
        
        # Save the preview image
        pygame.image.save(preview, self.preview_path)

    def load_images(self):
        try:
            print(f"Loading images for {self.name}...")  # Debug print
            self.image = pygame.image.load(self.image_path).convert_alpha()
            if not os.path.exists(self.preview_path):
                self.create_preview()
            self.preview = pygame.image.load(self.preview_path).convert_alpha()
            print(f"Successfully loaded images for {self.name}")  # Debug print
        except Exception as e:
            print(f"Error loading images for {self.name}: {str(e)}")  # Debug print
            raise

class BackgroundSelector:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_map_index = 0
        # Add hover states for buttons
        self.left_hover = False
        self.right_hover = False
        self.select_hover = False
        self.maps = [
            BackgroundMap(
                "Desert Ruins",
                "assets/images/background/desertmap.jpg",
                "assets/images/background/previews/desert_preview.jpg",
                "A sun-scorched battlefield amidst ancient desert ruins"
            ),
            BackgroundMap(
                "Mystical Forest",
                "assets/images/background/forestmap1.jpg",
                "assets/images/background/previews/forest1_preview.jpg",
                "An enchanted woodland pulsing with ancient magic"
            ),
            BackgroundMap(
                "Frozen Arena",
                "assets/images/background/icemap.jpg",
                "assets/images/background/previews/ice_preview.jpg",
                "A frigid battleground where only the strongest survive"
            ),
            BackgroundMap(
                "Sacred Temple",
                "assets/images/background/templemap.jpg",
                "assets/images/background/previews/temple_preview.jpg",
                "An ancient sanctuary where legends are forged"
            ),
            BackgroundMap(
                "Peaceful Plains",
                "assets/images/background/grassland.jpg",
                "assets/images/background/previews/grassland_preview.jpg",
                "A serene meadow where warriors test their skills"
            ),
            BackgroundMap(
                "Volcanic Fury",
                "assets/images/background/volcano.jpg",
                "assets/images/background/previews/volcano_preview.jpg",
                "A scorching battlefield surrounded by molten lava"
            ),
            BackgroundMap(
                "Murky Swamplands",
                "assets/images/background/Swamp_map.jpg",
                "assets/images/background/previews/swamp_preview.jpg",
                "A treacherous swamp where danger lurks in every shadow"
            ),
            BackgroundMap(
                "Grand Arena",
                "assets/images/background/Arena_map.jpg",
                "assets/images/background/previews/arena_preview.jpg",
                "A magnificent colosseum where champions battle for glory"
            )
        ]
        
        # Load fonts
        self.title_font = pygame.font.Font("assets/fonts/turok.ttf", 60)
        self.desc_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        
        # Button dimensions and properties
        self.PREVIEW_WIDTH = 400
        self.PREVIEW_HEIGHT = 225  # 16:9 ratio
        
        # Navigation buttons - sleek and simple design
        nav_size = 60
        self.left_button = pygame.Rect(50, self.screen_height//2 - nav_size//2, nav_size, nav_size)
        self.right_button = pygame.Rect(self.screen_width - 110, self.screen_height//2 - nav_size//2, nav_size, nav_size)
        self.select_button = pygame.Rect(self.screen_width//2 - 100, self.screen_height - 70, 200, 50)

    def draw_triangle(self, surface, button_rect, pointing_right=True):
        # Calculate triangle points
        button_center_x = button_rect.centerx
        button_center_y = button_rect.centery
        triangle_size = 20  # Size of the triangle
        
        if pointing_right:
            triangle_points = [
                (button_center_x - triangle_size//2, button_center_y - triangle_size//2),
                (button_center_x + triangle_size//2, button_center_y),
                (button_center_x - triangle_size//2, button_center_y + triangle_size//2)
            ]
        else:
            triangle_points = [
                (button_center_x + triangle_size//2, button_center_y - triangle_size//2),
                (button_center_x - triangle_size//2, button_center_y),
                (button_center_x + triangle_size//2, button_center_y + triangle_size//2)
            ]
        
        pygame.draw.polygon(surface, self.WHITE, triangle_points)

    def draw_stylized_button(self, surface, button_rect, text, is_nav=False, is_hovered=False):
        # Create a transparent surface for the button
        button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
        
        # Adjust opacity based on hover state
        base_alpha = 255 if is_hovered else 180  # More opaque when hovered
        bg_alpha = 200 if is_hovered else 160
        
        # Draw button outline with white (more opaque when hovered)
        pygame.draw.rect(button_surface, (255, 255, 255, base_alpha), button_surface.get_rect(), border_radius=10)
        
        # Draw slightly smaller inner rectangle
        inner_rect = button_surface.get_rect().inflate(-4, -4)
        pygame.draw.rect(button_surface, (0, 0, 0, bg_alpha), inner_rect, border_radius=8)
        
        # For navigation buttons, draw triangles instead of text
        if is_nav:
            # Draw triangle with semi-transparent white
            button_center_x = button_surface.get_width() // 2
            button_center_y = button_surface.get_height() // 2
            triangle_size = 20
            
            if text == "LEFT":
                triangle_points = [
                    (button_center_x + triangle_size//2, button_center_y - triangle_size//2),
                    (button_center_x - triangle_size//2, button_center_y),
                    (button_center_x + triangle_size//2, button_center_y + triangle_size//2)
                ]
            else:  # RIGHT
                triangle_points = [
                    (button_center_x - triangle_size//2, button_center_y - triangle_size//2),
                    (button_center_x + triangle_size//2, button_center_y),
                    (button_center_x - triangle_size//2, button_center_y + triangle_size//2)
                ]
            
            # Triangle becomes more opaque when hovered
            triangle_alpha = 255 if is_hovered else 200
            pygame.draw.polygon(button_surface, (255, 255, 255, triangle_alpha), triangle_points)
        else:
            # Draw text for non-navigation buttons
            text_size = 34 if is_hovered else 32  # Slightly larger text when hovered
            text_font = pygame.font.Font("assets/fonts/turok.ttf", text_size)
            text_surface = text_font.render(text, True, (255, 255, 255, 255))
            text_rect = text_surface.get_rect(center=button_surface.get_rect().center)
            button_surface.blit(text_surface, text_rect)
        
        # Add glow effect when hovered
        if is_hovered:
            glow_surface = pygame.Surface((button_rect.width + 10, button_rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 255, 40), glow_surface.get_rect(), border_radius=12)
            surface.blit(glow_surface, glow_surface.get_rect(center=button_rect.center))
        
        # Blit the button surface
        surface.blit(button_surface, button_rect)

    def draw(self, surface):
        # Draw current map as background
        current_map = self.maps[self.current_map_index]
        bg = pygame.transform.scale(current_map.image, (self.screen_width, self.screen_height))
        surface.blit(bg, (0, 0))
        
        # Draw semi-transparent overlay for better visibility
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill(self.BLACK)
        overlay.set_alpha(150)
        surface.blit(overlay, (0, 0))

        # Draw title with glow effect
        title_text = "SELECT YOUR ARENA"
        glow_font = pygame.font.Font("assets/fonts/turok.ttf", 62)
        glow_surf = glow_font.render(title_text, True, (255, 0, 255))
        glow_rect = glow_surf.get_rect(center=(self.screen_width//2, 50))
        surface.blit(glow_surf, glow_rect)
        
        title = self.title_font.render(title_text, True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        surface.blit(title, title_rect)
        
        # Draw map name with neon effect
        map_name = self.title_font.render(current_map.name, True, (0, 255, 255))
        name_rect = map_name.get_rect(center=(self.screen_width//2, 120))
        surface.blit(map_name, name_rect)
        
        # Draw preview with border
        preview = pygame.transform.scale(current_map.preview, (self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT))
        preview_rect = preview.get_rect(center=(self.screen_width//2, self.screen_height//2))
        
        # Draw border
        border = preview_rect.copy()
        border.inflate_ip(10, 10)
        pygame.draw.rect(surface, self.BLACK, border, 3)
        
        surface.blit(preview, preview_rect)
        
        # Draw description with fade effect
        desc_lines = self.wrap_text(current_map.description, 40)
        y_offset = self.screen_height//2 + 150
        for line in desc_lines:
            desc = self.desc_font.render(line, True, (200, 200, 255))
            desc_rect = desc.get_rect(center=(self.screen_width//2, y_offset))
            surface.blit(desc, desc_rect)
            y_offset += 35
        
        # Draw navigation buttons with hover effects
        self.draw_stylized_button(surface, self.left_button, "LEFT", True, self.left_hover)
        self.draw_stylized_button(surface, self.right_button, "RIGHT", True, self.right_hover)
        self.draw_stylized_button(surface, self.select_button, "SELECT", False, self.select_hover)

    def wrap_text(self, text, max_chars):
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            # Update hover states
            self.left_hover = self.left_button.collidepoint(mouse_pos)
            self.right_hover = self.right_button.collidepoint(mouse_pos)
            self.select_hover = self.select_button.collidepoint(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = event.pos
            if self.left_button.collidepoint(mouse_pos):
                self.current_map_index = (self.current_map_index - 1) % len(self.maps)
                print(f"Selected previous map: {self.maps[self.current_map_index].name}")  # Debug print
            elif self.right_button.collidepoint(mouse_pos):
                self.current_map_index = (self.current_map_index + 1) % len(self.maps)
                print(f"Selected next map: {self.maps[self.current_map_index].name}")  # Debug print
            elif self.select_button.collidepoint(mouse_pos):
                selected_map = self.maps[self.current_map_index]
                print(f"Confirmed map selection: {selected_map.name}")  # Debug print
                return selected_map
        return None

    def get_current_map(self):
        current_map = self.maps[self.current_map_index]
        print(f"Getting current map: {current_map.name}")  # Debug print
        return current_map 