#/usr/bin/env python

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
        self.original = self.image

        
        self.speed = 0.0
        self.max_speed = 20.0
        self.accel_rate = 2.0
        
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
        if self.speed <= self.max_speed:
            self.speed += self.accel_rate
        print "speed " + repr(self.speed)

    def brake(self):
        if self.speed >= 1.0:
            self.speed /= 2.0
        else:
            self.speed = 0
        print "braking: " + repr(self.speed)

    def decay(self):
        self.brake()
        self.turn_speed=0

    def turn(self, direction):
        if self.turn_speed < self.turn_max:
            self.turn_speed += self.accel_rate
        self.last_heading = self.heading
        self.heading += self.turn_speed * direction
        print "heading" + repr(self.heading)

    def _spin(self):
        self.speed = 0
        pass

    def jump(self):
        self.jumping=1
        pass

    def _move(self):
        #x, y = self.position
        #vector = self.rect.pos() * self.speed
        center = self.rect.center
        if self.heading >= 360:
            self.heading -= 360
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.heading)
        self.rect = self.image.get_rect(center=center)
        print repr(self.rect) + repr(self.image)

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
        print "speed: " + repr(kart.speed) + "-- heading: " + repr(kart.heading)
        print pygame.key.get_pressed()

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    kart.turn(1)
                if event.key == K_RIGHT:
                    kart.turn(-1)
                if event.key == K_UP:
                    kart.accel()
                if event.key == K_DOWN:
                    kart.brake()
                else:
                    kart.decay()

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