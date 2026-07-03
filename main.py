import pgzrun
import math
import random
from pygame import Rect

# oyun penceresi ayarları
WIDTH = 1000
HEIGHT = 600
TITLE = "Probably Cursed - Kodland"

# ilk aşamada menu, play ve game_over olacak
game_state = "menu"
sound_enabled = True # ses açık mı?

# menü butonları
play_btn = Rect((400, 200), (200, 50))
sound_btn = Rect((400, 300), (200, 50))
exit_btn = Rect((400, 400), (200, 50))

def draw():
    # şimdilik ekranı geçici bir renkle dolduralım
    screen.fill((68, 68, 69))

    if game_state == "menu":
        screen.draw.text(TITLE, center = (500, 100), fontsize = 50, color = "orange")

        screen.draw.filled_rect(play_btn, "green")
        screen.draw.filled_rect(sound_btn, "blue")
        screen.draw.filled_rect(exit_btn, "red")

        screen.blit("icons/play_icon", (play_btn.x + 80, play_btn.y))

        if sound_enabled:
            screen.blit("icons/sound_on_icon", (sound_btn.x + 80, sound_btn.y))
        else:
            screen.blit("icons/sound_off_icon", (sound_btn.x + 80, sound_btn.y))


        screen.blit("icons/exit_icon", (exit_btn.x + 80, exit_btn.y))

def update():
    pass

pgzrun.go()