import pygame
import sys

pygame.init()

pygame.display.set_caption("Gotta Graduate!")
screen = pygame.display.set_mode((1300, 500))

#Putting sounds at the top to clean up a little
music = pygame.mixer.Sound("mixkit-delightful-4.wav")
music.play(100) #Loop it for an impossibly long amount of time
jump_sound = pygame.mixer.Sound("jump.wav")
highlight_sound = pygame.mixer.Sound("bloop.wav")
restart_sound = pygame.mixer.Sound('mixkit-losing-drums-2023.wav')

#goal image load
goal_image = pygame.image.load("goal_fix.png")
goal_image = pygame.transform.scale(goal_image, (60, 60))


##level backdrops
lvl1backdrop = pygame.image.load("Rose.jpg")
lvl1backdrop = pygame.transform.scale(lvl1backdrop,(screen.get_width(), screen.get_height()))

lvl2backdrop = pygame.image.load("level2Backdrop.PNG")
lvl2backdrop = pygame.transform.scale(lvl2backdrop,(screen.get_width(),screen.get_height()))

lvl3backdrop = pygame.image.load("level3Backdrop.PNG")
lvl3backdrop = pygame.transform.scale(lvl3backdrop,(screen.get_width(),screen.get_height()))

lvl4backdrop = pygame.image.load("level4Backdrop.PNG")
lvl4backdrop = pygame.transform.scale(lvl4backdrop,(screen.get_width(),screen.get_height()))
 
lvl5backdrop = pygame.image.load("level5Backdrop.PNG")
lvl5backdrop = pygame.transform.scale(lvl5backdrop,(screen.get_width(),screen.get_height()))

##load elephant image
elephant_left = pygame.image.load("elephant_left.png")
elephant_big = pygame.transform.scale(elephant_left,(200,150))

#load diploma image
diploma = pygame.image.load('diploma2.png')
diploma = pygame.transform.scale(diploma,(60,60))


#Colors
rose_red = (184, 6, 23)
light_red = (244, 6, 23)

#Fonts
title_text = pygame.font.SysFont('impact', 100)
advance_text = pygame.font.SysFont('impact', 50)
small_text = pygame.font.SysFont('arial', 30)


