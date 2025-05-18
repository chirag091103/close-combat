import pygame
from pygame import mixer
import sys
from background_maps import BackgroundSelector

# Initialize Pygame
pygame.init()
mixer.init()

# Set up display
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("close combat - Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Font
menu_font = pygame.font.Font("assets/fonts/turok.ttf", 60)
player_label_font = pygame.font.Font("assets/fonts/turok.ttf", 35)
button_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
char_name_font = pygame.font.Font("assets/fonts/turok.ttf", 25)

# Load background
main_menu_bg = pygame.image.load("assets/images/background/main_menu_bg.jpg").convert_alpha()
player_select_bg = pygame.image.load("assets/images/background/player_selection_bg2.jpg").convert_alpha()

# Load character sprite images for selection buttons
warrior_img = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_img = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
huntress_img = pygame.image.load("assets/images/Huntress/Sprites/huntress.png").convert_alpha()
king_img = pygame.image.load("assets/images/Medieval King Pack 2/Sprites/king.png").convert_alpha()
hero_knight_img = pygame.image.load("assets/images/Hero Knight/Sprites/hero_knight.png").convert_alpha()
martial_hero_img = pygame.image.load("assets/images/Martial Hero/Sprites/martial_hero.png").convert_alpha()

# Load character display images for preview
warrior_display = pygame.image.load("assets/images/warrior/warrior_display.jpg").convert_alpha()
wizard_display = pygame.image.load("assets/images/wizard/wizard_display.jpg").convert_alpha()
huntress_display = pygame.image.load("assets/images/Huntress/huntress_display.jpg").convert_alpha()
king_display = pygame.image.load("assets/images/Medieval King Pack 2/hero king_display.jpg").convert_alpha()
hero_knight_display = pygame.image.load("assets/images/Hero Knight/hero knight_display.jpg").convert_alpha()
martial_hero_display = pygame.image.load("assets/images/Martial Hero/martial hero_display.jpg").convert_alpha()

# Dictionary to map character names to their display images
CHARACTER_DISPLAYS = {
    "WARRIOR": warrior_display,
    "WIZARD": wizard_display,
    "HUNTRESS": huntress_display,
    "KING": king_display,
    "HERO_KNIGHT": hero_knight_display,
    "MARTIAL_HERO": martial_hero_display
}

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface):
        color = YELLOW if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=12)
        text_surface = button_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.is_hovered:
                return True
        return False

