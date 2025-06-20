# Sprites Folder

This folder is for custom graphics and sprites that you can add to enhance the game's visual appearance.

## 🎨 Supported Formats

- PNG (recommended for transparency)
- JPG/JPEG
- BMP
- GIF

## 📏 Recommended Sizes

### Car Sprites:
- **Player Car**: 30x50 pixels
- **Enemy Cars**: 30x50 pixels
- **Fuel Stations**: 35x55 pixels

### UI Elements:
- **Icons**: 16x16 or 24x24 pixels
- **Backgrounds**: 800x600 pixels (full screen)

## 🔧 How to Use Custom Sprites

1. **Place your image files in this folder**
2. **Modify main.py to load your sprites**:

```python
# Example: Loading a custom player car sprite
try:
    player_sprite = pygame.image.load("sprites/player_car.png")
    player_sprite = pygame.transform.scale(player_sprite, (30, 50))
except:
    # Fallback to default drawing
    pass
```

3. **Replace the drawing code in the respective classes**

## 🎯 Sprite Ideas

- Custom car designs
- Animated sprites
- Background scenery
- UI elements
- Particle effects
- Road textures

## 📝 Naming Convention

Use descriptive names for your sprites:
- `player_car.png`
- `enemy_static.png`
- `enemy_police.png`
- `enemy_sports.png`
- `fuel_station.png`
- `background_road.png`

---

**Happy customizing! 🎨**
