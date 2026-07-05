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

class Entity:
    def __init__(self, grid_x, grid_y, base_name, frame_counts):
        self.grid_x = grid_x
        self.grid_y = grid_y

        # ekrandaki gerçek konum
        self.x = self.grid_x * TILE_SIZE
        self.y = self.grid_y * TILE_SIZE

        self.hp = 3
        self.speed = 4

        self.base_name = base_name
        self.frame_counts = frame_counts # örneğin {"idle": 2, "walk": 8}
        self.state = "idle"

        self.frame_index = 0
        self.animation_timer = 0
        self.update_sprite_list()

    def update_sprite_list(self):
        self.imgs = []

        # o state için kaç görsel var?
        count = self.frame_counts[self.state]

        for i in range (1, count + 1):
            self.imgs.append(f"{self.base_name}_{self.state}_{i}")

        self.current_img = self.imgs[self.frame_index]

    def update(self):
        # hedef konum
        target_x = self.grid_x * TILE_SIZE
        target_y = self.grid_y * TILE_SIZE

        is_moving = False
        
        if self.x < target_x:
            self.x += min(self.speed, target_x - self.x)
            is_moving = True
        elif self.x > target_x:
            self.x -= min(self.speed, self.x - target_x)
            is_moving = True
        if self.y < target_y:
            self.y += min(self.speed, target_y - self.y)
            is_moving = True
        elif self.y > target_y:
            self.y -= min(self.speed, self.y - target_y)
            is_moving = True

        new_state = "walk" if is_moving else "idle"

        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self.update_sprite_list()

        self.animation_timer += 1
        if self.animation_timer >= 6 and self.state == "walk":
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.imgs)
            self.current_img = self.imgs[self.frame_index]
        elif self.animation_timer >= 30 and self.state == "idle":
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.imgs)
            self.current_img = self.imgs[self.frame_index]

    def draw(self):
        screen.blit(self.current_img, (self.x, self.y))

class Player(Entity):
    def move(self, dx, dy):
        # gitmek istenen yeni konum
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        # ekrandan çıkmaması için
        if 0 <= new_x < COLS and 0 <= new_y < ROWS:
            self.grid_x = new_x
            self.grid_y = new_y

class Enemy(Entity):
    def __init__(self, grid_x, grid_y, base_name, frame_counts, patrol_axis, patrol_dist):
        super().__init__(grid_x, grid_y, base_name, frame_counts)

        self.start_x = grid_x
        self.start_y = grid_y
        self.patrol_axis = patrol_axis # "x ekseninde mi y ekseninde mi gezecek?
        self.patrol_dist = patrol_dist # merkezden kaç adım uzağa gidebilri?

        self.direction = 1
        self.move_timer = 0

    def bot_move(self):
            self.move_timer += 1
            if self.move_timer >= 60:
                self.move_timer = 0

                if self.patrol_axis == "x":
                    new_x = self.grid_x + self.direction

                    # menzilini aşmışsa veya ekranın dışına çıkmışsa
                    if abs(new_x - self.start_x) >= self.patrol_dist or not (0 <= new_x < COLS):
                        self.direction *= -1
                        new_x = self.grid_x + self.direction

                    self.grid_x = new_x

                elif self.patrol_axis == "y":
                    new_y = self.grid_y + self.direction
                    
                    if abs(new_y - self.start_y) >= self.patrol_dist or not (0 <= new_y < ROWS):
                        self.direction *= -1
                        new_y = self.grid_y + self.direction
                    
                    self.grid_y = new_y

