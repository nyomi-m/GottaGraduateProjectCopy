import pygame
import sys

class Goal:
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image


    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500))
    goal_image = pygame.image.load("goal-clipart-goal-line.png")
    goal_image = pygame.transform.scale(goal_image, (60,60))
    goal = Goal(screen, 50, 400, goal_image)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((200, 200, 200))

        goal.draw()
        pygame.display.update()



main()