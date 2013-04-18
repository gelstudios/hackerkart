#/usr/bin/env python

import os, pygame, random, math
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
    def __init__(self, img_name='kart.bmp'):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(img_name, -1)
        self.original = self.image
        self.original_rect = self.rect

        self.speed = 0.0
        self.max_speed = 60.0
        self.accel_rate = 0.5
        self.brake_rate = 1.1
        self.coast_rate = 1.025
        
        self.position = (0,0)
        self.last_position = (0,0)
        
        self.heading = 0
        self.last_heading = 0
        self.turn_speed = 0
        self.turn_max = 20
        self.turn_rate = 0.5

        self.jumping = 0
        self.spinning = 0

    def reset(self):
        self.rect = self.original_rect

    def accel(self):
        if self.speed < self.max_speed:
            self.speed += self.accel_rate
        elif self.speed > self.max_speed:
            self.coast()

    def brake(self):
        if self.speed >= 1.0:
            self.speed /= self.brake_rate
        else:
            self.speed = 0

    def coast(self):
        if self.speed >= 1.0:
            self.speed /= self.coast_rate
        else:
            self.speed = 0

    def turn(self, direction):
        if self.turn_speed < self.turn_max:
            self.turn_speed += self.turn_rate
        self.last_heading = self.heading
        self.heading += self.turn_speed/2 * direction
        self.heading %= 360

    def _spin(self):
        self.speed = 0
        pass

    def jump(self):
        self.jumping=1
        pass

    def _move(self):
        self.last_position = self.position
        amt_x = self.speed/2 * math.cos( math.radians(self.heading) )
        amt_y = self.speed/2 * math.sin( math.radians(self.heading) )
        newpos = self.rect.move((amt_x , -amt_y)) #i dont know why amt_y needs to be negative!
        self.rect = newpos

        center = self.rect.center
        rotate = pygame.transform.rotate
        rotozoom = pygame.transform.rotozoom
        self.image = rotate(self.original, self.heading)
        #self.image = rotozoom(self.original, self.heading, 2)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        if self.spinning:
            self._spin()
        else:
            self._move()

class Track(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('track.png',)
        self.rotation = 0
        self.walls = []
        self.startposition = (0,0)

    def update(self):
        pass

tileatlas = {
'default':{'base_fname':'default', 'ext':'.png', 'anim':1, 'frames':4, 'collision_type':0, 'speed_mod':1.0},
'pave': {'base_fname':'pave',  'ext':'.png', 'anim':0, 'frames':1, 'collision_type':0, 'speed_mod':1.0},
'star': {'base_fname':'star',  'ext':'.png', 'anim':1, 'frames':5, 'collision_type':0, 'speed_mod':1.0},
'coin': {'base_fname':'coin',  'ext':'.png', 'anim':2, 'frames':2, 'collision_type':2, 'speed_mod':1.0},
'item': {'base_fname':'item',  'ext':'.png', 'anim':2, 'frames':2, 'collision_type':2, 'speed_mod':1.0},
'boost':{'base_fname':'boost', 'ext':'.png', 'anim':1, 'frames':2 , 'collision_type':0, 'speed_mod':1.5},
'ramp': {'base_fname':'ramp',  'ext':'.png', 'anim':1, 'frames':2, 'collision_type':0, 'speed_mod':1.5},
'dirt': {'base_fname':'dirt',  'ext':'.png', 'anim':0, 'frames':1, 'collision_type':0, 'speed_mod':0.75},
'wall': {'base_fname':'wall',  'ext':'.png', 'anim':0, 'frames':1, 'collision_type':1, 'speed_mod':0.5},
'spawn':{'base_fname':'spawn', 'ext':'.png', 'anim':0, 'frames':1, 'collision_type':0, 'speed_mod':1.0},
'check':{'base_fname':'check', 'ext':'.png', 'anim':0, 'frames':1, 'collision_type':0, 'speed_mod':1.0},
'fline':{'base_fname':'fline', 'ext':'.png', 'anim':0, 'frames':1, 'collision_type':0, 'speed_mod':1.0},
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type='default'):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        global tileatlas
        tile=tileatlas.get(tile_type, 'default')
        filename = tile['base_fname'] + str(0) + tile['ext']

        self.image, self.rect = load_image(filename,)
        self.tile_type = tile_type
        self.collision_type = tile['collision_type']
        self.speed_mod = tile['speed_mod']

        self.anim = tile['anim'] #load animation frames, and change the update method
        if self.anim:
            self.frame = 0
            self.frames = []
            for f in range(tile['frames']):
                filename = tile['base_fname'] + str(f) + tile['ext']
                image, rect = load_image(filename,)
                self.frames.append(image)

            self.update = self._anim_update

        self.status = None

    def _anim_update(self):
        #get frames, load the next frame when this method is called
        if self.anim == 1:
            self.image = self.frames[self.frame]
        if self.anim == 2:
            pass

        if self.frame == len(self.frames)-1:
            self.frame = 0
        else:
            self.frame += 1

    def update(self):
        pass

class Hud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('hud.bmp', -1)

    def update(self):
        pass

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop"""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption('hacker kart')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    tile = Tile()
    track = Track()
    kart = Kart()
    allsprites = pygame.sprite.RenderPlain((kart, tile, track))

#Main Loop
    while 1:
        clock.tick(60)
        print "speed: " + repr(kart.speed) + " -- heading: " + repr(kart.heading) + " -- turn_speed: " + repr(kart.turn_speed)

        keys = pygame.key.get_pressed() #get keys held down in between frames

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    kart.jump()
                if event.key == K_SPACE:
                    kart.reset()

        if keys[K_LEFT]:
            kart.turn(1)
        elif keys[K_RIGHT]:
            kart.turn(-1)
        else:
            kart.turn_speed=0

        if keys[K_UP]:
            kart.accel()
        elif keys[K_DOWN]:
            kart.brake()
        else:
            kart.coast()
            
#       for racer in racers:
#                   if track.terrain(racer):
#                      chimp.punched()
#                 else:
        allsprites.update()

    #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.sprite.RenderPlain((tile)).draw(screen)
        pygame.sprite.RenderPlain((kart)).draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()