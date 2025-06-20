 🚗  Road Fighter - Pygame Edition

 👥  A classic arcade-style racing game inspired by the original Konami Road Fighter

 💻  Developed with Amazon Q (prompts) + Pygame



A classic arcade-style racing game built with Python and Pygame, inspired by the original Konami Road Fighter, created by **Juliano Salszbrun**

## 🎮 Game Features

- **Three Enemy Types**: Static, Reactive, and Zigzag cars with unique behaviors
- **Fuel Management**: Collect fuel from stationary fuel stations
- **Collision Physics**: Realistic sliding and spinning effects
- **Pause System**: ESC pauses game with resume/restart/menu options
- **Score Persistence**: Local high score tracking with JSON storage
- **Custom Assets**: Pixeled font and custom car/fuel station sprites
- **Visual Feedback**: Text-based feedback for sound effects when audio is disabled
- **Performance Optimized**: Runs at stable 60 FPS in 1400x900 fullscreen

## 📁 Folder Structure

```
Road Fighter/
├── main.py                 # Main game file
├── high_scores.json        # Local high scores storage (auto-generated)
├── founts/                 # Custom fonts folder
│   └── Pixeled.ttf        # Custom pixel font
├── sprites/               # Graphics files folder
│   ├── player_car.png     # Player car sprite (256x256)
│   ├── enemy_static.png   # Static enemy sprite (256x256)
│   ├── enemy_police.png   # Police car sprite (256x256)
│   ├── enemy_sports.png   # Sports car sprite (256x256)
│   └── fuel_station.png   # Fuel station sprite (500x500)
├── sounds/                # Audio files folder
│   ├── collision.mp3      # Crash sound effect
│   ├── pickup.mp3         # Fuel pickup sound
│   ├── selection.mp3      # Menu navigation sound
│   ├── menu.mp3          # Menu background music
│   └── background.mp3    # Game background music
├── create_sounds.py       # Utility to generate default sounds
├── README.md             # This file
└── PromptsAI.md          # Complete development guide
```

## 🔊 Audio System

The game supports both audio and visual feedback:

### With Audio Hardware:
- Background music for menu and gameplay
- Sound effects for collisions, fuel pickup, and menu navigation
- Automatic audio detection and initialization
- Volume control for music and effects

### Without Audio (Visual Mode):
- **CRASH!** - Collision feedback (red text)
- **+FUEL** - Fuel pickup feedback (green text)
- **SELECT** - Menu navigation feedback (yellow text)
- Clear audio status indicator

## 🎨 Customization

### Adding Custom Sounds:
1. Place your MP3 files in the `sounds/` folder
2. Use these exact filenames:
   - `collision.mp3` - Crash sound
   - `pickup.mp3` - Fuel pickup sound
   - `selection.mp3` - Menu navigation sound
   - `menu.mp3` - Menu background music
   - `background.mp3` - Game background music

### Adding Custom Sprites:
1. Place your image files in the `sprites/` folder
2. Recommended sizes:
   - Car sprites: 256x256 pixels (scaled to 75x75 in-game)
   - Fuel station: 500x500 pixels (scaled to 100x100 in-game)
3. Supported formats: PNG, JPG, BMP, GIF

### Custom Font:
- Place `Pixeled.ttf` in the `founts/` folder
- Game automatically falls back to default fonts if unavailable

## 🎯 Controls

### Menu Navigation:
- **UP/DOWN**: Navigate menu options
- **ENTER**: Select menu option
- **ESC**: Return to previous screen

### Gameplay:
- **Arrow Keys**: Move your car
- **ESC**: Pause game (shows pause menu)

### Pause Menu:
- **P or ESC**: Resume game
- **R**: Restart game
- **SPACE**: Return to main menu

### Special:
- **F11**: Toggle fullscreen mode
- **SPACE**: Start game from "How to Play" screen

## 🚗 Vehicle Types

### Player Car (Blue)
- Custom sprite with detailed graphics
- Spinning animation during control loss
- Collision damage effects with sliding physics

### Enemy Cars
1. **Static** (Red/Yellow/Orange): Move straight down at constant speed
2. **Reactive** (White/Gray): Move away when you get close, feature police lights
3. **Zigzag** (Blue/Purple): Move left-right unpredictably, have racing stripes

### Fuel Stations (Green)
- Stationary fuel pumps with "F" symbol
- Refill your fuel tank when collected
- Essential for survival - game ends when fuel reaches zero

## 🛠️ Technical Details

### Performance:
- **Target**: 60 FPS stable performance
- **Resolution**: 1400x900 pixels optimized for fullscreen
- **Road System**: 700px wide road with 6 lanes
- **Collision Detection**: Efficient rectangle-based collision system
- **Spawn Rates**: Optimized for smooth gameplay (1/80 for cars, 1/200 for fuel)

