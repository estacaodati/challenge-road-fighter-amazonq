import pygame
import random
import sys
import os
import json

# Initialize Pygame and mixer
pygame.init()
try:
    # Try different audio settings for better compatibility
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.mixer.init()
    SOUND_ENABLED = True
    print("Audio system initialized successfully!")
except pygame.error as e:
    print(f"Audio not available - running in silent mode: {e}")
    SOUND_ENABLED = False

class ScoreManager:
    def __init__(self):
        self.scores_file = "high_scores.json"
        self.high_scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    scores = json.load(f)
                    print(f"Loaded {len(scores)} high scores")
                    return scores
            else:
                print("No high scores file found, starting fresh")
                return []
        except Exception as e:
            print(f"Error loading scores: {e}")
            return []
    
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
            print(f"Saved {len(self.high_scores)} high scores")
        except Exception as e:
            print(f"Error saving scores: {e}")
    
    def add_score(self, score, distance):
        """Add a new score and keep top 10"""
        new_score = {
            'score': int(score),
            'distance': int(distance),
            'date': pygame.time.get_ticks()  # Simple timestamp
        }
        
        self.high_scores.append(new_score)
        # Sort by score (highest first)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        # Keep only top 10
        self.high_scores = self.high_scores[:10]
        self.save_scores()
        
        print(f"Added score: {int(score)} (Distance: {int(distance)} km)")
    
    def get_high_score(self):
        """Get the highest score"""
        if self.high_scores:
            return self.high_scores[0]['score']
        return 0
    
    def is_high_score(self, score):
        """Check if this score makes it to top 10"""
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1]['score']

# Sprite Manager Class
class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.load_all_sprites()
    
    def load_sprite(self, filename, size=(75, 75)):
        """Load a sprite with automatic resizing and aspect ratio preservation"""
        try:
            sprite_path = os.path.join("sprites", filename)
            if os.path.exists(sprite_path):
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, size)
                print(f"Loaded sprite: {filename} -> {size}")
                return sprite
            else:
                print(f"Sprite not found: {filename}")
                return None
        except Exception as e:
            print(f"Error loading sprite {filename}: {e}")
            return None
    
    def load_all_sprites(self):
        """Load all available sprites with proper aspect ratio preservation"""
        print("Loading sprites with proper sizing...")
        
        # Car sprites: 256x256 -> maintain aspect ratio, scale to fit game
        # Target height for cars: 75 pixels, calculate width proportionally
        car_target_height = 75
        car_aspect_ratio = 1.0  # 256x256 is square
        car_target_width = int(car_target_height * car_aspect_ratio)  # 75x75
        
        # Player car sprite
        self.sprites['player_car'] = self.load_sprite("player_car.png", (car_target_width, car_target_height))
        
        # Enemy car sprites
        self.sprites['enemy_static'] = self.load_sprite("enemy_static.png", (car_target_width, car_target_height))
        self.sprites['enemy_police'] = self.load_sprite("enemy_police.png", (car_target_width, car_target_height))
        self.sprites['enemy_sports'] = self.load_sprite("enemy_sports.png", (car_target_width, car_target_height))
        
        # Fuel station sprite: 500x500 -> maintain aspect ratio
        # Target height for fuel station: 100 pixels, calculate width proportionally
        fuel_target_height = 100
        fuel_aspect_ratio = 1.0  # 500x500 is square
        fuel_target_width = int(fuel_target_height * fuel_aspect_ratio)  # 100x100
        
        self.sprites['fuel_station'] = self.load_sprite("fuel_station.png", (fuel_target_width, fuel_target_height))
        
        # Amazon Q logo for splash screen - keep original 1024x1024 size
        self.sprites['amazonQ'] = self.load_sprite("amazonQ.png", (1024, 1024))  # Original size
        
        print(f"Loaded {len([s for s in self.sprites.values() if s is not None])} sprites successfully")
        print(f"Car sprites sized to: {car_target_width}x{car_target_height}")
        print(f"Fuel station sized to: {fuel_target_width}x{fuel_target_height}")
    
    def get_sprite(self, name):
        """Get a sprite by name"""
        return self.sprites.get(name, None)

# Constants
FPS = 60
SCREEN_WIDTH = 1400  # Increased for better fullscreen usage
SCREEN_HEIGHT = 900  # Increased for better fullscreen usage
GAME_AREA_WIDTH = 1400  # Match screen width
GAME_AREA_HEIGHT = 900  # Match screen height
FULLSCREEN_WIDTH = 1920  # Fullscreen dimensions
FULLSCREEN_HEIGHT = 1080

