import pygame
import time
import random
from fastapi import FastAPI


def snakeGame():
    # Initialize Pygame
    pygame.init()

    # Define colors
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    # Set display dimensions
    dis_width = 800
    dis_height = 600

    # Set snake block size and speed
    dis_block = 10
    snake_speed = 30
    player_speed = 15

    level=1
    score = 0

    # Create the display
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption("Score: " + str(score)+"   Level: "+str(level))
    clock = pygame.time.Clock()

    font_style = pygame.font.SysFont(None, 50)


    def our_snake(dis_block, snake_list):
        for snake in snake_list:
            for x in snake:
                for i in range((snake_speed//dis_block)):
                    pygame.draw.rect(dis, red, [x[0]+dis_block*i, x[1], dis_block, dis_block])


    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])


    def gameLoop(level,score):
        pygame.display.set_caption("Score: " + str(score)+"   Level: "+str(level))
        num_of_snake = level
        game_over = False
        game_close = False

        # Initialize player
        x1 = dis_width / 2
        y1 = dis_height / 2
        x1_change = 0
        y1_change = 0

        # Initialize snakes at random positions within the game window
        x2=[]
        y2=[]
        for i in range(num_of_snake):
            a=round(random.randrange(0, dis_width - dis_block) / 10.0) * 10.0
            while(a==(dis_width/2)): a=round(random.randrange(0, dis_width - dis_block) / 10.0) * 10.0
            x2.append(a)
            y2.append(round(random.randrange(0, dis_height - dis_block) / 10.0) * 10.0)
            
        x2_change = [snake_speed]*num_of_snake
        y2_change = [0]*num_of_snake
        snake_list = []
        for i in range(num_of_snake):
            snake_list.append([])
        length_of_snakes = []
        for i in range(num_of_snake):
            length_of_snakes.append(round(random.randrange(0,10)))

        foodx = round(random.randrange(0, dis_width - dis_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - dis_block) / 10.0) * 10.0


        # Define a function to check for collision
        def check_collision(x1, y1, x2, y2, player_width, player_height):
            if (x1 < x2 + player_width and
                x1 + player_width > x2 and
                y1 < y2 + player_height and
                y1 + player_height > y2):
                return True
            return False


        while not game_over:

            while game_close:
                dis.fill(blue)
                message("You Lost! Press Q-Quit or C-Play Again", red)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop(1,0)

            # setNewLevel(level)
            # Player controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -dis_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = dis_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -dis_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = dis_block
                        x1_change = 0

            # Check boundaries for player
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            # Update player position
            x1 += x1_change
            y1 += y1_change

            # Check boundaries for snake
            for i in range(num_of_snake):
                if x2[i] >= dis_width or x2[i] < 0 or y2[i] >= dis_height or y2[i] < 0:
                    x2[i]=(x2[i]+dis_width)%dis_width
                    y2[i]=(y2[i]+dis_height)%dis_height
                # Update snake position
                x2[i] += x2_change[i]
                y2[i] += y2_change[i]
                


            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, dis_block, dis_block])

            # check player touch snake
            for snake in snake_list:
                for x in snake:
                    for i in range((snake_speed//dis_block)):
                        if check_collision(x1,y1,x[0]+dis_block*i,x[1],dis_block,dis_block):
                            game_close = True
                            break

            # Draw and update player 1 snake
            # snake_head1 = []
            # snake_head1.append(x1)
            # snake_head1.append(y1)
            # snake_list1.append(snake_head1)
            # if len(snake_list1) > length_of_snake1:
            #     del snake_list1[0]

            pygame.draw.rect(dis, black, [x1, y1, dis_block, dis_block])
            # our_snake(dis_block, snake_list1)

            # Draw and update snake
            for i in range(num_of_snake):
                snake_head = []
                snake_head.append(x2[i])
                snake_head.append(y2[i])
                snake_list[i].append(snake_head)
                if len(snake_list[i]) > length_of_snakes[i]:
                    del snake_list[i][0]
                our_snake(dis_block, snake_list)

            # Check if player 1 eats the food
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - dis_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - dis_block) / 10.0) * 10.0
                score += 10
                level += 1
                gameLoop(level,score)

            # Display scores
            # score_text = font_style.render("Score: " + str(score)+"   Level: "+str(level),True, white)
            # dis.blit(score_text, [10, 10])

            pygame.display.update()

            clock.tick(player_speed)

        pygame.quit()
        quit()


    gameLoop(level,score)



app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Snake Game"}

from fastapi import BackgroundTasks

@app.post("/game")
async def run_game(background_tasks: BackgroundTasks):
    background_tasks.add_task(snakeGame)
    return {"message": "Game Running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)