### UI System:
- **Left Panel**: Fuel bar, speed indicator, and controls
- **Right Panel**: Score, distance, and high score display
- **Bottom Panel**: Instruction text in separate bordered area
- **Clean Layout**: No overlapping elements, proper spacing throughout

### Audio System:
- **Format Support**: MP3 files with fallback generation
- **Visual Feedback**: Text-based feedback when audio unavailable
- **Music System**: Separate menu and gameplay background music
- **Volume Control**: Automatic volume adjustment for different contexts

## 🚀 Running the Game

### Requirements:
```bash
pip install pygame
```

### Start Game:
```bash
python main.py
```

### Generate Default Sounds (Optional):
```bash
python create_sounds.py
```

## 🏆 Score System

### High Score Tracking:
- **Local Storage**: Scores saved to `high_scores.json`
- **Top 10**: Keeps your best 10 scores with date stamps
- **Persistence**: Scores survive game restarts
- **Display**: Shows current high score in-game and celebrates new records

### Scoring Mechanics:
- **Survival Points**: Points for staying alive and avoiding obstacles
- **Distance Bonus**: Additional points based on distance traveled
- **Fuel Efficiency**: Better scores for efficient fuel management
- **Speed Scaling**: Score multiplier increases with game speed

## 🎵 Audio Troubleshooting

If you experience audio issues:

1. **Check Audio Hardware**: Ensure speakers/headphones are connected
2. **File Format**: Ensure audio files are in MP3 format
3. **File Permissions**: Make sure sound files in `sounds/` folder are readable
4. **Fallback Mode**: Game automatically switches to visual feedback if audio fails
5. **Volume**: Check system volume and game audio settings

## 🎨 Visual Feedback System

When audio is unavailable, the game provides rich visual feedback:

- **Collision Effects**: Red "CRASH!" text with proper positioning
- **Fuel Collection**: Green "+FUEL" confirmation message
- **Menu Navigation**: Yellow "SELECT" indicator for menu actions
- **Status Display**: Clear audio on/off indicator in UI
- **Center Positioning**: All feedback messages appear in center screen area

## 📝 Game Mechanics

### Fuel System:
- **Consumption**: Fuel decreases continuously over time (-0.1 per frame)
- **Collection**: Collect fuel from green fuel stations to refill
- **Game Over**: Game ends only when fuel reaches zero
- **Collision Impact**: Crashes cause additional fuel loss (15 units)

### Collision System:
- **Light Collision**: Short slide effect (30 frames)
- **Medium Collision**: Slide + some control loss (60 frames)
- **Heavy Collision**: Long slide + significant spinning (90 frames)
- **Visual Effects**: Damage flash, spinning animation, and status messages

### Pause System:
- **ESC Key**: Pauses game instead of triggering game over
- **Overlay**: Semi-transparent overlay shows frozen game state
- **Direct Controls**: No menu navigation required - direct key responses
- **State Preservation**: Game state perfectly preserved during pause

### Scoring & Progression:
- **Dynamic Speed**: Speed increases gradually with score (max 5x)
- **Distance Tracking**: Measures how far you've traveled
- **High Score**: Persistent tracking of your best performances
- **Performance Rating**: EXCELLENT/GOOD/FAIR/TRY AGAIN based on distance

## 🔧 Development

### Adding New Features:
1. Fork the project
2. Add your enhancements to `main.py`
3. Test with both audio on/off modes
4. Update this README with new features
5. Test pause system and score persistence

### Code Structure:
- **ScoreManager**: Handles JSON-based score persistence
- **SpriteManager**: Manages loading and scaling of custom sprites
- **Game States**: Menu, Game, Paused, How to Play, Game Over
- **Clean UI**: Separate drawing methods for each UI panel
- **Error Handling**: Graceful fallbacks for missing assets

### File Organization:
- **Audio**: Keep all sound files in `sounds/` folder
- **Graphics**: Keep all sprites in `sprites/` folder
- **Fonts**: Keep custom fonts in `founts/` folder
- **Data**: High scores automatically saved to `high_scores.json`
- **Documentation**: Development guide in `PromptsAI.md`

---

## 🎮 How to Play

1. **Start**: Run `python main.py` and select "1 PLAYER"
2. **Learn**: Review the "How to Play" screen showing all vehicle types
3. **Play**: Use arrow keys to move, avoid enemies, collect fuel
4. **Pause**: Press ESC anytime to pause (P/ESC resume, R restart, SPACE menu)
5. **Survive**: Keep collecting fuel - game ends when fuel reaches zero
6. **Score**: Try to beat your high score and travel the furthest distance!

## 🏁 Game Objective

**Survive as long as possible** by:
- Avoiding collisions with enemy cars
- Collecting fuel from fuel stations
- Traveling the maximum distance
- Achieving the highest score

The game features three types of enemy cars with different behaviors, realistic collision physics, and a fuel management system that creates an engaging survival challenge.

---

**Enjoy the game! 🏁**

*For complete development documentation and replication guide, see `PromptsAI.md`*
