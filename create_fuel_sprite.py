import pygame
import os

def create_fuel_station_sprite():
    """Create a simple fuel station sprite (larger size)"""
    pygame.init()
    
    # Create fuel station sprite (50x80 pixels - increased size)
    sprite_surface = pygame.Surface((50, 80), pygame.SRCALPHA)
    
    # Main body (green)
    pygame.draw.rect(sprite_surface, (0, 150, 0), (3, 3, 44, 74))
    
    # Fuel pump body
    pygame.draw.rect(sprite_surface, (0, 100, 0), (7, 7, 36, 66))
    
    # Display screen
    pygame.draw.rect(sprite_surface, (200, 200, 200), (12, 12, 26, 20))
    pygame.draw.rect(sprite_surface, (0, 0, 0), (12, 12, 26, 20), 2)
    
    # Fuel nozzle holder
    pygame.draw.rect(sprite_surface, (50, 50, 50), (40, 20, 7, 12))
    
    # Fuel symbol in center
    pygame.draw.circle(sprite_surface, (0, 0, 0), (25, 50), 12)
    pygame.draw.circle(sprite_surface, (255, 255, 255), (25, 50), 9)
    
    # Gas pump icon
    pygame.draw.rect(sprite_surface, (0, 0, 0), (22, 46, 6, 8))
    pygame.draw.circle(sprite_surface, (0, 0, 0), (25, 43), 3)
    
    # "FUEL" text
    font = pygame.font.Font(None, 20)
    fuel_text = font.render("FUEL", True, (255, 255, 255))
    text_rect = fuel_text.get_rect(center=(25, 65))
    sprite_surface.blit(fuel_text, text_rect)
    
    # Base
    pygame.draw.rect(sprite_surface, (100, 100, 100), (0, 72, 50, 8))
    
    # Save the sprite
    os.makedirs("sprites", exist_ok=True)
    pygame.image.save(sprite_surface, "sprites/fuel_station.png")
    print("✅ Created larger fuel station sprite: sprites/fuel_station.png (50x80)")
    
    pygame.quit()

if __name__ == "__main__":
    print("🎨 Creating larger fuel station sprite...")
    create_fuel_station_sprite()
    print("🎯 Larger fuel station sprite ready for use!")
