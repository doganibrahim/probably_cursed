import pgzrun
import math
import random
from pygame import Rect

# oyun penceresi ayarları
WIDTH = 1000
HEIGHT = 600
TITLE = "Probably Cursed - Kodland"

TILE_SIZE = 50
COLS = WIDTH // TILE_SIZE
ROWS = HEIGHT // TILE_SIZE

# ilk aşamada menu, play ve game_over olacak
game_state = "menu"
sound_enabled = True # ses açık mı?

# menü butonları
play_btn = Rect((400, 200), (200, 50))
sound_btn = Rect((400, 300), (200, 50))
exit_btn = Rect((400, 400), (200, 50))

def draw_grid():
    """
    Oyun alanini esit karelere boler.
    """
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE # örn. ilk col. pixel = 50
            y = row * TILE_SIZE

            # kareleri iki farklı renkle çizerek grid yapısını belirginleştirelim
            if (row + col) % 2 == 0:
                color = (50, 50, 55)
            else:
                color = (60, 60, 65)

            screen.draw.filled_rect(Rect((x, y), (TILE_SIZE, TILE_SIZE)), color)

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

    elif game_state == "play":
        draw_grid()

def update():
    pass

def on_mouse_down(pos):
    global game_state, sound_enabled

    # menüdeysek tıklamaların sonuçları
    if game_state == "menu":
        # tıklanan nokta play butonunun içinde mi?
        if play_btn.collidepoint(pos):
            print("Emin misin? Basarilar!")
            game_state = "play"
        
        # tıklanan nokta sound butonunun içinde mi?
        elif sound_btn.collidepoint(pos):
            sound_enabled = not sound_enabled # sound_enabled'ı toggle et (true ise false, false ise true yap)
            print(f"Ses durumu: {sound_enabled}")

        elif exit_btn.collidepoint(pos):
            print("Olamaz! Nereye gidiyorsun?")
            exit()


pgzrun.go()