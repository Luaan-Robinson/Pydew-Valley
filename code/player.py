import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, group):
    super().__init__(group) #as soon as an instance of this class is created, it will automatically be added to the group that is passed in as an argument

    self.import_assets() # must be at the top of the init method so that the animations are imported before the image is set
    self.status = 'down_idle'
    self.frame_index = 0 # no clue what this does bruv


    # general setup
    self.image = self.animations[self.status][self.frame_index]
   # self.image.fill('green')
    self.rect = self.image.get_rect(center = pos)

    # movement attibutes
    self.direction = pygame.math.Vector2()
    self.pos = pygame.math.Vector2(self.rect.center)
    self.speed = 200

  def import_assets(self):
     self.animations = {'up': [], 'down' :[], 'left' : [], 'right' : [],
                        'right_idle': [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : [],
                        'right_hoe': [], 'left_hoe' : [], 'up_hoe' : [], 'down_hoe' : [],
                        'right_axe' : [], 'left_axe' : [], 'up_axe' : [], 'down_axe' : [],
                        'right_water': [], 'left_water' : [], 'up_water' : [], 'down_water' : []}
     for animation in self.animations.keys():
        full_path = './graphics/character/' + animation
        self.animations[animation] = import_folder(full_path)

  def animate(self, dt):
     self.frame_index += 4 * dt
     if self.frame_index >= len(self.animations[self.status]): # helps prevent the frame index from going out of bounds
        self.frame_index = 0
     self.image = self.animations[self.status][int(self.frame_index)] # look here man, I'm already getting lost

  def input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        self.direction.y = -1
        self.status = 'up'
    elif keys[pygame.K_DOWN]:
        self.direction.y = 1
        self.status = 'down'
    else:
       self.direction.y = 0    

    if keys[pygame.K_RIGHT]:
        self.direction.x = 1
        self.status = 'right'
    elif keys[pygame.K_LEFT]:
          self.direction.x = -1  
          self.status = 'left'      
    else:
       self.direction.x = 0    

  def get_status(self):
     if  self.direction.magnitude() == 0:
        self.status = self.status.split('_')[0] + '_idle' # the first item returned from this list will always be the status

  def move(self, dt):

    # normalizing a vector
     if self.direction.magnitude() > 0:
      self.direction = self.direction.normalize()

      # horizontal movement
     self.pos.x += self.direction.x * self.speed * dt
     self.rect.centerx = self.pos.x
     # vertical movement
     self.pos.y += self.direction.y * self.speed * dt
     self.rect.centery = self.pos.y

  def update(self, dt):
    self.input()
    self.get_status()
    self.move(dt)
    self.animate(dt)
