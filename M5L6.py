## IND-PS2-67-WED-19 shooter bagian 2

""" HUBUNGKAN MODUL """
import pygame
from random import randint

""" bagian variabel """
LEBAR_SCENE = 600
TINGGI_SCENE = 400
GAMBAR_BACKGROUND = "latar1.jpg"
GAMBAR_PLAYER1 = "rocket.png" 
GAMBAR_MUSUH1 = "ufo.png"
MUSIK_BACKGROUND = "space.ogg"
GAME_ON = True 
TERLEWAT = 0 ## melacak ikan yang terlewat
WARNA_HITAM = (0, 0, 0)

""" buat scene """
SCENE = pygame.display.set_mode((LEBAR_SCENE, TINGGI_SCENE))
pygame.display.set_caption("GAME TANK MELAWAN ALIEN")
BACKGROUND = pygame.transform.scale(pygame.image.load(GAMBAR_BACKGROUND), (LEBAR_SCENE, TINGGI_SCENE))
FPS = pygame.time.Clock()

""" buat musik """
pygame.mixer.init()
pygame.mixer.music.load(MUSIK_BACKGROUND)
# pygame.mixer.music.play()

""" buat font """
pygame.font.init()
FONT1 = pygame.font.Font(None, 35)

""" bagian kelas """
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, gambar, x, y, lebar, tinggi, kecepatan):
        super().__init__()
        self.gambar = pygame.transform.scale(pygame.image.load(gambar), (lebar, tinggi))
        self.kecepatan = kecepatan
        self.rect = self.gambar.get_rect() ## ini kotaknya
        self.rect.x = x # posisi X
        self.rect.y = y # posisi Y
        self.lebar = lebar
    def tampil(self):
        SCENE.blit(self.gambar, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def gerak(self):
        TOMBOL = pygame.key.get_pressed()
        if TOMBOL[pygame.K_a] and self.rect.x > 0: # kiri
            self.rect.x -= self.kecepatan
        if TOMBOL[pygame.K_d] and self.rect.x < LEBAR_SCENE-self.lebar: # kanan
            self.rect.x += self.kecepatan
class Enemy(GameSprite):
    def gerak(self):
        global TERLEWAT
        self.rect.y += self.kecepatan # turun otomatis
        ## jika kena bawah layar
        if self.rect.y > LEBAR_SCENE:
            self.rect.y = -100 # pindah lagi ke atas
            self.rect.x = randint(50, LEBAR_SCENE-self.lebar) # acak posisi X nya
            TERLEWAT += 1


""" bagian objek game """
PLAYER1 = Player(GAMBAR_PLAYER1, 50, TINGGI_SCENE-100, 100, 100, 15)

""" musuh / enemy """
GRUP_MUSUH = pygame.sprite.Group()
for a in range(5):
    MUSUH = Enemy(GAMBAR_MUSUH1, randint(50, LEBAR_SCENE-50), -100, 50, 50, randint(1, 3))
    GRUP_MUSUH.add(MUSUH)

""" game loop """
while GAME_ON:
    """ event handling untuk QUIT """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_ON = False ## matikan game

    """ tampilan game """
    SCENE.blit(BACKGROUND, (0, 0))
    PLAYER1.tampil()
    PLAYER1.gerak()

    """ tulisan score dan terlewat """
    TEKS_SCORE = FONT1.render("SCORE: " + str(TERLEWAT), 1, WARNA_HITAM)
    TEKS_TERLEWAT = FONT1.render("MISSED: " + str(TERLEWAT), 1, WARNA_HITAM)
    SCENE.blit(TEKS_SCORE, (50, 0))
    SCENE.blit(TEKS_TERLEWAT, (50, 50))

    """ grup musuh tampil dan gerakkan """
    for musuh in GRUP_MUSUH:
        SCENE.blit(musuh.gambar, musuh.rect)
        musuh.gerak()

    """ penting """
    FPS.tick(60)
    pygame.display.update()















