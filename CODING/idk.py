import wave
import pygame
from pygame import mixer

mixer.init(frequency=44100, size=-16, channels=2)

file_name = "2.mp3"
    
# load a sound file
sound = mixer.Sound(file_name)
sound.play()
# play the sound on channel 0
channel = pygame.mixer.Channel(0)
channel.play(sound)