# Calculate game area position (centered on fullscreen)
GAME_OFFSET_X = (FULLSCREEN_WIDTH - GAME_AREA_WIDTH) // 2
GAME_OFFSET_Y = (FULLSCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

class Game:
    def __init__(self):
        # Set up fullscreen display
        self.fullscreen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), pygame.FULLSCREEN)
        
        # Create game surface (centered on fullscreen)
        self.screen = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        
        pygame.display.set_caption("Road Fighter")
        self.clock = pygame.time.Clock()
        
        # Load custom font
        try:
            self.font_large = pygame.font.Font("fonts/Pixeled.ttf", 48)
            self.font_medium = pygame.font.Font("fonts/Pixeled.ttf", 32)
            self.font_small = pygame.font.Font("fonts/Pixeled.ttf", 24)
            self.font_tiny = pygame.font.Font("fonts/Pixeled.ttf", 16)
            print("Loaded custom Pixeled font successfully!")
        except Exception as e:
            print(f"Could not load custom font: {e}")
            # Fallback to default fonts
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 36)
            self.font_tiny = pygame.font.Font(None, 24)
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        
        # Initialize score manager
        self.score_manager = ScoreManager()
        
        self.state = "SPLASH"  # Start with splash screen
        self.splash_timer = 0  # Timer for splash screen
        self.menu_selection = 0
        self.pause_selection = 0  # For pause menu
        self.road_offset = 0
        self.how_to_play_timer = 0
        self.game_over_timer = 0  # Timer for game over screen
        
        # Game statistics
        self.distance = 0
        self.high_score = self.score_manager.get_high_score()  # Load from saved scores
        
        # Game objects
        self.player = None
        self.enemy_cars = []
        self.fuel = 100
        self.score = 0
        self.speed = 2
        self.damage_flash = 0
        self.slide_effect = 0
        self.slide_direction = 0
        self.control_loss = 0
        self.spin_angle = 0
        
        # Visual sound feedback (since audio isn't available)
        self.sound_feedback = ""
        self.sound_feedback_timer = 0
        self.sound_feedback_color = WHITE
        self.sound_feedback_size = 'medium'
        
        # Load sounds (will be disabled but structure remains)
        self.load_sounds()
        
        # Start menu music when game starts
        self.play_menu_music()
    
    def load_sounds(self):
        """Load sound effects and music from MP3/WAV files in sounds folder"""
        global SOUND_ENABLED
        
        if not SOUND_ENABLED:
            self.sounds = {}
            self.music_files = {}
            print("Skipping sound loading - audio disabled")
            return
            
        try:
            print("Loading sounds from sounds/ folder...")
            self.sounds = {}
            self.music_files = {}
            
            # Load sound effects (MP3 files)
            sound_files = {
                'collision': 'sounds/collision.mp3',
                'pickup': 'sounds/pickup.mp3',
                'selection': 'sounds/selection.mp3'
            }
            
            # Load music files (for pygame.mixer.music)
            self.music_files = {
                'menu': 'sounds/menu.mp3',
                'background': 'sounds/background.mp3'
            }
            
            # Load sound effects
            for sound_name, filename in sound_files.items():
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filename)
                    print(f"Loaded {filename}")
                except Exception as e:
                    print(f"Could not load {filename}: {e}")
                    # Fallback to generated sound
                    if sound_name == 'selection':
                        self.sounds[sound_name] = self.create_simple_tone(600, 0.1, 0.2)
                    elif sound_name == 'pickup':
                        self.sounds[sound_name] = self.create_simple_tone(800, 0.2, 0.3)
                    elif sound_name == 'collision':
                        self.sounds[sound_name] = self.create_simple_tone(300, 0.3, 0.5)
                    print(f"Using generated sound for {sound_name}")
            
            # Check music files exist
            for music_name, filename in self.music_files.items():
                try:
                    # Just check if file exists, don't load it yet
                    with open(filename, 'rb'):
                        print(f"Found music file: {filename}")
                except Exception as e:
                    print(f"Could not find music file {filename}: {e}")
                    self.music_files[music_name] = None
            
            print("Sound loading completed!")
            
        except Exception as e:
            print(f"Could not load sounds: {e}")
            self.sounds = {}
            self.music_files = {}
            SOUND_ENABLED = False
    
    def create_simple_tone(self, frequency, duration, volume):
        """Create a simple tone using pygame's built-in capabilities"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        # Create simple sine wave
        arr = []
        for i in range(frames):
            # Calculate sine wave value
            time_point = float(i) / sample_rate
            wave_value = volume * 32767 * pygame.math.sin(frequency * 2 * pygame.math.pi * time_point)
            
            # Apply fade out to avoid clicks
            fade = 1.0 - (float(i) / frames)
            wave_value = int(wave_value * fade)
            
            # Stereo sound (left and right channels)
            arr.append([wave_value, wave_value])
        
        # Convert to pygame sound
        sound_array = pygame.array.array('h', arr)
        return pygame.sndarray.make_sound(sound_array)
    
    def play_menu_music(self):
        """Start menu music (loops during menu)"""
        if not SOUND_ENABLED:
            print("Menu music would be playing (audio disabled)")
            return
            
        try:
            if self.music_files.get('menu'):
                print("Starting menu music...")
                pygame.mixer.music.load(self.music_files['menu'])
                pygame.mixer.music.set_volume(0.4)  # Medium volume for menu
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print("Menu music started successfully!")
            else:
                print("Menu music file not available")
        except Exception as e:
            print(f"Could not start menu music: {e}")
    
    def play_background_music(self):
        """Start background music during gameplay"""
        if not SOUND_ENABLED:
            print("Background music would be playing (audio disabled)")
            return
            
        try:
            if self.music_files.get('background'):
                print("Starting background music...")
                pygame.mixer.music.load(self.music_files['background'])
                pygame.mixer.music.set_volume(0.3)  # Lower volume during gameplay
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print("Background music started successfully!")
            else:
                print("Background music file not available")
        except Exception as e:
            print(f"Could not start background music: {e}")
    
    def stop_music(self):
        """Stop currently playing music"""
        if SOUND_ENABLED:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                print(f"Could not stop music: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect or show visual feedback with markdown-style icons"""
        if SOUND_ENABLED and sound_name in self.sounds:
            try:
                print(f"Playing sound: {sound_name}")
                pygame.mixer.Sound.play(self.sounds[sound_name])
            except Exception as e:
                print(f"Could not play sound {sound_name}: {e}")
        
        # Enhanced visual feedback with plain text
        sound_effects = {
            'collision': {
                'text': 'CRASH!',
                'color': RED,
                'size': 'large'
            },
            'pickup': {
                'text': '+FUEL',
                'color': GREEN,
                'size': 'medium'
            },
            'selection': {
                'text': 'SELECT',
                'color': YELLOW,
                'size': 'small'
            }
        }
        
        if sound_name in sound_effects:
            effect = sound_effects[sound_name]
            self.sound_feedback = effect['text']
            self.sound_feedback_color = effect['color']
            self.sound_feedback_size = effect['size']
            self.sound_feedback_timer = 90 if effect['size'] == 'large' else 60 if effect['size'] == 'medium' else 30
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:  # Toggle fullscreen
                        self.toggle_fullscreen()
                    # Remove the ESC handling from here - let each state handle it
                
                if self.state == "SPLASH":
                    self.handle_splash_events(event)
                elif self.state == "MENU":
                    self.handle_menu_events(event)
                elif self.state == "GAME":
                    self.handle_game_events(event)
                elif self.state == "PAUSED":
                    self.handle_pause_events(event)
                elif self.state == "CREDITS":
                    self.handle_credits_events(event)
                elif self.state == "HOW_TO_PLAY":
                    self.handle_how_to_play_events(event)
                elif self.state == "GAME_OVER":
                    self.handle_game_over_events(event)
            
            self.update()
            self.draw()
            
            # Blit game surface to fullscreen and display
            self.fullscreen.fill((0, 0, 0))  # Black background
            self.fullscreen.blit(self.screen, (GAME_OFFSET_X, GAME_OFFSET_Y))
            pygame.display.flip()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def update(self):
        """Update game state"""
        if self.state == "SPLASH":
            self.update_splash()
        elif self.state == "GAME":
            self.update_game()
        elif self.state == "HOW_TO_PLAY":
            self.update_how_to_play()
        # Note: PAUSED state doesn't update game logic
        """Toggle between fullscreen and windowed mode"""
        try:
            if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
                self.fullscreen = pygame.display.set_mode((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
                self.screen = self.fullscreen
            else:
                self.fullscreen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), pygame.FULLSCREEN)
                self.screen = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        except Exception as e:
            print(f"Could not toggle fullscreen: {e}")
    
    def handle_splash_events(self, event):
        """Handle splash screen events - REMOVED"""
        pass
    
    def update_splash(self):
        """Update splash screen - REMOVED"""
        pass
    
    def handle_splash_events(self, event):
        """Handle splash screen events"""
        if event.type == pygame.KEYDOWN:
            # Any key skips splash screen
            self.state = "MENU"
            self.play_sound('selection')
    
    def update_splash(self):
        """Update splash screen - auto-advance after 3 seconds"""
        self.splash_timer += 1
        if self.splash_timer >= 180:  # 3 seconds at 60 FPS
            self.state = "MENU"
    
    def game_over(self):
        """Transition to game over screen"""
        print(f"Game Over! Final Score: {int(self.score)}, Distance: {int(self.distance)} km")
        
        # Add score to high scores
        self.score_manager.add_score(self.score, self.distance)
        
        # Update high score display
        self.high_score = self.score_manager.get_high_score()
        
        self.state = "GAME_OVER"
        self.game_over_timer = pygame.time.get_ticks()  # Start 10-second timer
        self.stop_music()
        self.play_menu_music()
        
        if self.score_manager.is_high_score(self.score):
            print(f"New high score achieved! Score: {int(self.score)}")
    
    def handle_pause_events(self, event):
        """Handle simple pause menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                # Resume game
                self.state = "GAME"
            elif event.key == pygame.K_r:
                # Restart game
                self.start_game()
            elif event.key == pygame.K_SPACE:
                # Return to main menu
                self.stop_music()
                self.play_menu_music()
                self.state = "MENU"
    
    def handle_game_over_events(self, event):
        """Handle game over screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.state = "MENU"
                self.play_sound('selection')
            elif event.key == pygame.K_r:
                self.start_game()  # Restart game
                self.play_sound('selection')
    
    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % 3
                self.play_sound('selection')
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % 3
                self.play_sound('selection')
            elif event.key == pygame.K_RETURN:
                self.play_sound('selection')
                if self.menu_selection == 0:  # Start Game
                    self.show_how_to_play()
                elif self.menu_selection == 1:  # Credits
                    self.state = "CREDITS"
                elif self.menu_selection == 2:  # Exit
                    pygame.quit()
                    sys.exit()
    
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Pause the game
                self.state = "PAUSED"
    
    def handle_credits_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.play_sound('selection')  # Play selection sound
                self.state = "MENU"
    
    def handle_how_to_play_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.play_sound('selection')  # Play selection sound
                self.state = "MENU"
            elif event.key == pygame.K_SPACE:
                self.play_sound('selection')  # Play selection sound
                self.start_game()
    
    def show_how_to_play(self):
        self.state = "HOW_TO_PLAY"
        self.how_to_play_timer = pygame.time.get_ticks()
    
    def start_game(self):
        self.state = "GAME"
        
        # Stop menu music and start background music
        self.stop_music()
        self.play_background_music()
        
        self.player = PlayerCar(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.sprite_manager)
        self.enemy_cars = []
        self.fuel = 100
        self.score = 0
        self.distance = 0  # Reset distance
        self.speed = 2
        self.road_offset = 0
        self.damage_flash = 0
        self.slide_effect = 0
        self.slide_direction = 0
        self.control_loss = 0
        self.spin_angle = 0
        
        # Visual sound feedback
        self.sound_feedback = ""
        self.sound_feedback_timer = 0
        self.sound_feedback_color = WHITE
        self.sound_feedback_size = 'medium'
    
    def update(self):
        if self.state == "GAME":
            self.update_game()
        elif self.state == "HOW_TO_PLAY":
            self.update_how_to_play()
    
    def update_game(self):
        # Update road scrolling
        self.road_offset += self.speed
        if self.road_offset >= 40:
            self.road_offset = 0
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.slide_effect, self.slide_direction, self.control_loss, self.spin_angle)
        
        # Update damage effects
        if self.damage_flash > 0:
            self.damage_flash -= 1
        if self.slide_effect > 0:
            self.slide_effect -= 1
        if self.control_loss > 0:
            self.control_loss -= 1
            self.spin_angle += 15  # Spin during control loss
        if self.sound_feedback_timer > 0:
            self.sound_feedback_timer -= 1
        
        # Spawn enemy cars
        if random.randint(1, 80) == 1:  # Reduced spawn rate for better performance
            # Multiple lanes for wider road
            lane = random.choice([450, 550, 650, 750, 850, 950])  # 6 lanes across wider road
            car_type = 'normal'  # Remove fuel from regular cars
            enemy_type = random.choice(['static', 'reactive', 'zigzag'])
            self.enemy_cars.append(EnemyCar(lane, -50, car_type, enemy_type, self.sprite_manager))
        
        # Spawn stationary fuel stations more frequently
        if random.randint(1, 200) == 1:  # More frequent fuel stations
            lane = random.choice([500, 650, 800])  # 3 fuel lanes across road
            self.enemy_cars.append(EnemyCar(lane, -50, 'fuel', 'fuel_station', self.sprite_manager))
        
        # Update enemy cars
        for car in self.enemy_cars[:]:
            car.update(self.speed, self.player)
            if car.y > SCREEN_HEIGHT:
                self.enemy_cars.remove(car)
                self.score += 10
        
        # Check collisions
        for car in self.enemy_cars[:]:
            if self.player.rect.colliderect(car.rect):
                if car.car_type == 'fuel':
                    self.fuel = min(100, self.fuel + 20)
                    self.play_sound('pickup')  # Changed from 'fuel' to 'pickup'
                    self.enemy_cars.remove(car)
                else:
                    # Collision with enemy car - damage and effects
                    self.fuel -= 15
                    self.damage_flash = 30  # Flash for 30 frames (0.5 seconds at 60 FPS)
                    self.play_sound('collision')
                    
                    # Enhanced collision effects
                    collision_severity = random.randint(1, 3)
                    
                    if collision_severity == 1:  # Light collision
                        self.slide_effect = 30  # Short slide
                        self.slide_direction = random.choice([-1, 1])
                    elif collision_severity == 2:  # Medium collision
                        self.slide_effect = 60  # Longer slide
                        self.slide_direction = random.choice([-1, 1])
                        self.control_loss = 45  # Some control loss
                    else:  # Heavy collision
                        self.slide_effect = 90  # Long slide
                        self.slide_direction = random.choice([-1, 1])
                        self.control_loss = 60  # Significant control loss
                        self.spin_angle = 0  # Reset spin angle
                    
                    self.enemy_cars.remove(car)
                    break
        
        # Decrease fuel over time
        self.fuel -= 0.1
        
        # Track distance (based on speed and time)
        self.distance += self.speed * 0.1
        
        # Check if fuel is empty - trigger game over
        if self.fuel <= 0:
            self.fuel = 0  # Ensure fuel doesn't go negative
            self.game_over()
            return  # Exit update_game to prevent further updates
        
        # Increase speed gradually
        self.speed = min(5, 2 + self.score / 1000)
    
    def update_how_to_play(self):
        # Check if 10 seconds have passed
        current_time = pygame.time.get_ticks()
        if current_time - self.how_to_play_timer >= 10000:  # 10 seconds
            self.start_game()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "SPLASH":
            self.draw_splash()
        elif self.state == "MENU":
            self.draw_menu()
        elif self.state == "GAME":
            self.draw_game()
        elif self.state == "PAUSED":
            self.draw_pause()
        elif self.state == "CREDITS":
            self.draw_credits()
        elif self.state == "HOW_TO_PLAY":
            self.draw_how_to_play()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
        
        # Note: pygame.display.flip() is now handled in run() method
    
    def draw_splash(self):
        """Draw simple splash screen with Amazon Q logo only"""
        # No background fill - let the transparent logo show on black screen
        self.screen.fill((0, 0, 0))
        
        # Amazon Q logo - centered, keeping original 1024x1024 size
        amazonQ_sprite = self.sprite_manager.get_sprite('amazonQ')
        if amazonQ_sprite:
            logo_rect = amazonQ_sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(amazonQ_sprite, logo_rect)
    
    def draw_menu(self):
        # Title
        title = self.font_large.render("ROAD FIGHTER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Menu options
        options = ["1 PLAYER", "CREDITS", "EXIT"]
        for i, option in enumerate(options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Instructions
        instruction = self.font_small.render("Use UP/DOWN arrows and ENTER to select", True, GRAY)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game(self):
        # Draw road
        self.draw_road()
        
        # Draw player (with damage flash effect)
        if self.damage_flash > 0 and self.damage_flash % 6 < 3:
            # Flash effect - don't draw player every few frames
            pass
        else:
            self.player.draw(self.screen, self.control_loss, self.spin_angle)
        
        # Draw enemy cars
        for car in self.enemy_cars:
            car.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
    
    def draw_road(self):
        # Road background - properly sized for fullscreen with room for UI
        road_rect = pygame.Rect(350, 0, 700, SCREEN_HEIGHT)  # Wider road, moved right
        pygame.draw.rect(self.screen, DARK_GRAY, road_rect)
        
        # Guardrails
        # Left guardrail - moved right to make room for UI
        left_guardrail = pygame.Rect(340, 0, 10, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, left_guardrail)
        # Left guardrail posts
        for y in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.rect(self.screen, GRAY, (335, y, 20, 5))
        
        # Right guardrail
        right_guardrail = pygame.Rect(1050, 0, 10, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, right_guardrail)
        # Right guardrail posts
        for y in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.rect(self.screen, GRAY, (1045, y, 20, 5))
        
        # Road edges (inner lines)
        pygame.draw.line(self.screen, WHITE, (350, 0), (350, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, WHITE, (1050, 0), (1050, SCREEN_HEIGHT), 2)
        
        # Lane dividers - animated with multiple lanes
        self.road_offset += self.speed
        if self.road_offset > 80:
            self.road_offset = 0
        
        # Multiple lane lines for wider road
        lane_positions = [450, 550, 650, 750, 850, 950]  # 6 lanes
        
        for lane_x in lane_positions:
            for y in range(-40, SCREEN_HEIGHT + 40, 80):
                line_y = y + self.road_offset
                if lane_x == 700:  # Center line
                    pygame.draw.line(self.screen, YELLOW, (lane_x, line_y), (lane_x, line_y + 40), 4)
                else:
                    pygame.draw.line(self.screen, WHITE, (lane_x, line_y), (lane_x, line_y + 40), 2)
    
    def draw_ui(self):
        # LEFT UI Panel - Fuel and Speed
        left_panel = pygame.Rect(20, 10, 280, 300)
        pygame.draw.rect(self.screen, (40, 40, 40), left_panel)
        pygame.draw.rect(self.screen, WHITE, left_panel, 2)
        
        # Fuel label
        fuel_label = self.font_small.render("FUEL", True, WHITE)
        self.screen.blit(fuel_label, (30, 30))
        
        # Fuel percentage positioned at current position
        fuel_percent = self.font_small.render(f"{int(self.fuel)}%", True, WHITE)
        self.screen.blit(fuel_percent, (160, 60))  # Keep percentage at current position
        
        # Fuel bar positioned back to original position (rolled back)
        fuel_rect = pygame.Rect(30, 95, 120, 12)  # Rolled back to original y-position 95
        pygame.draw.rect(self.screen, RED, fuel_rect)
        fuel_fill = pygame.Rect(30, 95, int(120 * self.fuel / 100), 12)  # Rolled back to y-position 95
        pygame.draw.rect(self.screen, GREEN, fuel_fill)
        pygame.draw.rect(self.screen, WHITE, fuel_rect, 1)
        
        # Speed with more spacing between label and value
        speed_label = self.font_small.render("SPEED", True, WHITE)
        self.screen.blit(speed_label, (30, 110))
        speed_value = self.font_small.render(f"{int(self.speed * 10)} KM/H", True, YELLOW)
        self.screen.blit(speed_value, (30, 140))
        
        # Instructions moved to bottom area with larger panel
        instruction_panel = pygame.Rect(20, SCREEN_HEIGHT - 140, 280, 120)  # Larger panel
        pygame.draw.rect(self.screen, (40, 40, 40), instruction_panel)
        pygame.draw.rect(self.screen, WHITE, instruction_panel, 2)
        
        instruction_y = SCREEN_HEIGHT - 130  # Moved up from -120 to -130 for better top spacing
        esc_text = self.font_tiny.render("ESC - RETURN", True, WHITE)
        self.screen.blit(esc_text, (30, instruction_y))
        menu_text = self.font_tiny.render("TO MENU", True, WHITE)
        self.screen.blit(menu_text, (30, instruction_y + 20))
        
        arrow_text = self.font_tiny.render("ARROW KEYS", True, WHITE)
        self.screen.blit(arrow_text, (30, instruction_y + 45))
        move_text = self.font_tiny.render("TO MOVE", True, WHITE)
        self.screen.blit(move_text, (30, instruction_y + 65))
        
        # RIGHT UI Panel - Distance and Score (outside right guardrail)
        right_panel = pygame.Rect(1080, 10, 280, 300)
        pygame.draw.rect(self.screen, (40, 40, 40), right_panel)
        pygame.draw.rect(self.screen, WHITE, right_panel, 2)
        
        # Score with more spacing between label and value
        score_label = self.font_small.render("SCORE", True, WHITE)
        self.screen.blit(score_label, (1090, 30))
        score_value = self.font_small.render(f"{int(self.score)}", True, YELLOW)
        self.screen.blit(score_value, (1090, 60))
        
        # Distance with more spacing between label and value
        distance_label = self.font_small.render("DISTANCE", True, WHITE)
        self.screen.blit(distance_label, (1090, 120))
        distance_value = self.font_small.render(f"{int(self.distance)} KM", True, YELLOW)
        self.screen.blit(distance_value, (1090, 150))
        
        # High Score with more spacing between label and value
        high_score_label = self.font_small.render("HIGH SCORE", True, WHITE)
        self.screen.blit(high_score_label, (1090, 210))
        high_score_value = self.font_small.render(f"{int(self.high_score)}", True, YELLOW)
        self.screen.blit(high_score_value, (1090, 240))
        
        # Status messages moved to center screen to avoid UI overlap
        if self.damage_flash > 0:
            damage_text = self.font_medium.render("COLLISION!", True, RED)
            damage_rect = damage_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(damage_text, damage_rect)
        
        # Control loss indicator - center screen
        if self.control_loss > 0:
            control_text = self.font_medium.render("SPINNING OUT!", True, RED)
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
            self.screen.blit(control_text, control_rect)
        
        # Visual sound feedback - center screen only
        if self.sound_feedback_timer > 0:
            if self.sound_feedback_size == 'large':
                font = self.font_large
                y_pos = 180
            elif self.sound_feedback_size == 'medium':
                font = self.font_medium
                y_pos = 185
            else:  # small
                font = self.font_small
                y_pos = 190
            
            sound_text = font.render(self.sound_feedback, True, self.sound_feedback_color)
            sound_rect = sound_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(sound_text, sound_rect)
    
    def draw_pause(self):
        """Draw simple pause menu overlay"""
        # First draw the game in the background (frozen)
        self.draw_road()
        
        # Draw player and cars (frozen)
        if self.damage_flash > 0 and self.damage_flash % 6 < 3:
            pass
        else:
            self.player.draw(self.screen, self.control_loss, self.spin_angle)
        
        for car in self.enemy_cars:
            car.draw(self.screen)
        
        self.draw_ui()
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw ONLY the pause content - nothing else
        pause_title = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_title.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(pause_title, pause_rect)
        
        # Simple instructions only
        instructions = [
            "P or ESC - Resume Game",
            "R - Restart Game", 
            "SPACE - Return to Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400 + i * 40))
            self.screen.blit(text, text_rect)
    
    def draw_credits(self):
        credits_text = [
            "Road Fighter - Pygame Edition",
            "",
            " A classic arcade-style racing game inspired by the original Konami Road Fighter",
            "",
            "Developed with Amazon Q (prompts) + Pygame",
            "",
            "Created by Juliano Salszbrun"
        ]
        
        for i, line in enumerate(credits_text):
            color = YELLOW if i == 0 else WHITE
            font = self.font_medium if i == 0 else self.font_small
            text = font.render(line, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_how_to_play(self):
        """Completely recreated How to Play screen with better spacing and layout"""
        # Dark gradient background
        self.screen.fill((10, 20, 40))
        
        # Title - centered at top with more space
        title_text = self.font_large.render("HOW TO PLAY", True, WHITE)
        title_rect = title_text.get_rect(center=(GAME_AREA_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # VEHICLES section
        vehicles_y = 200
        vehicles_title = self.font_medium.render("VEHICLES", True, YELLOW)
        vehicles_rect = vehicles_title.get_rect(center=(GAME_AREA_WIDTH // 2, vehicles_y))
        self.screen.blit(vehicles_title, vehicles_rect)
        
        # Vehicle sprites display - moved to the right, keeping original spacing
        sprite_y = vehicles_y + 80
        sprite_names = ['player_car', 'enemy_static', 'enemy_police', 'enemy_sports']
        # Original spacing but shifted right by 200px
        x_positions = [450, 650, 850, 1050]  # Moved from [250, 450, 650, 850] to the right
        
        # Display vehicle sprites
        for i, sprite_name in enumerate(sprite_names):
            sprite = self.sprite_manager.get_sprite(sprite_name)
            if sprite:
                sprite_rect = sprite.get_rect(center=(x_positions[i], sprite_y))
                self.screen.blit(sprite, sprite_rect)
        
        # Vehicle labels with better spacing - moved to match vehicle positions
        descriptions = ["YOUR CAR", "BASIC FOE", "DODGES YOU", "ZIGZAG MOVE"]
        
        for i, desc in enumerate(descriptions):
            # Only description text - moved to match new vehicle positions
            desc_text = self.font_tiny.render(desc, True, WHITE)
            desc_rect = desc_text.get_rect(center=(x_positions[i], sprite_y + 80))
            self.screen.blit(desc_text, desc_rect)
        
        # FUEL STATION section - separate area
        fuel_y = sprite_y + 140  # Reduced spacing since we removed labels
        fuel_title = self.font_medium.render("FUEL STATION", True, GREEN)
        fuel_title_rect = fuel_title.get_rect(center=(GAME_AREA_WIDTH // 2, fuel_y))
        self.screen.blit(fuel_title, fuel_title_rect)
        
        # Fuel station sprite - centered and prominent
        fuel_sprite = self.sprite_manager.get_sprite('fuel_station')
        if fuel_sprite:
            fuel_rect = fuel_sprite.get_rect(center=(GAME_AREA_WIDTH // 2, fuel_y + 70))
            self.screen.blit(fuel_sprite, fuel_rect)
        
        # Fuel description
        fuel_desc = self.font_small.render("COLLECT TO REFUEL YOUR CAR", True, GREEN)
        fuel_desc_rect = fuel_desc.get_rect(center=(GAME_AREA_WIDTH // 2, fuel_y + 140))
        self.screen.blit(fuel_desc, fuel_desc_rect)
        
        # Bottom section - CONTROLS and OBJECTIVES side by side - moved up to avoid overlapping
        bottom_section_y = fuel_y + 160  # Reverted back to 160 as requested
        
        # CONTROLS section - left side with more space and bottom padding
        controls_x = 300
        controls_title = self.font_medium.render("CONTROLS", True, YELLOW)
        self.screen.blit(controls_title, (controls_x, bottom_section_y))
        
        # Control instructions with better spacing
        controls = [
            "ARROW KEYS - MOVE YOUR CAR",
            "ESC - RETURN TO MENU",
            "F11 - TOGGLE FULLSCREEN"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font_tiny.render(control, True, WHITE)
            self.screen.blit(control_text, (controls_x, bottom_section_y + 60 + (i * 35)))  # Changed from +50 to +60 for line space
        
        # Add 2px bottom padding for controls section
        controls_bottom = bottom_section_y + 60 + (len(controls) * 35) + 2  # Updated calculation
        
        # OBJECTIVES section - right side with more space and bottom padding
        objectives_x = 900
        objectives_title = self.font_medium.render("OBJECTIVES", True, RED)
        self.screen.blit(objectives_title, (objectives_x, bottom_section_y))
        
        # Objective list with better spacing
        objectives = [
            "AVOID ENEMY CARS",
            "COLLECT FUEL TO SURVIVE",
            "DRIVE AS FAR AS POSSIBLE"
        ]
        
        for i, objective in enumerate(objectives):
            obj_text = self.font_tiny.render(objective, True, WHITE)
            self.screen.blit(obj_text, (objectives_x, bottom_section_y + 60 + (i * 35)))  # Changed from +50 to +60 for line space
        
        # Add 2px bottom padding for objectives section
        objectives_bottom = bottom_section_y + 60 + (len(objectives) * 35) + 2  # Updated calculation for line space
        
        # Calculate the bottom of both sections to avoid overlapping
        sections_bottom = max(controls_bottom, objectives_bottom)
        
        # Instructions at bottom with proper spacing - no overlapping
        instruction_y = sections_bottom + 50  # Reduced from 60 to 50 for tighter spacing
        
        # Main instruction - prominent
        instruction_text = self.font_small.render("PRESS SPACE TO START GAME", True, YELLOW)
        instruction_rect = instruction_text.get_rect(center=(GAME_AREA_WIDTH // 2, instruction_y))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Secondary instruction
        escape_text = self.font_tiny.render("PRESS ESC TO RETURN TO MENU", True, GRAY)
        escape_rect = escape_text.get_rect(center=(GAME_AREA_WIDTH // 2, instruction_y + 40))
        self.screen.blit(escape_text, escape_rect)
    
    def draw_game_over(self):
        """Draw game over screen with statistics"""
        self.screen.fill((40, 20, 20))  # Dark red background
        
        # Game Over title
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(GAME_AREA_WIDTH // 2, 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Statistics
        stats_y = 200
        
        # Final Score
        score_text = self.font_medium.render(f"Final Score: {int(self.score)}", True, WHITE)
        score_rect = score_text.get_rect(center=(GAME_AREA_WIDTH // 2, stats_y))
        self.screen.blit(score_text, score_rect)
        
        # Distance Traveled
        distance_text = self.font_medium.render(f"Distance: {int(self.distance)} km", True, WHITE)
        distance_rect = distance_text.get_rect(center=(GAME_AREA_WIDTH // 2, stats_y + 50))
        self.screen.blit(distance_text, distance_rect)
        
        # High Score
        high_score_text = self.font_medium.render(f"High Score: {int(self.high_score)}", True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(GAME_AREA_WIDTH // 2, stats_y + 100))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Performance rating
        if self.distance > 100:
            rating = "EXCELLENT!"
            rating_color = GREEN
        elif self.distance > 50:
            rating = "GOOD!"
            rating_color = YELLOW
        elif self.distance > 20:
            rating = "FAIR"
            rating_color = ORANGE
        else:
            rating = "TRY AGAIN"
            rating_color = RED
        
        rating_text = self.font_medium.render(rating, True, rating_color)
        rating_rect = rating_text.get_rect(center=(GAME_AREA_WIDTH // 2, stats_y + 150))
        self.screen.blit(rating_text, rating_rect)
        
        # Instructions
        restart_text = self.font_small.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(GAME_AREA_WIDTH // 2, 450))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("Press SPACE to Return to Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(GAME_AREA_WIDTH // 2, 480))
        self.screen.blit(menu_text, menu_rect)

class PlayerCar:
    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.width = 75  # Updated for square sprites
        self.height = 75  # Updated for square sprites
        self.speed = 5
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.sprite_manager = sprite_manager
        self.sprite = sprite_manager.get_sprite('player_car')
    
    def update(self, keys, slide_effect, slide_direction, control_loss, spin_angle):
        # Calculate control factor based on effects
        if control_loss > 0:
            control_factor = 0.1  # Very little control during spin out
        elif slide_effect > 0:
            control_factor = 0.4  # Reduced control during slide
        else:
            control_factor = 1.0  # Full control
        
        # Apply slide effect if active
        if slide_effect > 0:
            slide_force = 2 * (slide_effect / 60)  # Stronger at the beginning
            self.x += slide_direction * slide_force
        
        # Apply random movement during control loss
        if control_loss > 0:
            # Random jerky movement during spin out
            self.x += random.randint(-2, 2)
            self.y += random.randint(-1, 1)
        
        # Movement with control factor
        move_speed = self.speed * control_factor
        
        if keys[pygame.K_LEFT] and self.x > 400:  # Adjusted for new road boundaries (350 + 50 margin)
            self.x -= move_speed
        if keys[pygame.K_RIGHT] and self.x < 1000:  # Adjusted for new road boundaries (1050 - 50 margin)
            self.x += move_speed
        if keys[pygame.K_UP] and self.y > 75:  # Adjusted for larger cars
            self.y -= move_speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - 75:  # Adjusted for larger cars
            self.y += move_speed
        
        # Keep player within road boundaries
        self.x = max(400, min(1000, self.x))  # Adjusted for new road boundaries
        self.y = max(75, min(SCREEN_HEIGHT - 75, self.y))  # Adjusted for larger cars
        
        # Update rect
        self.rect.center = (self.x, self.y)
    
    def draw(self, screen, control_loss, spin_angle):
        if self.sprite:
            # Use sprite if available
            if control_loss > 0:
                # Rotate sprite during control loss
                rotated_sprite = pygame.transform.rotate(self.sprite, spin_angle % 360)
                sprite_rect = rotated_sprite.get_rect(center=(self.x, self.y))
                screen.blit(rotated_sprite, sprite_rect)
            else:
                # Normal sprite drawing
                sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
                screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback to original drawing if no sprite
            if control_loss > 0:
                # During control loss, draw a simple rotated rectangle
                simple_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
                pygame.draw.rect(simple_surface, BLUE, (5, 5, 30, 50))
                pygame.draw.rect(simple_surface, WHITE, (10, 10, 20, 12))  # Windshield
                pygame.draw.rect(simple_surface, RED, (12, 47, 16, 6))     # Taillights
                
                rotated_surface = pygame.transform.rotate(simple_surface, spin_angle % 360)
                rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
                screen.blit(rotated_surface, rotated_rect)
            else:
                # Normal drawing - simplified for performance
                car_rect = pygame.Rect(self.x - 37, self.y - 37, 75, 75)  # Updated for square cars
                pygame.draw.rect(screen, BLUE, car_rect)
                
                # Windshield
                pygame.draw.rect(screen, (173, 216, 230), (self.x - 25, self.y - 30, 50, 20))
                # Rear window
                pygame.draw.rect(screen, (173, 216, 230), (self.x - 25, self.y + 10, 50, 15))
                
                # Headlights
                pygame.draw.circle(screen, YELLOW, (int(self.x - 15), int(self.y - 33)), 5)
                pygame.draw.circle(screen, YELLOW, (int(self.x + 15), int(self.y - 33)), 5)
                
                # Taillights
                pygame.draw.rect(screen, RED, (self.x - 20, self.y + 27, 15, 8))
                pygame.draw.rect(screen, RED, (self.x + 5, self.y + 27, 15, 8))

class EnemyCar:
    def __init__(self, x, y, car_type='normal', enemy_type='static', sprite_manager=None):
        self.x = x
        self.y = y
        if car_type == 'fuel':
            self.width = 100  # Fuel stations are larger
            self.height = 100
        else:
            self.width = 75  # Cars are square
            self.height = 75
        self.speed = random.randint(1, 3)
        self.car_type = car_type
        self.enemy_type = enemy_type
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.sprite_manager = sprite_manager
        
        # Load appropriate sprite
        self.sprite = None
        if sprite_manager:
            if car_type == 'fuel' and enemy_type == 'fuel_station':
                self.sprite = sprite_manager.get_sprite('fuel_station')
            elif enemy_type == 'static':
                self.sprite = sprite_manager.get_sprite('enemy_static')
            elif enemy_type == 'reactive':
                self.sprite = sprite_manager.get_sprite('enemy_police')
            elif enemy_type == 'zigzag':
                self.sprite = sprite_manager.get_sprite('enemy_sports')
        
        # For zigzag movement
        self.zigzag_direction = random.choice([-1, 1])  # -1 for left, 1 for right
        self.zigzag_speed = 2
        self.zigzag_counter = 0
        
        # For reactive movement
        self.reaction_distance = 100
        self.side_speed = 3
        
        # Set color based on type and enemy behavior (fallback for when no sprite)
        if car_type == 'fuel':
            self.color = GREEN
        else:
            if enemy_type == 'static':
                self.color = random.choice([RED, YELLOW, ORANGE])
            elif enemy_type == 'reactive':
                self.color = random.choice([WHITE, GRAY])
            elif enemy_type == 'zigzag':
                self.color = random.choice([BLUE, (128, 0, 128)])  # Blue or Purple
    
    def update(self, road_speed, player):
        # Fuel stations don't move
        if self.enemy_type == 'fuel_station':
            self.y += road_speed  # Only move with road speed, no additional movement
        else:
            # Basic downward movement for other cars
            self.y += road_speed + self.speed
        
        # Apply specific enemy behavior (only for non-fuel-station cars)
        if self.enemy_type == 'static':
            # Static enemy - just moves down
            pass
            
        elif self.enemy_type == 'reactive':
            # Reactive enemy - moves away if player is too close
            distance_to_player = abs(self.x - player.x)
            vertical_distance = abs(self.y - player.y)
            
            # If player is close enough, move away
            if distance_to_player < self.reaction_distance and vertical_distance < self.reaction_distance:
                if self.x < player.x:
                    # Player is to the right, move left
                    self.x -= self.side_speed
                else:
                    # Player is to the left, move right
                    self.x += self.side_speed
                
                # Keep within road boundaries (updated for new road)
                self.x = max(220, min(580, self.x))
                
        elif self.enemy_type == 'zigzag':
            # Zigzag enemy - moves left and right while coming down
            self.zigzag_counter += 1
            
            # Change direction every 30 frames (about half a second at 60 FPS)
            if self.zigzag_counter >= 30:
                self.zigzag_direction *= -1
                self.zigzag_counter = 0
            
            # Apply horizontal movement
            self.x += self.zigzag_direction * self.zigzag_speed
            
            # Keep within road boundaries and bounce off edges (updated for new road)
            if self.x <= 220:
                self.x = 220
                self.zigzag_direction = 1
            elif self.x >= 580:
                self.x = 580
                self.zigzag_direction = -1
        
        # Update rect position
        self.rect.center = (self.x, self.y)
    
    def draw(self, screen):
        if self.sprite:
            # Use sprite if available
            sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
            screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback to original drawing if no sprite
            if self.car_type == 'fuel':
                if self.enemy_type == 'fuel_station':
                    # Stationary fuel station - simple design (larger)
                    station_rect = pygame.Rect(self.x - 50, self.y - 50, 100, 100)
                    pygame.draw.rect(screen, GREEN, station_rect)
                    
                    # Fuel symbol (large and clear)
                    pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 25)
                    pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 20)
                    
                    # "F" for fuel
                    font = pygame.font.Font(None, 48)
                    fuel_text = font.render("F", True, BLACK)
                    text_rect = fuel_text.get_rect(center=(self.x, self.y))
                    screen.blit(fuel_text, text_rect)
                    
                else:
                    # Moving fuel truck - simplified (larger)
                    truck_rect = pygame.Rect(self.x - 37, self.y - 37, 75, 75)
                    pygame.draw.rect(screen, GREEN, truck_rect)
                    
                    # Fuel symbol
                    pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 18)
                    pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 15)
                    
            else:
                # Regular enemy car - simplified (square)
                car_rect = pygame.Rect(self.x - 37, self.y - 37, 75, 75)
                pygame.draw.rect(screen, self.color, car_rect)
                
                # Windshield
                pygame.draw.rect(screen, (173, 216, 230), (self.x - 25, self.y - 30, 50, 20))
                
                # Car type indicators (simplified)
                if self.enemy_type == 'reactive':
                    # Police lights
                    pygame.draw.rect(screen, RED, (self.x - 15, self.y - 40, 10, 6))
                    pygame.draw.rect(screen, BLUE, (self.x + 5, self.y - 40, 10, 6))
                    
                elif self.enemy_type == 'zigzag':
                    # Racing stripe
                    pygame.draw.line(screen, WHITE, (self.x, self.y - 37), (self.x, self.y + 37), 6)
                    
                    # Direction arrow (simplified)
                    if self.zigzag_direction == 1:  # Moving right
                        pygame.draw.polygon(screen, WHITE, [
                            (self.x + 20, self.y), (self.x + 30, self.y - 6), (self.x + 30, self.y + 6)
                        ])
                    else:  # Moving left
                        pygame.draw.polygon(screen, WHITE, [
                            (self.x - 20, self.y), (self.x - 30, self.y - 6), (self.x - 30, self.y + 6)
                        ])
                
                # Headlights for all cars
                pygame.draw.circle(screen, WHITE, (int(self.x - 15), int(self.y - 33)), 4)
                pygame.draw.circle(screen, WHITE, (int(self.x + 15), int(self.y - 33)), 4)

if __name__ == "__main__":
    game = Game()
    game.run()
