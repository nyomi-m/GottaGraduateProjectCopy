import pygame
import sys



class Student:
    def __init__(self, screen, x, y, image, speed):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.speed = speed
        self.walk_count = 0
        self.is_jump = False
        self.jump_count = 8

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_RIGHT]:
            if self.walk_count < 5:
                self.image = pygame.image.load('elephant_right.png')
                self.walk_count += 1
            else:
                self.image = pygame.image.load('elephant_right_still.png')
                self.walk_count += 1
                if self.walk_count > 10:
                    self.walk_count = 0
            self.x += self.speed

        if pressed_key[pygame.K_LEFT] and self.x >= 0:
            if self.walk_count < 5:
                self.image = pygame.image.load('elephant_left.png')
                self.walk_count += 1
            else:
                self.image = pygame.image.load('elephant_left_still.png')
                self.walk_count += 1
                if self.walk_count > 10:
                    self.walk_count = 0
            self.x -= self.speed

    def jump(self):
        pressed_key = pygame.key.get_pressed()
        if not self.is_jump:
            if pressed_key[pygame.K_SPACE]:
                self.is_jump = True
        else:
            if self.jump_count >= -8:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 8


# def main():
#     pygame.init()
#     clock = pygame.time.Clock()
#     screen = pygame.display.set_mode((500, 500))
#     image = 'elephant_right_still.png'
#     student = Student(screen, 50, 400, image, 3)
#
#     while True:
#         clock.tick(60)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#         screen.fill((200, 200, 200))
#
#         student.move()
#         student.draw()
#         student.jump()
#         pygame.display.update()
#
#
#
# main()