class Goal:
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image
        self.box = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class Goose:
    def __init__(self, screen, x, y, image, image2, speed):
        self.screen = screen
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.current_image = pygame.image.load(image)
        self.image2 = pygame.image.load(image2)
        self.move_count = 0
        self.direction = 'right'
        self.chase_count = 0

    def draw(self):
        self.screen.blit(self.current_image, (self.x, self.y))

    def move(self):
        if self.x > self.screen.get_width() - self.image.get_width():
            self.speed = -self.speed
            self.direction = 'left'
        if self.x < 0:
            self.speed = -self.speed
            self.direction = 'right'

        if self.direction == 'right':
            if self.move_count < 20:
                self.current_image = pygame.image.load('Goose_right_wings.png')
                self.move_count += 1
            else:
                self.current_image = pygame.image.load('goose_right.png')
                self.move_count += 1
            if self.move_count > 40:
                self.move_count = 0
            self.x += self.speed

        if self.direction == 'left':
            if self.move_count < 20:
                self.current_image = pygame.image.load('Goose_left_wings.png')
                self.move_count += 1
            else:
                self.current_image = pygame.image.load('goose_left.png')
                self.move_count += 1
            if self.move_count > 40:
                self.move_count = 0
            self.x += self.speed

    def chase(self, student_x, student_y):
        if self.x - student_x == 0 and self.y < student_y:
            self.y += 2
        elif self.x - student_x == 0 and self.y > student_y:
            self.y -= 2
        else:
            slope = abs(round((self.y - student_y) // (self.x - student_x)))
            if self.y == student_x and self.x < student_x:
                self.x += 3
            elif self.y == student_x and self.x > student_x:
                self.x -= 3
            elif slope > 3 and self.y < student_y:
                self.y += 2
            elif slope > 4 and self.y > student_y:
                self.y -= 2
            elif self.x >= student_x and self.y > student_y:
                self.x -= 1
                self.y -= slope
                self.direction = 'left'
            elif self.x <= student_x and self.y >= student_y:
                self.x += 1
                self.y -= slope
                self.direction = 'right'
            elif self.x >= student_x and self.y <= student_y:
                self.x -= 1
                self.y += slope
                self.direction = 'left'
            else:
                self.x += 1
                self.y += slope
                self.direction = 'right'

        if self.direction == 'right':
            if self.chase_count < 20:
                self.current_image = pygame.image.load('Goose_right_wings.png')
                self.chase_count += 1
            else:
                self.current_image = pygame.image.load('goose_right.png')
                self.chase_count += 1
            if self.chase_count > 40:
                self.chase_count = 0

        if self.direction == 'left':
            if self.chase_count < 20:
                self.current_image = pygame.image.load('Goose_left_wings.png')
                self.chase_count += 1
            else:
                self.current_image = pygame.image.load('goose_left.png')
                self.chase_count += 1
            if self.chase_count > 40:
                self.chase_count = 0

    def get_distance(self, x, y):
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** (1/2)

    def restart(self):
        self.x = self.original_x
        self.y = self.original_y
        self.direction = 'right'
        if self.speed < 0:
            self.speed = -self.speed

class Block:

    def __init__(self, screen, x_list, y_list,speedx,speedy,color):
        self.screen = screen
        self.x_list = x_list
        self.y_list = y_list
        self.color = color
        self.speedx = speedx
        self.speedy = speedy
        self.bloc = []
        self.is_moving = []

    def load_bloc(self):
        for k in range(len(self.x_list)):
            self.bloc = self.bloc + [pygame.Rect(self.x_list[k], self.y_list[k], 60, 10)]


    def draw(self):
        for k in range(len(self.bloc)):
            pygame.draw.rect(self.screen,self.color,self.bloc[k])


    def move_horizontal(self,index,leftbound,rightbound):

        self.bloc[index].x = self.bloc[index].x + self.speedx[index]
        if self.bloc[index].x > rightbound:
            self.speedx[index] = -self.speedx[index]
        if self.bloc[index].x < leftbound:
            self.speedx[index] = -self.speedx[index]

    def move_vertical(self,index,upperbound,lowerbound):
        self.bloc[index].y = self.bloc[index].y + self.speedy[index]
        if self.bloc[index].y > lowerbound:
            self.speedy[index] = -self.speedy[index]
        if self.bloc[index].y < upperbound:
            self.speedy[index] = -self.speedy[index]


class Student:
    def __init__(self, screen, x, y, image, speed):
        self.screen = screen
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.walk_count = 0
        self.is_jump = True
        self.is_fall = True
        self.jump_count = 8

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.walk_count < 5:
            self.image = pygame.image.load('elephant_left_still.png')
            self.walk_count += 1
        else:
            self.image = pygame.image.load('elephant_left.png')
            self.walk_count += 1
        if self.walk_count > 10:
            self.walk_count = 0
            self.x -= self.speed
        self.x -= 5

    def move_right(self):
        if self.walk_count < 5:
            self.image = pygame.image.load('elephant_right.png')
            self.walk_count += 1
        else:
            self.image = pygame.image.load('elephant_right_still.png')
            self.walk_count += 1
        if self.walk_count > 10:
            self.walk_count = 0
            self.x -= self.speed
        self.x += 5

    def gravity(self):
        if self.is_fall:
                self.y+=self.speed*2


    def jump(self):
        if self.is_jump:
            self.is_jump = False
        else:
            if self.jump_count >= 0:
                self.y -= 15
                self.jump_count -= 1

    def restart(self):
        self.x = self.original_x
        self.y= self.original_y

class Button:
    def __init__(self, screen, message, x, y, width, height, start_color, interact_color, font):
        self.screen = screen
        self.message = message
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start_color = start_color
        self.interact_color = interact_color
        self.font = font
        self.count = 0


    def draw(self):
        mouse = pygame.mouse.get_pos()
        word = self.font.render(self.message, True, (255, 255, 255))

        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(self.screen, self.interact_color, (self.x, self.y, self.width, self.height))
            self.screen.blit(word, ((self.x + self.width // 2) - word.get_width() // 2, (self.y + self.height // 2) - word.get_height() // 2))
        else:
            pygame.draw.rect(self.screen, self.start_color, (self.x, self.y, self.width, self.height))
            self.screen.blit(word, ((self.x + self.width // 2) - word.get_width() // 2, (self.y + self.height // 2) - word.get_height() // 2))

    def is_clicked(self):
        mouse = pygame.mouse.get_pos()
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y and pygame.mouse.get_pressed()[0] != 0:
            self.count += 1
        if self.count > 0:
            return True
        return False

class Time:
    def __init__(self,screen,font):
        self.screen = screen
        self.font = font
        self.time = 0

    def restart(self):
        self.time = 0

    def stop(self):
        return self.time

    def draw(self):
        self.time = self.time + (1 / 60)
        time_string = self.font.render(str(round(self.time,2)),True,(252,237,96))
        self.screen.blit(time_string,(10,0))




def main():
    #initialize level count
    level_count = 0

    #Create Goal
    goal = Goal(screen, 1200, 300-goal_image.get_height(), goal_image)

    #For character
    image = 'elephant_right_still.png'
    student = Student(screen, 20, 200, image, 3)

    #For timer
    timer = Time(screen, advance_text)

    #restart Button
    restart_button = Button(screen,'Restart',550, 400, 200, 60, (0,0,0), light_red, small_text)

    # level one blocks
    x_list_levelone = [50, 175, 233, 293, 425, 524, 584, 644, 808, 812, 872, 981, 1139, 1200]
    y_list_levelone = [385, 356, 288, 288, 263, 244, 244, 244, 180, 437, 437, 366, 384, 300]
    speedx_levelone = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  ##ADD
    speedy_levelone = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  ##ADD
    block_levelone = Block(screen, x_list_levelone, y_list_levelone, speedx_levelone, speedy_levelone, [124, 10, 2])
    block_levelone.load_bloc()  ##ADD
    block = block_levelone
    count = 0

    # Level two blocks
    x_list_leveltwo = [50, 139, 332, 492, 723, 991, 1200]
    y_list_leveltwo = [385, 440, 376, 288, 326, 388, 300]
    speedx_leveltwo = [0, 2, 3, 2, 3, 2, 0]  ##ADD
    speedy_leveltwo = [0, 0, 0, 0, 0, 0, 0]  ##ADD
    block_leveltwo = Block(screen, x_list_leveltwo, y_list_leveltwo, speedx_leveltwo, speedy_leveltwo, [255, 255, 255])
    block_leveltwo.load_bloc()

    # level three blocks
    x_list_levelthree = [50]
    y_list_levelthree = [385]
    speedx_levelthree = [0]  ##ADD
    speedy_levelthree = [0]  ##ADD
    for k in range(50):
        x_list_levelthree.append(206)
        y_list_levelthree.append(400 + 200 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(-1)
    for k in range(50):
        x_list_levelthree.append(356)
        y_list_levelthree.append(-200 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(2)
    for k in range(50):
        x_list_levelthree.append(510)
        y_list_levelthree.append(400 + 200 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(-2)
    for k in range(50):
        x_list_levelthree.append(642)
        y_list_levelthree.append(- 300 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(2)
    for k in range(50):
        x_list_levelthree.append(783)
        y_list_levelthree.append(400 + 300 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(-3)
    for k in range(50):
        x_list_levelthree.append(904)
        y_list_levelthree.append(-300 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(2)
    for k in range(50):
        x_list_levelthree.append(1027)
        y_list_levelthree.append(400 + 300 * k)
        speedx_levelthree.append(0)
        speedy_levelthree.append(-3)
    x_list_levelthree.append(1200)
    y_list_levelthree.append(300)
    speedx_levelthree.append(0)
    speedy_levelthree.append(0)

    block_levelthree = Block(screen, x_list_levelthree, y_list_levelthree, speedx_levelthree, speedy_levelthree,
                             [52, 204, 255])
    block_levelthree.load_bloc()

    # level 4 blocks
    x_list_levelfour = [50]
    y_list_levelfour = [385]
    speedx_levelfour = [0]  ##ADD
    speedy_levelfour = [0]  ##ADD
    for k in range(300):
        x_list_levelfour.append(50 - 100 * k)
        y_list_levelfour.append(500 + 40 * k)
        speedx_levelfour.append(4.8)
        speedy_levelfour.append(-1.7)
    x_list_levelfour.append(1200)
    y_list_levelfour.append(300)
    speedx_levelfour.append(0)
    speedy_levelfour.append(0)
    block_levelfour = Block(screen, x_list_levelfour, y_list_levelfour, speedx_levelfour, speedy_levelfour,
                            [207, 189, 151])
    block_levelfour.load_bloc()

    ## level 5 blocks
    x_list_levelfive = [50,110,170,230,290,350,410,470,530,590,650,710,770,830,890,950,1010,1070,1130,1190,1200]
    y_list_levelfive = [395, 395,395,395,395,395,395,395,395,395,395,395,395,395,395,395,395,395,395,395,395,395]
    speedx_levelfive = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0]  ##ADD
    speedy_levelfive = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0]  ##ADD
    block_levelfive = Block(screen, x_list_levelfive, y_list_levelfive, speedx_levelfive, speedy_levelfive, [98, 102, 106])
    block_levelfive.load_bloc()

    # For Gooses
    goose1 = Goose(screen, 300, 50, 'Goose_right_wings.png', 'Goose_right.png', 2)
    goose1_chase = False
    goose2 = Goose(screen, 300, 300, 'Goose_right_wings.png', 'Goose_right.png', 2)
    goose3 = Goose(screen, 900, 400, 'Goose_right_wings.png', 'Goose_right.png', 2)

    #Clock
    clock = pygame.time.Clock()


    def instructions():
        screen.fill(rose_red)
        description1 = "You are Rosie on a mission to make your way to commencement! "
        description2 = "Press the LEFT and RIGHT keys to move along"
        description3 = "Hop from platform to platform by pressing the Spacebar"
        description4 = ""
        description5 = "Do everything you can to avoid those pesky geese!"
        description7 = "You don't want to be late, so go go go as fast as you can!"
        desc_list = [description1, description2, description3, description4, description5, description7]
        for k in range(len(desc_list)):
            words = small_text.render(desc_list[k], True, (255, 255, 255))
            screen.blit(words, (10, 10 + 40 * k))

        goose_wings = pygame.image.load('Goose_right_wings.png')
        goose_wings = pygame.transform.scale(goose_wings, (200, 150))
        screen.blit(goose_wings, (900, 300))
        screen.blit(elephant_big, (900, 50))
        rosie_text = small_text.render('Rosie',True,(0,0,0))
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(955,164,rosie_text.get_width()+12,rosie_text.get_height()+8))
        screen.blit(rosie_text,(960,170))
        goose_text = small_text.render('Goose',True,(0,0,0))
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(955,427,goose_text.get_width()+12,goose_text.get_height()+8))
        screen.blit(goose_text,(960,427))
        pygame.display.update()


    while True:
        clock.tick(60)

        hitbox = pygame.Rect(student.x + 15, student.y + 20, student.image.get_width() - 25,
                             student.image.get_height() - 40)
        goalbox = pygame.Rect(goal.x, goal.y, goal.image.get_width(), goal.image.get_height())

        if level_count ==1:#first level
            screen.blit(lvl1backdrop, (0, 0))
            text_level1 = small_text.render('Make your way across Moench Hall!', True, (0,0,0))
            rect_l1 = pygame.Rect(screen.get_width()//2 - (text_level1.get_width()//2 + 5), 20, text_level1.get_width() + 10,text_level1.get_height() + 10 )
            pygame.draw.rect(screen,(255,255,255),rect_l1)
            screen.blit(text_level1,(screen.get_width()//2 - text_level1.get_width()//2, 25))
            block = block_levelone
            timer.draw()
            block.draw()
            student.gravity()
            student.draw()
            goal.draw()
            pygame.display.update()


        if level_count == 2: #second level
            screen.blit(lvl2backdrop, (0, 0))
            text_level2 = small_text.render('Hop across Speed Lake! Be careful of the geese!', True, (0, 0, 0))
            rect_l2 = pygame.Rect(screen.get_width() // 2 - (text_level2.get_width() // 2 + 5), 20,
                                  text_level2.get_width() + 10, text_level2.get_height() + 10)
            pygame.draw.rect(screen, (255, 255, 255), rect_l2)
            screen.blit(text_level2, (screen.get_width() // 2 - text_level2.get_width() // 2, 25))
            block = block_leveltwo
            block.draw()
            block.move_horizontal(1, 50, 330)
            block.move_horizontal(2, 330, 450)
            block.move_horizontal(3, 450, 700)
            block.move_horizontal(4, 700, 950)
            block.move_horizontal(5, 950, 1150)
            goose1.draw()
            goose2.draw()
            goose3.draw()

            goose2.move()
            goose3.move()

            if goose1.get_distance(student.x, student.y) < 250:
                goose1_chase = True
            if goose1_chase:
                goose1.chase(student.x, student.y)
            else:
                goose1.move()

            if abs(goose1.x - student.x) < 15 and abs(goose1.y - student.y) < 15:
                goose1.restart()
                student.restart()
                restart_sound.play()
                goose1_chase = False


            if abs(goose2.x - student.x) < 30 and abs(goose2.y - student.y) < 30:
                student.restart()
                restart_sound.play()

            if abs(goose3.x - student.x) < 30 and abs(goose3.y - student.y) < 30:
                student.restart()
                restart_sound.play()


            timer.draw()
            student.gravity()
            student.draw()
            goal.draw()



            pygame.display.update()



        if level_count == 3: #third level
            screen.blit(lvl3backdrop, (0, 0))

            text_level3 = small_text.render('The geese got angry! Make your way past the Union before they get you!', True, (0, 0, 0))
            rect_l3 = pygame.Rect(screen.get_width() // 2 - (text_level3.get_width() // 2 + 5), 20,
                                  text_level3.get_width() + 10, text_level3.get_height() + 10)
            pygame.draw.rect(screen, (255, 255, 255), rect_l3)
            screen.blit(text_level3, (screen.get_width() // 2 - text_level3.get_width() // 2, 25))
            block = block_levelthree
            timer.draw()
            block.draw()
            student.gravity()
            student.draw()
            goal.draw()
            pygame.display.update()
            for k in range(len(block.x_list)-2):
                block.move_vertical(k+1, 500000, -50000)

            goose1.draw()
            goose1.chase(student.x,student.y)

            if abs(goose1.x - student.x) < 15 and abs(goose1.y - student.y) < 15:
                goose1.restart()
                student.restart()
                restart_sound.play()


            goose2.draw()
            goose2.chase(student.x,student.y)
            if abs(goose2.x - student.x) < 15 and abs(goose2.y - student.y) < 15:
                goose2.restart()
                student.restart()
                restart_sound.play()


            goose3.draw()
            goose3.chase(student.x, student.y)
            if abs(goose3.x - student.x) < 15 and abs(goose3.y - student.y) < 15:
                goose3.restart()
                student.restart()
                restart_sound.play()


        if level_count == 4: #fourth level
            screen.blit(lvl4backdrop, (0, 0))

            text_level4 = small_text.render('Climb the SRC stairs to get to the Commencement Ceremony! Careful, they are slippery!',
                                            True, (0, 0, 0))
            rect_l4 = pygame.Rect(screen.get_width() // 2 - (text_level4.get_width() // 2 + 5), 20,
                                  text_level4.get_width() + 10, text_level4.get_height() + 10)
            pygame.draw.rect(screen, (255, 255, 255), rect_l4)
            screen.blit(text_level4, (screen.get_width() // 2 - text_level4.get_width() // 2, 25))

            block = block_levelfour
            timer.draw()
            block.draw()
            student.gravity()
            student.draw()
            goal.draw()
            pygame.display.update()
            for k in range(len(x_list_levelfour)-2):
                block.move_vertical(k+1, 500000, -50000)
                block.move_horizontal(k+1,-500000,500000)

        if level_count == 5: #fifth level
            screen.blit(lvl5backdrop, (0, 0))
            text_level5 = small_text.render('Walk across the stage and get your diploma off the podium!',
                                            True, (0, 0, 0))
            rect_l5 = pygame.Rect(screen.get_width() // 2 - (text_level5.get_width() // 2 + 5), 20,
                                  text_level5.get_width() + 10, text_level5.get_height() + 10)
            pygame.draw.rect(screen, (255, 255, 255), rect_l5)
            screen.blit(text_level5, (screen.get_width() // 2 - text_level5.get_width() // 2, 25))
            block = block_levelfive
            timer.draw()
            block.draw()
            student.gravity()
            student.draw()
            screen.blit(diploma, (screen.get_width()//2, 250))
            diploma_hitbox = pygame.Rect(screen.get_width()//2, 250, diploma.get_width(), diploma.get_height())
            if hitbox.colliderect(diploma_hitbox):
                start_btn.count = 6
                student.restart()
                final_time = timer.stop()

            pygame.display.update()

        if level_count == 6:
            screen.fill(rose_red)
            text_congrats = title_text.render('Congratulations!', True,(255,255,255))
            screen.blit(text_congrats,(screen.get_width()//2 - text_congrats.get_width()//2,100))
            text_score = small_text.render('You graduated with a time of',True,(255,255,255))
            screen.blit(text_score,(screen.get_width()//2 - text_score.get_width()//2 ,250))
            score_string = str(round(final_time,3)) + ' ' + 'seconds'
            score_numbers = advance_text.render(score_string,True,(0,0,0))
            screen.blit(score_numbers,(screen.get_width()//2-score_numbers.get_width()//2,285))

            restart_text = small_text.render('Click the button below to play again!',True,(255,255,255))
            screen.blit(restart_text,(screen.get_width()//2 - restart_text.get_width()//2,350))
            restart_button.draw()


            if restart_button.is_clicked():
                timer.restart()
                main()

            pygame.display.update()




        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                highlight_sound.play()


            if count == 0:
                def start_menu():
                    beginning_background = pygame.image.load("rose_entrance.jpg")
                    beginning_background = pygame.transform.scale(beginning_background,
                                                                  (screen.get_width(), screen.get_height()))
                    screen.blit(beginning_background, (0, 0))

                    title = title_text.render("Gotta Graduate!", True, (245, 215, 66))
                    title_shadow = title_text.render("Gotta Graduate!", True, (0, 0, 0))

                    screen.blit(title_shadow, (19, 82))
                    screen.blit(title, (20, 80))
                start_menu()

                instruction_btn = Button(screen, "INSTRUCTIONS", 150, 400, 200, 60, rose_red, light_red, small_text)
                instruction_btn.draw()
                start_btn = Button(screen, "START", 550, 400, 200, 60, rose_red, light_red, small_text)
                start_btn.draw()
                quit_btn = Button(screen, "QUIT", 950, 400, 200, 60, rose_red, light_red, small_text)
                quit_btn.draw()


            if instruction_btn.is_clicked() == True:
                count = count + 1
                instructions()
                back_btn = Button(screen, "BACK", 550, 400, 200, 60, (150, 158, 171), (240, 175, 24), small_text)
                back_btn.draw()
                if back_btn.is_clicked() == True: #restarts the main game loop to return to start
                    main()

            if start_btn.is_clicked() == True:
                count = count + 1 #prevents start menu from displaying
                if start_btn.count == 1:
                    level_count =1 #directs to level 1

                if start_btn.count == 2:
                    level_count =2 #directs to level 2

                if start_btn.count == 3:
                    level_count = 3 #directs to level 3

                if start_btn.count == 4:
                    level_count = 4 #directs to level 4

                if start_btn.count == 5:
                    level_count = 5 #directs to level 5

                if start_btn.count == 6:
                    level_count = 6


            if quit_btn.is_clicked() == True: #The 'X' on the window does the same thing, but I think a quit was fun
                sys.exit()

        #Key press events that occur continuously for our student object
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and student.x > 0:
            student.move_left()
        if pressed_keys[pygame.K_RIGHT] and student.x < screen.get_width()-student.image.get_width():
            student.move_right()
        if pressed_keys[pygame.K_SPACE]:
            jump_sound.play()
            student.jump()

        #Collisions for blocks
        for k in range(len(block.bloc)):
            if hitbox.colliderect(block.bloc[k]):
                student.is_fall = False
                student.can_jump = True
                student.jump_count = 8
                if abs(block.speedx[k]) > 0:          #keeps student moving with block
                    student.x = student.x + block.speedx[k]
                if abs(block.speedy[k]) >0:
                    student.y = student.y + block.speedy[k]
                break
            else:
                student.is_fall = True
                student.can_jump = False

        if hitbox.colliderect(goalbox):
            start_btn.count += 1
            student.restart()


        if student.y >= screen.get_height():
            student.restart()
            restart_sound.play()
        if student.y < 0:
            student.restart()
            restart_sound.play()
        if student.x > screen.get_width():
            student.restart()
            restart_sound.play()


        pygame.display.update()
main()