import pygame
import random
import time
import os

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('Snake Game')
pygame.mixer.music.load("snake_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
font=pygame.font.SysFont("Arial", 30)
font2=pygame.font.SysFont("Arial", 20)
font3=pygame.font.SysFont("Arial", 15)
clock=pygame.time.Clock()
screen_width=600
screen_height=400
screen=pygame.display.set_mode((screen_width, screen_height))
bg=pygame.image.load("snakeimage.jpg")
bg=pygame.transform.scale(bg, (screen_width, screen_height))
icon=pygame.image.load("snake_icon.png")
pygame.display.set_icon(icon)
food_img=pygame.image.load("snakefood.jpg")
food_img=pygame.transform.scale(food_img, (20, 20))
game_over_img=pygame.image.load("snake_game-over.jpg")
game_over_img=pygame.transform.scale(game_over_img, (200, 100))
high_score_file="high_score.txt"
if not os.path.exists(high_score_file):
    with open(high_score_file, "w") as f:
        f.write("0")
with open(high_score_file, "r") as f:
    high_score=int(f.read().strip())

class Snake:
    def __init__(self):
        self.size=1
        self.positions=[(screen_width//2, screen_height//2)]
        self.direction=random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.color=(0, 255, 0)
        self.score=0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        if (direction == 'UP' and self.direction != 'DOWN') or \
           (direction == 'DOWN' and self.direction != 'UP') or \
           (direction == 'LEFT' and self.direction != 'RIGHT') or \
           (direction == 'RIGHT' and self.direction != 'LEFT'):
            self.direction = direction

    def move(self):
        head_x, head_y = self.get_head_position()
        if self.direction == 'UP':
            new_head = (head_x, head_y - 10)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 10)
        elif self.direction == 'LEFT':
            new_head = (head_x - 10, head_y)
        elif self.direction == 'RIGHT':
            new_head = (head_x + 10, head_y)

        if new_head in self.positions or \
           new_head[0] < 0 or new_head[0] >= screen_width or \
           new_head[1] < 0 or new_head[1] >= screen_height:
            return False

        self.positions.insert(0, new_head)
        if len(self.positions) > self.size:
            self.positions.pop()
        return True

    def grow(self):
        self.size += 1
        self.score += 10

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.color, (*pos, 20, 20))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        surface.blit(high_score_text, (400, 10))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (screen_width - 20) // 20) * 20,
                         random.randint(0, (screen_height - 20) // 20) * 20)

    def draw(self, surface):
        surface.blit(food_img, self.position)

    def game_over_screen(surface, score):
        surface.blit(game_over_img, (200, 150))
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        score_text = font2.render(f"Your Score: {score}", True, (255, 255, 255))
        restart_text = font3.render("Press R to Restart or Q to Quit", True, ("black"))
        surface.blit(game_over_text, (250, 160))
        surface.blit(score_text, (250, 200))
        surface.blit(restart_text, (205, 235))
        pygame.display.flip()
        time.sleep(1)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        return
def main():
    global high_score
    snake = Snake()
    food = Food()
    running = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn('UP')
                elif event.key == pygame.K_DOWN:
                    snake.turn('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.turn('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.turn('RIGHT')

        if not snake.move():
            if snake.score > high_score:
                high_score = snake.score
                with open(high_score_file, "w") as f:
                    f.write(str(high_score))
            Food.game_over_screen(screen, snake.score)
            snake = Snake()
            food = Food()

        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()

        screen.blit(bg, (0, 0))
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

