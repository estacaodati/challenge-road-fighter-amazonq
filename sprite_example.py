"""
Example of how to add custom sprites to the Road Fighter game.
This file shows how you can load and use custom graphics.
"""

import pygame
import os

def load_sprite(filename, default_size=(30, 50)):
    """
    Load a sprite from the sprites folder with fallback to None
    
    Args:
        filename: Name of the sprite file
        default_size: Tuple of (width, height) to scale the sprite
    
    Returns:
        pygame.Surface or None if loading fails
    """
    try:
        sprite_path = os.path.join("sprites", filename)
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path)
            sprite = pygame.transform.scale(sprite, default_size)
            print(f"✅ Loaded sprite: {filename}")
            return sprite
        else:
            print(f"⚠️  Sprite not found: {filename}")
            return None
    except Exception as e:
        print(f"❌ Error loading sprite {filename}: {e}")
        return None

def create_sample_sprite():
    """Create a simple sample sprite file"""
    pygame.init()
    
    # Create a simple car sprite (30x50 pixels)
    sprite_surface = pygame.Surface((30, 50), pygame.SRCALPHA)
    
    # Draw a simple car
    # Body
    pygame.draw.rect(sprite_surface, (0, 100, 255), (5, 5, 20, 40))  # Blue body
    # Windshield
    pygame.draw.rect(sprite_surface, (173, 216, 230), (8, 8, 14, 12))  # Light blue
    # Wheels
    pygame.draw.circle(sprite_surface, (0, 0, 0), (10, 15), 3)  # Left wheel
    pygame.draw.circle(sprite_surface, (0, 0, 0), (20, 15), 3)  # Right wheel
    pygame.draw.circle(sprite_surface, (0, 0, 0), (10, 35), 3)  # Left wheel
    pygame.draw.circle(sprite_surface, (0, 0, 0), (20, 35), 3)  # Right wheel
    # Headlights
    pygame.draw.circle(sprite_surface, (255, 255, 0), (12, 5), 2)  # Left headlight
    pygame.draw.circle(sprite_surface, (255, 255, 0), (18, 5), 2)  # Right headlight
    
    # Save the sprite
    os.makedirs("sprites", exist_ok=True)
    pygame.image.save(sprite_surface, "sprites/sample_player_car.png")
    print("✅ Created sample sprite: sprites/sample_player_car.png")
    
    pygame.quit()

if __name__ == "__main__":
    print("🎨 Sprite Example for Road Fighter")
    print("=" * 40)
    
    # Create a sample sprite
    create_sample_sprite()
    
    # Show how to load sprites
    pygame.init()
    
    print("\n📁 Testing sprite loading:")
    player_sprite = load_sprite("sample_player_car.png", (30, 50))
    enemy_sprite = load_sprite("enemy_car.png", (30, 50))  # This won't exist
    
    print("\n💡 To use custom sprites in the game:")
    print("1. Place your PNG/JPG files in the sprites/ folder")
    print("2. Modify the PlayerCar.draw() method in main.py")
    print("3. Use load_sprite() function to load your graphics")
    print("4. Replace pygame.draw.rect() calls with screen.blit(sprite, rect)")
    
    print("\n🎯 Example modification for PlayerCar class:")
    print("""
    # In PlayerCar.__init__():
    self.sprite = load_sprite("player_car.png", (30, 50))
    
    # In PlayerCar.draw():
    if self.sprite:
        sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        screen.blit(self.sprite, sprite_rect)
    else:
        # Fallback to current drawing code
        pygame.draw.rect(screen, BLUE, car_rect)
    """)
    
    pygame.quit()
