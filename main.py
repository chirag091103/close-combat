import pygame
from pygame import mixer
from fighter import Fighter
import main_menu

def start_game(p1_character, p2_character, background_map):
    print("Starting game with:", p1_character, p2_character, background_map.name)  # Debug print
    mixer.init()
    pygame.init()

    #create game window
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("close")

    #set framerate
    clock = pygame.time.Clock()
    FPS = 60

    #define colours
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    #define game variables
    intro_count = 5
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]#player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    #define fighter variables
    WARRIOR_SIZE = 162
    WARRIOR_SCALE = 4
    WARRIOR_OFFSET = [72, 62]
    WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
    WIZARD_SIZE = 250
    WIZARD_SCALE = 3
    WIZARD_OFFSET = [112, 113]
    WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
    HUNTRESS_SIZE = 150
    HUNTRESS_SCALE = 3.5
    HUNTRESS_OFFSET = [50, 45]
    HUNTRESS_DATA = [HUNTRESS_SIZE, HUNTRESS_SCALE, HUNTRESS_OFFSET]
    KING_SIZE = 160
    KING_SCALE = 3
    KING_OFFSET = [60, 70]
    KING_DATA = [KING_SIZE, KING_SCALE, KING_OFFSET]
    HERO_KNIGHT_SIZE = 180
    HERO_KNIGHT_SCALE = 3
    HERO_KNIGHT_OFFSET = [70, 55]
    HERO_KNIGHT_DATA = [HERO_KNIGHT_SIZE, HERO_KNIGHT_SCALE, HERO_KNIGHT_OFFSET]
    MARTIAL_HERO_SIZE = 200
    MARTIAL_HERO_SCALE = 3
    MARTIAL_HERO_OFFSET = [80, 62]
    MARTIAL_HERO_DATA = [MARTIAL_HERO_SIZE, MARTIAL_HERO_SCALE, MARTIAL_HERO_OFFSET]

    #load music and sounds
    pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.5)
    magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    magic_fx.set_volume(0.75)

    #load spritesheets
    warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
    huntress_sheet = pygame.image.load("assets/images/Huntress/Sprites/huntress.png").convert_alpha()
    king_sheet = pygame.image.load("assets/images/Medieval King Pack 2/Sprites/king.png").convert_alpha()
    hero_knight_sheet = pygame.image.load("assets/images/Hero Knight/Sprites/hero_knight.png").convert_alpha()
    martial_hero_sheet = pygame.image.load("assets/images/Martial Hero/Sprites/martial_hero.png").convert_alpha()

    #load victory image
    victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

    #define number of steps in each animation
    WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
    WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
    HUNTRESS_ANIMATION_STEPS = [8, 8, 2, 5, 5, 3, 8]
    KING_ANIMATION_STEPS = [8, 8, 2, 4, 4, 4, 6]
    HERO_KNIGHT_ANIMATION_STEPS = [11, 8, 3, 7, 7, 4, 11]
    MARTIAL_HERO_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]

    #define font
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
    control_font = pygame.font.Font("assets/fonts/turok.ttf", 20)

    #function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function for drawing control keys
    def draw_controls():
        # Player 1 Controls
        draw_text("PLAYER 1 CONTROLS:", control_font, WHITE, 50, 200)
        draw_text("Move: A / D", control_font, YELLOW, 50, 230)
        draw_text("Jump: W", control_font, YELLOW, 50, 260)
        draw_text("Attack 1: R", control_font, YELLOW, 50, 290)
        draw_text("Attack 2: T", control_font, YELLOW, 50, 320)
        
        # Player 2 Controls
        draw_text("PLAYER 2 CONTROLS:", control_font, WHITE, SCREEN_WIDTH - 250, 200)
        draw_text("Move: Left / Right", control_font, YELLOW, SCREEN_WIDTH - 250, 230)
        draw_text("Jump: Up", control_font, YELLOW, SCREEN_WIDTH - 250, 260)
        draw_text("Attack 1: Num 1", control_font, YELLOW, SCREEN_WIDTH - 250, 290)
        draw_text("Attack 2: Num 2", control_font, YELLOW, SCREEN_WIDTH - 250, 320)

    #function for drawing background
    def draw_bg():
        try:
            if not background_map or not background_map.image:
                print("Error: Background map or image is None")  # Debug print
                return
            scaled_bg = pygame.transform.scale(background_map.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))
        except Exception as e:
            print(f"Error drawing background: {str(e)}")  # Debug print
            # Fill with black as fallback
            screen.fill((0, 0, 0))

    #function for drawing fighter health bars
    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

    # Create fighters based on selection
    def create_fighter(player_num, x_pos, y_pos, character):
        if character == "WARRIOR":
            return Fighter(player_num, x_pos, y_pos, player_num == 2, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
        elif character == "WIZARD":
            return Fighter(player_num, x_pos, y_pos, player_num == 2, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
        elif character == "HUNTRESS":
            return Fighter(player_num, x_pos, y_pos, player_num == 2, HUNTRESS_DATA, huntress_sheet, HUNTRESS_ANIMATION_STEPS, sword_fx)
        elif character == "KING":
            return Fighter(player_num, x_pos, y_pos, player_num == 2, KING_DATA, king_sheet, KING_ANIMATION_STEPS, sword_fx)
        elif character == "HERO_KNIGHT":
            return Fighter(player_num, x_pos, y_pos, player_num == 2, HERO_KNIGHT_DATA, hero_knight_sheet, HERO_KNIGHT_ANIMATION_STEPS, sword_fx)
        else:  # MARTIAL_HERO
            return Fighter(player_num, x_pos, y_pos, player_num == 2, MARTIAL_HERO_DATA, martial_hero_sheet, MARTIAL_HERO_ANIMATION_STEPS, sword_fx)

    #create two instances of fighters based on selection
    fighter_1 = create_fighter(1, 250, 310, p1_character)
    fighter_2 = create_fighter(2, 650, 310, p2_character)

    #game loop
    run = True
    while run:
        clock.tick(FPS)

        #draw background
        draw_bg()

        #show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            #display control keys
            draw_controls()
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters
        fighter_1.update()
        fighter_2.update()

        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            #display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 5
                fighter_1 = create_fighter(1, 250, 310, p1_character)
                fighter_2 = create_fighter(2, 650, 310, p2_character)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #update display
        pygame.display.update()

    #exit pygame
    pygame.quit()

if __name__ == "__main__":
    # Initialize Pygame for the menu
    pygame.init()
    mixer.init()
    
    # Get selections from menu
    result = main_menu.main_menu()
    
    if result:
        p1_char, p2_char, selected_bg = result
        # Start the actual game
        start_game(p1_char, p2_char, selected_bg)