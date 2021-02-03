import os
import sys
import pygame
import random

pygame.init()

FPS = 50
speed = 4
WIDTH = 390
HEIGHT = 430
font_style = pygame.font.SysFont(None, 25)

pygame.display.set_caption("Змейка")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def game(row, line, size):
    running = True
     
    if size == 30:
        x, y = 180, 180
    else:
        x, y = 140, 140
    x1, y1 = 0, 0
    
    s = ["еда/eda.png", "еда/eda1.png", "еда/eda2.png"]
    
    count = 0 
    lenn = 1
    snake = []
    last = ""
        
    foodx = round(random.choice(range(30, 330, size)))
    foody = round(random.choice(range(30, 330, size)))
    s1 = random.choice(s)  
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if last != "l" or int(lenn) == 1:
                        x1 = size
                        y1 = 0
                        last = "r"
                elif event.key == pygame.K_LEFT:
                    if last != "r" or int(lenn) == 1:
                        x1 = -size
                        y1 = 0
                        last = "l"
                elif event.key == pygame.K_DOWN:
                    if last != "u" or int(lenn) == 1:
                        x1 = 0
                        y1 = size
                        last = "d"
                elif event.key == pygame.K_UP:
                    if last != "d" or int(lenn) == 1:
                        x1 = 0
                        y1 = -size
                        last = "u"  
        x += x1
        y += y1
        
        if x == 360 or x < 30 or y == 360 or y < 30:
            running = False
            Stop()              
        
        screen.fill((25, 48, 71))  
        
        back = pygame.Surface((390, 430))
        back.fill((72, 82, 105))
        screen.blit(back, (1, 1))
        
        v = 0
        z = 360
        for i in range(0, 390, 30):
            fon = pygame.transform.scale(load_image('стены/стена.png'),
                                         (30, 30))
            back.blit(fon, (v, z)) 
            v += 30
        v = 0
        z = 0
        for j in range(0, 390, 30):
            wall = pygame.transform.scale(load_image('стены/стена1.png'),
                                          (30, 30))
            back.blit(wall, (v, z)) 
            z += 30     
        v = 360
        z = 0
        for j in range(0, 390, 30):
            wall = pygame.transform.scale(load_image('стены/стена2.png'),
                                          (30, 30))
            back.blit(wall, (v, z)) 
            z += 30
        v = 0
        z = 0
        for j in range(0, 390, 30):
            wall = pygame.transform.scale(load_image('стены/стена3.png'),
                                          (30, 30))
            back.blit(wall, (v, z)) 
            v += 30    
        screen.blit(back, (0, 0))
        
        v = 0
        z = 390
        for j in range(0, 390, 30):
            wall = pygame.transform.scale(load_image('стены/стена4.png'),
                                          (30, 50))
            back.blit(wall, (v, z)) 
            v += 30  
        screen.blit(back, (0, 0)) 

        background = pygame.transform.scale(load_image('фоны/gr.png'), 
                                            (140, 30))
        screen.blit(background, (220, 370))         
        
        background = pygame.transform.scale(load_image('фоны/gr.png'), 
                                            (120, 30))
        screen.blit(background, (30, 370))  
            
        board = Board(row, line, size)
        
        if size == 30:
            food = pygame.transform.scale(load_image(s1), (35, 41))
        else:
            food = pygame.transform.scale(load_image(s1), (55, 59))        
        
        if size == 30:
            screen.blit(food, (foodx - 5, foody - 6)) 
        if size > 30:
            screen.blit(food, (foodx - 1, foody))             
        if row == 11:
            board.render11(screen)
        if row == 6:    
            board.render6(screen)
        pygame.draw.rect(screen, pygame.Color("Black"), [30, 30, 330, 330], 3)
        
        head = []
        head.append(x)
        head.append(y)
        snake.append(head)
        if len(snake) > lenn:
            snake.remove(snake[0]) 
            
        for elem in snake[:-1]:
            if elem == head:
                Stop()                   
        
        body(size, snake, last)
        Countt(count, size, (lenn - 1))
        
        if size == 30:
            if len(snake) == 121:
                Win()
        else:
            if len(snake) == 36:
                Win()
        
        pygame.display.update()
        
        if x == foodx and y == foody:
            dd = []
            count += 1
            lenn += 1
            foodx = random.choice(range(30, 330, size))
            foody = random.choice(range(30, 330, size))
            s1 = random.choice(s) 
            dd.append(foodx)
            dd.append(foody)
            if dd in snake:
                while dd in snake:
                    foodx = random.choice(range(30, 330, size))
                    foody = random.choice(range(30, 330, size))   
                    s1 = random.choice(s) 
                    dd.append(foodx)
                    dd.append(foody)                          
            
        clock.tick(speed)
        
    pygame.display.update()    
    

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()
    
    
class Board:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.size = size
    
    def render11(self, screen):
        self.left = 30
        self.top = 30        
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (40, 63, 86),
                                 (j * self.size + self.left,
                                  i * self.size + self.top, self.size,
                                  self.size), 1)
                
    def render6(self, screen):
        self.left = 30
        self.top = 30        
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (40, 63, 86),
                                 (j * self.size + self.left,
                                  i * self.size + self.top, self.size,
                                  self.size), 1)    
                
                