class CharacterSelect:
    def __init__(self):
        self.p1_selected = None
        self.p2_selected = None
        self.p1_confirmed = False
        self.p2_confirmed = False
        self.current_player = 1
        self.characters = ["WARRIOR", "WIZARD", "HUNTRESS", "KING", "HERO_KNIGHT", "MARTIAL_HERO"]
        
        # Dictionary to map full names to display names
        self.display_names = {
            "WARRIOR": "WARRIOR",
            "WIZARD": "WIZARD",
            "HUNTRESS": "HUNTER",
            "KING": "KING",
            "HERO_KNIGHT": "KNIGHT",
            "MARTIAL_HERO": "MARTIAL"
        }
        
        # Preview sections dimensions
        self.preview_width = 150
        self.preview_height = 150
        self.preview_y = 180
        # Adjust x positions for more space between boxes
        self.p1_preview_x = 200
        self.p2_preview_x = SCREEN_WIDTH - 350
        
        # Calculate positions for character selection buttons
        self.button_width = 130  # Increased from 100 to 130
        self.button_height = 50
        self.button_spacing = 35  # Increased from 20 to 35
        
        # Calculate total width needed for all buttons
        total_buttons_width = (self.button_width * len(self.characters)) + (self.button_spacing * (len(self.characters) - 1))
        self.start_x = (SCREEN_WIDTH - total_buttons_width) // 2
        
        # Create character selection buttons
        self.char_buttons = {}
        for i, char in enumerate(self.characters):
            x = self.start_x + (self.button_width + self.button_spacing) * i
            y = SCREEN_HEIGHT - 80
            button_text = self.display_names[char]
            self.char_buttons[char] = Button(x, y, self.button_width, self.button_height, button_text, RED)

        # Create confirm buttons for each player
        self.p1_confirm_button = Button(self.p1_preview_x + 25, self.preview_y + self.preview_height + 60, 100, 40, "OKAY", RED)
        self.p2_confirm_button = Button(self.p2_preview_x + 25, self.preview_y + self.preview_height + 60, 100, 40, "OKAY", RED)
        
        # Start button (only shown when both players confirm)
        self.start_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 150, 200, 50, "START", RED)

    def draw(self, surface):
        # Draw background
        scaled_bg = pygame.transform.scale(player_select_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(scaled_bg, (0, 0))

        # Add semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(120)
        surface.blit(overlay, (0, 0))

        # Draw title with glow effect
        title_text = "SELECT YOUR FIGHTERS"
        # Glow effect
        glow_font = pygame.font.Font("assets/fonts/turok.ttf", 72)
        glow_surf = glow_font.render(title_text, True, (255, 0, 255))
        glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH//2, 50))
        surface.blit(glow_surf, glow_rect)
        # Main text
        title = menu_font.render(title_text, True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        surface.blit(title, title_rect)

        # Draw player labels with glow
        for label, x in [("PLAYER 1", self.p1_preview_x), ("PLAYER 2", self.p2_preview_x)]:
            # Main text only, no glow
            text = player_label_font.render(label, True, WHITE)
            text_rect = text.get_rect(midtop=(x + self.preview_width//2, self.preview_y - 60))
            surface.blit(text, text_rect)

        # Draw VS text with glow
        vs_glow = glow_font.render("VS", True, (255, 255, 0))
        vs_rect = vs_glow.get_rect(center=(SCREEN_WIDTH//2, self.preview_y + self.preview_height//2))
        surface.blit(vs_glow, vs_rect)
        vs_text = menu_font.render("VS", True, WHITE)
        vs_rect = vs_text.get_rect(center=(SCREEN_WIDTH//2, self.preview_y + self.preview_height//2))
        surface.blit(vs_text, vs_rect)

        # Draw preview boxes and character displays
        for preview_x, selected, confirmed, confirm_button in [
            (self.p1_preview_x, self.p1_selected, self.p1_confirmed, self.p1_confirm_button),
            (self.p2_preview_x, self.p2_selected, self.p2_confirmed, self.p2_confirm_button)
        ]:
            # Draw preview box with border and background
            preview_rect = pygame.Rect(preview_x, self.preview_y, self.preview_width, self.preview_height)
            pygame.draw.rect(surface, (30, 30, 30), preview_rect)
            
            # Change border color based on confirmation status
            border_color = (0, 255, 0) if confirmed else BLACK  # Changed from purple to black when not confirmed
            pygame.draw.rect(surface, border_color, preview_rect, 3)

            # Draw character preview if selected
            if selected:
                display_img = CHARACTER_DISPLAYS[selected]
                img_rect = display_img.get_rect()
                scale = min(self.preview_width / img_rect.width, self.preview_height / img_rect.height)
                new_width = int(img_rect.width * scale * 0.95)
                new_height = int(img_rect.height * scale * 0.95)
                scaled_img = pygame.transform.scale(display_img, (new_width, new_height))
                img_x = preview_x + (self.preview_width - new_width) // 2
                img_y = self.preview_y + (self.preview_height - new_height) // 2
                surface.blit(scaled_img, (img_x, img_y))

                # Draw character name below the preview box
                name_text = self.display_names[selected]
                name_surf = char_name_font.render(name_text, True, WHITE)
                name_rect = name_surf.get_rect(midtop=(preview_x + self.preview_width//2, self.preview_y + self.preview_height + 10))
                surface.blit(name_surf, name_rect)

                # Draw confirm button if not confirmed
                if not confirmed:
                    confirm_button.draw(surface)
                else:
                    # Draw "CONFIRMED" text
                    confirmed_text = button_font.render("OKAY!", True, (0, 255, 0))
                    confirmed_rect = confirmed_text.get_rect(center=(confirm_button.rect.center))
                    surface.blit(confirmed_text, confirmed_rect)

        # Draw character selection buttons with background highlight
        for char, button in self.char_buttons.items():
            highlight_rect = pygame.Rect(button.rect.x - 2, button.rect.y - 2,
                                      button.rect.width + 4, button.rect.height + 4)
            
            # Highlight based on selection and confirmation
            if char == self.p1_selected and not self.p1_confirmed:
                pygame.draw.rect(surface, (255, 0, 255), highlight_rect, 3, border_radius=12)
            elif char == self.p2_selected and not self.p2_confirmed:
                pygame.draw.rect(surface, (255, 255, 0), highlight_rect, 3, border_radius=12)
            elif char == self.p1_selected and self.p1_confirmed:
                pygame.draw.rect(surface, (0, 255, 0), highlight_rect, 3, border_radius=12)
            elif char == self.p2_selected and self.p2_confirmed:
                pygame.draw.rect(surface, (0, 255, 0), highlight_rect, 3, border_radius=12)
            else:
                pygame.draw.rect(surface, (255, 0, 255), highlight_rect, 2, border_radius=12)
            
            button.draw(surface)

        # Draw current player indicator if not both confirmed
        if not (self.p1_confirmed and self.p2_confirmed):
            if not self.p1_confirmed:
                player_text = "PLAYER 1 SELECT"
                color = WHITE  # Changed from purple to white
            elif not self.p2_confirmed:
                player_text = "PLAYER 2 SELECT"
                color = WHITE  # Changed from yellow to white
            # Main text only, no glow
            text = player_label_font.render(player_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 160))
            surface.blit(text, text_rect)

        # Draw start button only if both players have confirmed
        if self.p1_confirmed and self.p2_confirmed:
            self.start_button.draw(surface)

    def handle_event(self, event):
        # Handle character selection
        if not (self.p1_confirmed and self.p2_confirmed):
            for char, button in self.char_buttons.items():
                if button.handle_event(event):
                    # Allow selection only if player hasn't confirmed
                    if not self.p1_confirmed and (self.current_player == 1 or self.p1_selected == char):
                        self.p1_selected = None if self.p1_selected == char else char
                        self.current_player = 1
                    elif not self.p2_confirmed and (self.current_player == 2 or self.p2_selected == char):
                        self.p2_selected = None if self.p2_selected == char else char
                        self.current_player = 2
                    return False

        # Handle confirm buttons
        if self.p1_selected and not self.p1_confirmed:
            if self.p1_confirm_button.handle_event(event):
                self.p1_confirmed = True
                self.current_player = 2
                return False

        if self.p2_selected and not self.p2_confirmed:
            if self.p2_confirm_button.handle_event(event):
                self.p2_confirmed = True
                return False

        # Handle start button
        if self.p1_confirmed and self.p2_confirmed:
            if self.start_button.handle_event(event):
                return True

        return False

class MainMenu:
    def __init__(self):
        self.play_button = Button(400, 200, 200, 50, "PLAY", RED)
        self.quit_button = Button(400, 300, 200, 50, "QUIT", RED)

    def draw(self, surface):
        # Draw main menu background
        scaled_bg = pygame.transform.scale(main_menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(scaled_bg, (0, 0))

        # Add semi-transparent overlay for better text readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(100)  # Adjust transparency (0-255)
        surface.blit(overlay, (0, 0))

        # Draw title with subtle glow effect
        title_text = "CLOSE COMBAT"
        # Draw glow
        glow_font = pygame.font.Font("assets/fonts/turok.ttf", 65)  # Decreased from 82
        glow_surf = glow_font.render(title_text, True, (255, 0, 255))  # Pink glow
        glow_surf.set_alpha(150)  # Make glow more subtle
        glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(glow_surf, glow_rect)
        # Draw main text
        title = menu_font.render(title_text, True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(title, title_rect)

        # Draw buttons
        self.play_button.draw(surface)
        self.quit_button.draw(surface)

    def handle_event(self, event):
        if self.play_button.handle_event(event):
            return "PLAY"
        elif self.quit_button.handle_event(event):
            return "QUIT"
        return None

def main_menu():
    clock = pygame.time.Clock()
    menu = MainMenu()
    char_select = CharacterSelect()
    bg_selector = BackgroundSelector(SCREEN_WIDTH, SCREEN_HEIGHT)
    current_screen = "MENU"
    selected_chars = None

    # Background music
    pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_screen == "MENU":
                result = menu.handle_event(event)
                if result == "PLAY":
                    current_screen = "CHARACTER_SELECT"
                elif result == "QUIT":
                    pygame.quit()
                    sys.exit()
            
            elif current_screen == "CHARACTER_SELECT":
                if char_select.handle_event(event):
                    selected_chars = (char_select.p1_selected, char_select.p2_selected)
                    current_screen = "BACKGROUND_SELECT"
            
            elif current_screen == "BACKGROUND_SELECT":
                selected_bg = bg_selector.handle_event(event)
                if selected_bg is not None:
                    return selected_chars[0], selected_chars[1], selected_bg

        screen.fill(BLACK)
        
        if current_screen == "MENU":
            menu.draw(screen)
        elif current_screen == "CHARACTER_SELECT":
            char_select.draw(screen)
        elif current_screen == "BACKGROUND_SELECT":
            bg_selector.draw(screen)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    result = main_menu()
    if result:
        p1_char, p2_char, selected_bg = result
        print(f"Selected: Player 1: {p1_char}, Player 2: {p2_char}, Background: {selected_bg.name}") 