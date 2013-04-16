import os, pygame, random
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Kart(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('kart.bmp', -1)
        self.speed = 0
        self.position = (0,0)
        self.heading = 0
        self.turning = 0

    def turn(self):
    	if self.turning:
    		self.heading += self.turning
    	pass

    def spin(self):
    	self.speed = 0
    	pass

    def jump(self):
    	pass

    def update(self):
    	x, y = self.position
    	vector = self.speed * self.heading
    	#get new position?

class Track(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('track.bmp', -1)
        self.rotation = 0
        self.walls = []
        


