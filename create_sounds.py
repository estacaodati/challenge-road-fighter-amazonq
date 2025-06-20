import wave
import math
import struct
import os

def create_wav_file(filename, frequency, duration, sample_rate=44100, amplitude=0.5):
    """Create a simple WAV file with a sine wave"""
    frames = int(duration * sample_rate)
    
    # Ensure sounds directory exists
    os.makedirs("sounds", exist_ok=True)
    
    # Full path to sounds folder
    filepath = os.path.join("sounds", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate sine wave data
        for i in range(frames):
            # Calculate sine wave value
            time_point = float(i) / sample_rate
            wave_value = amplitude * math.sin(frequency * 2 * math.pi * time_point)
            
            # Apply fade out to avoid clicks
            fade = 1.0 - (float(i) / frames)
            wave_value = wave_value * fade
            
            # Convert to 16-bit integer
            sample = int(wave_value * 32767)
            
            # Write stereo sample (left and right channels)
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)

def create_background_music(filename, duration=10.0):
    """Create a more complex background music track"""
    sample_rate = 44100
    frames = int(duration * sample_rate)
    
    # Ensure sounds directory exists
    os.makedirs("sounds", exist_ok=True)
    
    # Full path to sounds folder
    filepath = os.path.join("sounds", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate background music with multiple layers
        for i in range(frames):
            time_point = float(i) / sample_rate
            
            # Base rhythm (low frequency)
            base = 0.3 * math.sin(2 * math.pi * 80 * time_point)
            
            # Mid-range harmony
            harmony = 0.2 * math.sin(2 * math.pi * 160 * time_point)
            
            # High frequency sparkle
            sparkle = 0.1 * math.sin(2 * math.pi * 320 * time_point)
            
            # Combine all layers
            combined = base + harmony + sparkle
            
            # Apply gentle volume variation
            volume_variation = 0.8 + 0.2 * math.sin(2 * math.pi * 0.5 * time_point)
            combined *= volume_variation
            
            # Convert to 16-bit integer
            sample = int(combined * 16383)  # Lower amplitude for background
            
            # Write stereo sample
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)

# Create sound files
print("Creating sound files in sounds/ folder...")

try:
    # Collision sound - low frequency
    create_wav_file("collision.wav", 200, 0.3, amplitude=0.3)
    print("Created sounds/collision.wav")
    
    # Fuel pickup sound - high frequency
    create_wav_file("fuel.wav", 800, 0.2, amplitude=0.2)
    print("Created sounds/fuel.wav")
    
    # Menu sound - medium frequency
    create_wav_file("menu.wav", 600, 0.1, amplitude=0.1)
    print("Created sounds/menu.wav")
    
    # Background engine sound - very low frequency (legacy)
    create_wav_file("engine.wav", 60, 2.0, amplitude=0.05)
    print("Created sounds/engine.wav")
    
    # New background music - more complex
    create_background_music("background.wav", duration=15.0)
    print("Created sounds/background.wav")
    
    print("\n✅ All sound files created successfully in sounds/ folder!")
    print("🎵 You can now replace these with your own custom sounds")
    print("📁 Just make sure to keep the same filenames")
    print("🎼 background.wav is the main background music file")
    
except Exception as e:
    print(f"❌ Error creating sound files: {e}")