class Stop:
    
    def __init__(self):
        self.stop()
        
    def stop(self):
        background = pygame.transform.scale(load_image('фоны/gr.png'),
                                            (330, 330))
        screen.blit(background, (30, 30))     
        text = pygame.transform.scale(load_image('надписи/por.png'),
                                      (360, 200))
        screen.blit(text, (10, 1))         
    
        button = pygame.Surface((150, 50))
        button.fill((55, 78, 101))    
        screen.blit(button, (120, 180)) 
    
        button1 = pygame.Surface((150, 50))
        button1.fill((40, 63, 86))    
        screen.blit(button1, (120, 250))    
    
        text = pygame.transform.scale(load_image('надписи/eexit.png'),
                                      (350, 100))
        screen.blit(text, (20, 210)) 
    
        text = pygame.transform.scale(load_image('надписи/new.png'), (350, 100))
        screen.blit(text, (20, 140))         

        pygame.display.update() 
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in (range(120, 270)) and y in (range(180, 230)):
                        return Choice()
                    if x in (range(120, 270)) and y in (range(250, 300)):
                        return terminate()                
              
                pygame.display.flip()
                clock.tick(FPS)      
    
    
def body(pos, snake, last):
    for elem1 in snake:
        if elem1 == snake[-1]:
            if last == "d":   
                part = pygame.transform.scale(load_image('тело/down.png'),
                                              (pos, pos))
                screen.blit(part, (elem1[0], elem1[1])) 
            elif last == "r":   
                part = pygame.transform.scale(load_image('тело/right.png'),
                                              (pos, pos))
                screen.blit(part, (elem1[0], elem1[1]))  
            elif last == "l":   
                part = pygame.transform.scale(load_image('тело/left.png'),
                                              (pos, pos))
                screen.blit(part, (elem1[0], elem1[1]))                
            else:    
                part = pygame.transform.scale(load_image('тело/up.png'),
                                              (pos, pos))
                screen.blit(part, (elem1[0], elem1[1]))                 
        else:    
            part = pygame.transform.scale(load_image('тело/bodyyy.png'),
                                          (pos, pos))
            screen.blit(part, (elem1[0], elem1[1]))
            
            
class Countt:
    
    def __init__(self, count, size, lenn):
        self.count = count
        self.size = size
        self.lenn = lenn
        self.score(lenn)
        self.best(count, size)
        
    def score(self, lenn):
        value = font_style.render(f"счёт: {lenn}", True, (245, 245, 245))
        screen.blit(value, [35, 370])
    
    def best(self, count, size):
        if size == 30:
            a = open("data/рекорд/record.txt", "r+")
            text = "".join(a)    
            if count > int(text):
                with open('data/рекорд/record.txt', 'w') as a:
                    a.write(str(count))   
            value1 = font_style.render(f"лучший счёт: {text}", True,
                                       (245, 245, 245))
            screen.blit(value1, [225, 370])    
            a.close()
        else:    
            a = open("data/рекорд/record1.txt", "r+")
            text = "".join(a)    
            if count > int(text):
                with open('data/рекорд/record1.txt', 'w') as a:
                    a.write(str(count))   
            value1 = font_style.render(f"лучший счёт: {text}", True,
                                       (245, 245, 245))
            screen.blit(value1, [225, 370])    
            a.close()
    
    
