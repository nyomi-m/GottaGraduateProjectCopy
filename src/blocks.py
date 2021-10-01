import pygame
import sys
import Character
from Character import Student
import Character as ch



class Block:

    def __init__(self, screen, x, y, color, speedx, speedy, clock_tick):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.speed_x = speedx
        self.speed_y = speedy
        self.rect = 0
        self.clock = clock_tick

    def draw(self):
        self.rect = pygame.Rect(self.x,self.y,60,20)
        pygame.draw.rect(self.screen,self.color,self.rect)

    def move(self):  # a given list of indices will be in puted, those are the rectangles that will move across screen

        self.x = self.x + self.speed_x  # notice this is mutated

        if (self.x + 60 > self.screen.get_width()) or (self.x < 0):
            self.speed_x = -self.speed_x

        self.y = self.y + self.speed_y  # notice this is mutated

        if (self.y + 20 > self.screen.get_height()) or (self.y < 0):
            self.speed_y = -self.speed_y

    def fall(self):
       self.y = self.y - 0.5*9.81*(self.clock)**(-2)

    def hit_by(self,student):
        return self.rect.collidepoint(student.x,student.y)



def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Blocks')
    screen.fill(pygame.Color('gray'))
    clock = pygame.time.Clock()
    block_x = 180
    block_y = 420
    color = (255, 0, 0)
    blocks = Block(screen, block_x, block_y, color, 1, 1, 60)


    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(pygame.Color('gray'))
        blocks.draw()
        blocks.move()

        pygame.display.update()


# main()