class Potion:
    def __init__(self, grid_x, grid_y, img, is_poison=False):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.is_poison = is_poison
        self.collected = False

        self.actor = Actor(img)

        center_x = (self.grid_x * TILE_SIZE) + (TILE_SIZE //  2)
        bottom_y = (self.grid_y * TILE_SIZE) + TILE_SIZE

        self.actor.midbottom = (center_x, bottom_y)

    def draw(self):
        if not self.collected:
            self.actor.draw()


our_hero = Player(0, 0, "hero", {"idle": 2, "walk": 8})
zombie = Enemy(10, 5, "zombie", {"idle": 2, "walk": 4}, "x", 3)
robot = Enemy(15, 2, "robot", {"idle": 2, "walk": 4}, "y", 4)

# iksirleri haritaya diziyoruz (1 tanesi zehirli)
potions = [
    Potion(17, 2, "potion_1"),
    Potion(18, 5, "potion_2"),
    Potion(15, 3, "potion_3"),
    Potion(17, 6, "potion_4", is_poison=True)
]
collected_potions = 0

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

        # önce iksirleri çizelim ki kahramanımız üstlerine basabilsin
        for p in potions:
            p.draw()

        our_hero.draw()
        zombie.draw()
        robot.draw()

        # sol üstte canımız
        screen.draw.text(f"CAN: {our_hero.hp}", topleft=(20, 20), fontsize=40, color="red")
        
        # toplanan iksir sayacı
        screen.draw.text(f"IKSIR: {collected_potions}/3", topleft=(20, 60), fontsize=40, color="yellow")

        screen.draw.text("DIKKAT: Kirmizi iksirlerden uzak dur!", topleft=(20, 100), fontsize=30, color="red")

    # maalesef kaybettik
    elif game_state == "game_over":
        screen.draw.text("OYUN BITTI!", center=(500, 250), fontsize=80, color="red")
        screen.draw.text("Menuye Don", center=(500, 350), fontsize=40, color="white")

    # kazandık, süper
    elif game_state == "win":
        screen.draw.text("KAZANDIN!", center=(500, 250), fontsize=80, color="green")
        screen.draw.text("Menuye Don", center=(500, 350), fontsize=40, color="white")

def update():
    global game_state, collected_potions
    our_hero.update()

    if game_state == "play":
        zombie.bot_move()
        zombie.update()

        robot.bot_move()
        robot.update()

        # iksir toplama kontrolleri
        for p in potions:
            if not p.collected and our_hero.grid_x == p.grid_x and our_hero.grid_y == p.grid_y:
                p.collected = True
                
                # zehirliyse canımız azalsın
                if p.is_poison:
                    our_hero.hp -= 1
                    
                    if sound_enabled:
                        sounds.hit.play()
                    
                    if our_hero.hp <= 0:
                        game_state = "game_over"
                        if sound_enabled:
                            music.stop()
                            sounds.game_over.play()
                # zehirli değilse sayacı artır
                else:
                    collected_potions += 1
                    if sound_enabled:
                        sounds.drink.play()
                        
                    if collected_potions >= 3:
                        game_state = "win"
                        if sound_enabled:
                            music.stop()
                            sounds.win.play()

        # kahramanımız ve zombi veya robot aynı hücredeyse yandık
        if (our_hero.grid_x == zombie.grid_x and our_hero.grid_y == zombie.grid_y) or (our_hero.grid_x == robot.grid_x and our_hero.grid_y == robot.grid_y):
            our_hero.hp -= 1
            
            if sound_enabled:
                sounds.hit.play()
            
            # hop başlangıç noktasına ışınlan
            our_hero.grid_x = 0
            our_hero.grid_y = 0
            our_hero.x = 0
            our_hero.y = 0
            
            # can sıfırlandıysa
            if our_hero.hp <= 0:
                game_state = "game_over"
                if sound_enabled:
                    music.stop()
                    sounds.game_over.play()

def on_mouse_down(pos):
    global game_state, sound_enabled, collected_potions

    # menüdeysek tıklamaların sonuçları
    if game_state == "menu":
        # tıklanan nokta play butonunun içinde mi?
        if play_btn.collidepoint(pos):
            print("Emin misin? Basarilar!")
            game_state = "play"
            
            if sound_enabled:
                music.play("bg_music")
        
        # tıklanan nokta sound butonunun içinde mi?
        elif sound_btn.collidepoint(pos):
            sound_enabled = not sound_enabled # sound_enabled'ı toggle et (true ise false, false ise true yap)
            print(f"Ses durumu: {sound_enabled}")
            
            if not sound_enabled:
                music.stop()
            elif game_state == "play" and sound_enabled:
                music.play("bg_music")

        elif exit_btn.collidepoint(pos):
            print("Olamaz! Nereye gidiyorsun?")
            exit()

    # game over veya win ekranındayken tıklarsak menüye dönelim ve her şeyi sıfırlayalım
    elif game_state == "game_over" or game_state == "win":
        game_state = "menu"
        our_hero.hp = 3
        collected_potions = 0
        
        # kahramanı başa al
        our_hero.grid_x = 0
        our_hero.grid_y = 0
        our_hero.x = 0
        our_hero.y = 0

        # iksirleri haritaya geri koy
        for p in potions:
            p.collected = False

def on_key_down(key):
    if game_state == "play":
        if key == keys.LEFT or key == keys.A:
            our_hero.move(-1, 0)
        elif key == keys.RIGHT or key == keys.D:
            our_hero.move(1, 0)
        elif key == keys.UP or key == keys.W:
            our_hero.move(0, -1) # bilgisayarlar biraz garip
        elif key == keys.DOWN or key == keys.S:
            our_hero.move(0, 1)

pgzrun.go()