class Homescreen:  
    def __init__(self):
        self.home()
        
    def home(self):
        back = pygame.transform.scale(load_image('фоны/ав.jpg'),
                                      (WIDTH, HEIGHT))
        screen.blit(back, (0, 0))
    
        text = pygame.transform.scale(load_image('надписи/text.png'),
                                      (350, 140))
        screen.blit(text, (20, 10))
     
        button1 = pygame.Surface((150, 50))
        button1.fill((55, 78, 101))    
        screen.blit(button1, (120, 140))
     
        text = pygame.transform.scale(load_image('надписи/play.png'),
                                      (350, 105))
        screen.blit(text, (20, 110))     
    
        button2 = pygame.Surface((150, 50))
        button2.fill((40, 63, 86))    
        screen.blit(button2, (120, 215))  
    
        text1 = pygame.transform.scale(load_image('надписи/rules.png'),
                                       (350, 105))
        screen.blit(text1, (20, 185))         
    
        button3 = pygame.Surface((150, 50))
        button3.fill((25, 48, 71))
        screen.blit(button3, (120, 290))  
    
        text2 = pygame.transform.scale(load_image('надписи/exit.png'),
                                       (350, 105))
        screen.blit(text2, (20, 260))     
       
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in (range(120, 270)) and y in (range(140, 190)):
                        return Choice()     
                    elif x in (range(120, 270)) and y in (range(215, 265)):
                        return Rules()
                    elif x in (range(120, 270)) and y in (range(290, 340)):
                        terminate()               
                pygame.display.flip()
                clock.tick(FPS)   
                
                
class Rules: 
    
    def __init__(self):
        self.rules() 
        
    def rules(self):
        intro_text = ["Управление: клавиши", "стрелок на клавиатуре", "",
                      "Цель: собрать наибольшее", "количество еды" "", "",
                      "Нельзя врезаться в стенки", "экрана и хвост змейки"]
        text_coord = 30
        font = pygame.font.Font(None, 35)
    
        back = pygame.transform.scale(load_image('фоны/ав.jpg'),
                                      (WIDTH, HEIGHT))
        screen.blit(back, (0, 0)) 
    
        back = pygame.transform.scale(load_image('фоны/gr.png'), (360, 280))
        screen.blit(back, (20, 20))        
    
        button4 = pygame.Surface((150, 50))
        button4.fill((55, 78, 101))    
        screen.blit(button4, (240, 370)) 
    
        text = pygame.transform.scale(load_image('надписи/back.png'),
                                      (350, 105))
        screen.blit(text, (140, 340))    
    
        for line in intro_text:
            string_rendered = font.render(line, 1, (245, 245, 245))
            intro_rect = string_rendered.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in (range(240, 390)) and y in (range(370, 420)):
                        return Homescreen()                 
              
                pygame.display.flip()
                clock.tick(FPS)    
                
                
class Choice:
    
    def __init__(self):
        self.choice()
        
    def choice(self): 
        back = pygame.transform.scale(load_image('фоны/ав.jpg'),
                                      (WIDTH, HEIGHT))
        screen.blit(back, (0, 0)) 
    
        back = pygame.transform.scale(load_image('фоны/gr.png'), (360, 280))
        screen.blit(back, (20, 20))        
    
        button = pygame.Surface((150, 50))
        button.fill((25, 48, 71))    
        screen.blit(button, (240, 370))
    
        text = pygame.transform.scale(load_image('надписи/back.png'),
                                      (350, 105))
        screen.blit(text, (140, 340))        
    
        button1 = pygame.transform.scale(load_image('надписи/11.png'),
                                         (500, 160))
        screen.blit(button1, (30, 20))
    
        button2 = pygame.transform.scale(load_image('надписи/6.png'),
                                         (500, 160))
        screen.blit(button2, (200, 20))    
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in (range(240, 390)) and y in (range(370, 420)):
                        return Homescreen()
                    elif x in (range(50, 180)) and y in (range(65, 120)):
                        return game(11, 11, 30)
                    elif x in (range(227, 344)) and y in (range(65, 120)):
                        return game(6, 6, 55)
              
                pygame.display.flip()
                clock.tick(FPS)   
      
            
class Win:
    
    def __init__(self):
        self.win()

    def win(self):
        back = pygame.transform.scale(load_image('фоны/gr.png'), (330, 330))
        screen.blit(back, (30, 30))     
        text = pygame.transform.scale(load_image('надписи/win.png'), (360, 200))
        screen.blit(text, (10, 1))         
    
        button = pygame.Surface((150, 50))
        button.fill((55, 78, 101))    
        screen.blit(button, (120, 180)) 
    
        button1 = pygame.Surface((150, 50))
        button1.fill((40, 63, 86))    
        screen.blit(button1, (120, 250))    
    
        text = pygame.transform.scale(load_image('надписи/eexit.png'),
                                      (350, 100))
        screen.blit(text, (20, 140)) 
    
        text = pygame.transform.scale(load_image('надписи/new.png'), (350, 100))
        screen.blit(text, (20, 210))         
    
        pygame.display.update()
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in (range(120, 270)) and y in (range(180, 230)):
                        return terminate()
                    if x in (range(120, 270)) and y in (range(50, 300)):
                        return Choice()                
              
                pygame.display.flip()
                clock.tick(FPS) 
    
    
Homescreen()     
terminate() 