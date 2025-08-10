# Maze Game in Python using Pygame
# Import necessary libraries
from pygame import * 
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # each sprite must store an image property
       self.image = transform.scale(image.load(player_image), (55, 55))
       self.speed = player_speed
       # each sprite must store the rect property it is inscribed in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

    #method for updating the sprite position
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#child class for the player sprite (controlled by arrows)
class Player(GameSprite):
    def update(self):
       keys = key.get_pressed() # get the state of all keys
       if keys[K_LEFT] and self.rect.x > 5: # check if the left arrow is pressed and if the player is not at the left edge
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 80:
           self.rect.y += self.speed

#child class for the enemy sprite (moves itself)
class Enemy(GameSprite):
    def update(self): # check the position of the enemy and change its direction
       if self.rect.x <= 470:
           self.side = "right"
       if self.rect.x >= win_width - 85:
           self.side = "left"
       if self.side == "left":
           self.rect.x -= self.speed
       else:
           self.rect.x += self.speed

#class for obstacle sprites
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
       super().__init__() # call the parent class constructor
       self.color_1 = color_1
       self.color_2 = color_2
       self.color_3 = color_3
       self.width = wall_width
       self.height = wall_height

       # picture of the wall — a rectangle of the desired size and color
       self.image = Surface((self.width, self.height))
       self.image.fill((color_1, color_2, color_3))
       
       # each sprite must store a rect property
       self.rect = self.image.get_rect()
       self.rect.x = wall_x
       self.rect.y = wall_y
    def draw_wall(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
       #draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))

#Game scene:
win_width = 700
win_height = 500

# Initialize Pygame
window = display.set_mode((win_width, win_height))

# Set the window title
display.set_caption("Maze")

# Load background image and scale it to fit the window
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

#Game characters:
player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

# Create walls (obstacles) in the game
w1 = Wall(154, 205, 50, 100, 20 , 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20 , 10, 380)

game = True # game state variable
finish = False # game state variable
clock = time.Clock()
FPS = 60

# Initialize the font for displaying messages
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

# Initialize the mixer for sound effects
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

# Start the game loop
while game:
    # Handle events
    for e in event.get():
        if e.type == QUIT:
           game = False
    
    # Draw the background
    if finish != True:
        window.blit(background,(0, 0))
        player.update() # update player position
        monster.update()
        player.reset() # draw player
        monster.reset()
        final.reset()

        # Draw walls 
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        # Check for collisions
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2)or sprite.collide_rect(player, w3):
           finish = True # "Losing" situation
           window.blit(lose, (200, 200))
           kick.play()


        # Check if the player reaches the final sprite (treasure)
        if sprite.collide_rect(player, final):
           finish = True # "Winning" situation
           window.blit(win, (200, 200))
           money.play()

    display.update() # update the display
    clock.tick(FPS) # set the frame rate
