from pygame import *
from time import time as timer
from random import *




WIDTH, HEIGHT = 750, 500
SQUARE_SIZE = 50
FPS = 60




w = display.set_mode((WIDTH, HEIGHT))
display.set_caption('змейка')




font.init()
game_font = font.Font(None, 50)
text = game_font.render('you lose!', True, (255, 0, 0))
small_font = font.Font(None, 30)




bg = transform.scale(image.load('background.jpg'), (WIDTH, HEIGHT))

def load_record():
    try:
        with open('record.txt', 'r') as file:
            return int(file.read())
    except:
        return 0

def save_record(value):
    with open('record.txt', 'w') as file:
        file.write(str(value))

record = load_record()
score = 0


class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect. y = pl_y
   
    def draw_sprite(self):
        w.blit(self.image, (self.rect.x, self.rect.y))




class Snake(GameSprite):
    def __init__(self, pl_image, pl_x, pl_y):
        super().__init__(pl_image, pl_x, pl_y)
        self.dx = SQUARE_SIZE
        self.dy = 0
   
    def update(self):




        for i in range(len(snake) - 1, 0, -1):
            snake[i].rect.x = snake[i - 1].rect.x
            snake[i].rect.y = snake[i - 1].rect.y


        self.rect.x += self.dx
        self.rect.y += self.dy




        if self.rect.x > 700:
            self.rect.x = 0
       
        if self.rect.x < 0:
            self.rect.x = 700
       
        if self.rect.y < 0:
            self.rect.y = 450
       
        if self.rect.y > 450:
            self.rect.y = 0
   
    def get_diction(self):
        keys = key.get_pressed()
        if keys [K_UP] and self.dy == 0:
            self.dx = 0
            self.dy = -SQUARE_SIZE
        if keys [K_DOWN] and self.dy == 0:
            self.dx = 0
            self.dy = SQUARE_SIZE
        if keys [K_LEFT] and self.dx == 0:
            self.dx = -SQUARE_SIZE
            self.dy = 0
        if keys [K_RIGHT] and self.dx == 0:
            self.dx = SQUARE_SIZE
            self.dy = 0




class Apple(GameSprite):
    def __init__(self, pl_image):
        super().__init__(pl_image, 0, 0)
        self.respawn()
   
    def respawn(self):
        self.rect.x = randrange(0, WIDTH - SQUARE_SIZE, SQUARE_SIZE)
        self.rect.y = randrange(0, HEIGHT - SQUARE_SIZE, SQUARE_SIZE)








head = Snake('head.png', 200, 250)
apple = Apple('apple.png')
bad_thing = Apple('dafuq.png')
burger = Apple('hamburger.png')
clock = time.Clock()
step_time = timer()
running = True
finish = False




snake = [head]




while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
   
    if not finish:
        cur_time = timer()
        head.get_diction()
        w.blit(bg, (0, 0))
       
       
        if cur_time - step_time >= 0.5:
            head.update()
           




            if head.rect.colliderect(apple.rect):
                apple.respawn()
                score += 1
                last_part = snake[-1]
       
                new_x, new_y = last_part.rect.x, last_part.rect.y




                if head.dx > 0:
                    new_x -= 50
                elif head.dx < 0:
                    new_x += 50
                elif head.dy > 0:
                    new_y -= 50
                elif head.dy < 0:
                    new_y += 50
           
                new_part = Snake('square.png', new_x, new_y)
                snake.append(new_part)
       
            step_time = timer()

            if head.rect.colliderect(bad_thing.rect):
                bad_thing.respawn()
                score -= 1
                last_part = snake[-1]
                snake.remove(last_part)
            

            if head.rect.colliderect(burger.rect):
                burger.respawn()
                score += 2
                last_part = snake[-1]

                new_x, new_y = last_part.rect.x, last_part.rect.y
                
                for i in range(2):
                    if head.dx > 0:
                        new_x -= 50
                    elif head.dx < 0:
                        new_x += 50
                    elif head.dy > 0:
                        new_y -= 50
                    elif head.dy < 0:
                        new_y += 50

                    new_part = Snake('square.png', new_x, new_y)
                    snake.append(new_part)  
        

        score_text = small_font.render(f'Очки: {score}', True, (255, 215, 0))
        record_text = small_font.render(f'Рекорд: {record}', True, (255, 215, 0))
        w.blit(score_text, (10, 20))
        w.blit(record_text, (10, 50))
        

        for part in snake[1:]:
            if head.rect.colliderect(part.rect):
                finish = True
                w.blit(text, (250, 200))
                if record < score:
                    record = score
                    save_record(record)
           
        for part in snake:
            part.draw_sprite()  
   
        head.draw_sprite()
        apple.draw_sprite()
        bad_thing.draw_sprite()
        burger.draw_sprite()
   
    display.update()
    clock.tick(FPS)

    




