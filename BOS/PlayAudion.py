import pygame

def play_audio(file_path):
    pygame.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 990))  # Wait for the sound to finish playing
    pygame.quit()  # Quit pygame to release resources
