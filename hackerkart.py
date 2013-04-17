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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('kart.bmp', -1)
        self.original = self.image

        
        self.speed = 0.0
        self.max_speed = 30.0
        self.accel_rate = 1.0
        self.brake_rate = 2.0
        self.coast_rate = 1.05
        
        self.position = (0,0)
        self.last_position = (0,0)
        
        self.heading = 0
        self.last_heading = 0
        self.turn_speed = 0
        self.turn_max = 10
        self.turn_rate = 1

        self.jumping = 0
        self.spinning = 0

    def accel(self):
        if self.speed < self.max_speed:
            self.speed += self.accel_rate

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
        print "coasting"

    def turn(self, direction):
        if self.turn_speed < self.turn_max:
            self.turn_speed += self.turn_rate
        self.last_heading = self.heading
        self.heading += self.turn_speed * direction
        self.heading %= 360

    def _spin(self):
        self.speed = 0
        pass

    def jump(self):
        self.jumping=1
        pass

    def _move(self):
        self.position = self.last_position
        x, y = self.position
        x = self.speed * math.cos(math.radians(self.heading))
        y = self.speed * math.sin(math.radians(self.heading))
        print "x: " + repr(x) + "y: " + repr(y)

        newpos = self.rect.move((x, y))
        self.rect = newpos

        center = self.rect.center
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.heading)
        self.rect = self.image.get_rect(center=center)


    def update(self):
        if self.spinning:
            self._spin()
        else:
            self._move()

class Track(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('track.bmp', -1)
        self.rotation = 0
        self.walls = []
        self.startposition = (0,0)

    def update(self):
        pass

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
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
    track = Track()
    kart = Kart()
    allsprites = pygame.sprite.RenderPlain((track, kart))

#Main Loop
    while 1:
        clock.tick(60)
        print "speed: " + repr(kart.speed) + " -- heading: " + repr(kart.heading) + " -- turn_speed: " + repr(kart.turn_speed)

        keys = pygame.key.get_pressed()

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    kart.jump()

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
        pygame.display.flip()

if __name__ == '__main__': main()