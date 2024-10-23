from random import randrange as rnd
from itertools import cycle
from random import choice
from PIL import Image
import pygame
from ai import QLearningAgent

agent = QLearningAgent(state_size=1000000, action_size=3)  # Adjust state size as needed

pygame.init()
speed = 4



# extracting game items and characters from the resource.png image.
player_init = Image.open("resources.png").crop((77,5,163,96)).convert("RGBA")
player_init = player_init.resize(list(map(lambda x:x//2 , player_init.size)))
player_frame_1 = Image.open("resources.png").crop((1679,2,1765,95)).convert("RGBA")
player_frame_1 = player_frame_1.resize(list(map(lambda x:x//2 , player_frame_1.size)))
player_frame_2 = Image.open("resources.png").crop((1767,2,1853,95)).convert("RGBA")
player_frame_2 = player_frame_2.resize(list(map(lambda x:x//2 , player_frame_2.size)))
player_frame_3 = Image.open("resources.png").crop((1855,2,1941,95)).convert("RGBA")
player_frame_3 = player_frame_3.resize(list(map(lambda x:x//2 , player_frame_3.size)))
player_frame_31 = Image.open("resources.png").crop((1943,2,2029,95)).convert("RGBA")
player_frame_31 = player_frame_31.resize(list(map(lambda x:x//2 , player_frame_31.size)))
player_frame_4 = Image.open("resources.png").crop((2030,2,2117,95)).convert("RGBA")
player_frame_4 = player_frame_4.resize(list(map(lambda x:x//2 , player_frame_4.size)))
player_frame_5 = Image.open("resources.png").crop((2207,2,2323,95)).convert("RGBA")
player_frame_5 = player_frame_5.resize(list(map(lambda x:x//2 , player_frame_5.size)))
player_frame_6 = Image.open("resources.png").crop((2324,2,2441,95)).convert("RGBA")
player_frame_6 = player_frame_6.resize(list(map(lambda x:x//2 , player_frame_6.size)))
cloud = Image.open("resources.png").crop((166,2,257,29)).convert("RGBA")
cloud = cloud.resize(list(map(lambda x:x//2 , cloud.size)))
ground = Image.open("resources.png").crop((2,102,2401,127)).convert("RGBA")
ground = ground.resize(list(map(lambda x:x//2 , ground.size)))
obstacle1 = Image.open("resources.png").crop((446,2,479,71)).convert("RGBA")
obstacle1 = obstacle1.resize(list(map(lambda x:x//2 , obstacle1.size)))
obstacle2 = Image.open("resources.png").crop((446,2,547,71)).convert("RGBA")
obstacle2 = obstacle2.resize(list(map(lambda x:x//2 , obstacle2.size)))
obstacle3 = Image.open("resources.png").crop((446,2,581,71)).convert("RGBA")
obstacle3 = obstacle3.resize(list(map(lambda x:x//2 , obstacle3.size)))
obstacle4 = Image.open("resources.png").crop((653,2,701,101)).convert("RGBA")
obstacle4 = obstacle4.resize(list(map(lambda x:x//2 , obstacle4.size)))
obstacle5 = Image.open("resources.png").crop((653,2,701,101)).convert("RGBA")
obstacle5 = obstacle5.resize(list(map(lambda x:x//2 , obstacle5.size)))
obstacle6 = Image.open("resources.png").crop((851,2,950,101)).convert("RGBA")
obstacle6 = obstacle6.resize(list(map(lambda x:x//2 , obstacle6.size)))


cust_speed = 8
running = cycle([player_frame_3]*cust_speed+[player_frame_31]*cust_speed)
crouch = cycle([player_frame_5]*cust_speed+ [player_frame_6]*cust_speed)
crouch_scope = [player_frame_5]+[player_frame_6]
obstacles = [obstacle1,obstacle2, obstacle3,obstacle4,obstacle5,obstacle6]

gameDisplay = pygame.display.set_mode((600, 200))
pygame.display.set_caption('Dino Game')
clock = pygame.time.Clock()
start = False
crashed = True
Running = True
frameCounter = 0
maxScore = -1
score = 0
height = 110
obs1 = (rnd(600, 600 + 500), 130)
obs2 = (rnd(600 + 100 + 500, 1200 + 500), 130)
obs3 = (rnd(1700, 2000), 130)
nstate = 0
player = player_frame_1
state = running
jumping = False
iterations = 1
maxScoreIterations = 1
#run the game
while Running:
    state = agent.discretize_state(height, obs1[0], obs2[0], obs3[0])
    #below handles game resets
    score = int(frameCounter / 12)
    if crashed:
        if iterations - maxScoreIterations > 100:
            maxScore = maxScore/2
            print("PB Threshold Lowered")
        if iterations % 100 == 0:
            print(iterations)
        if score > maxScore and score != 0:
            print("New PB! " + str(score / 10) + "s after " + str(iterations) + " iterations")
            maxScore = score #max score = 21.3 rn
            maxScoreIterations = iterations
        iterations = iterations + 1
        reward = 0
        frameCounter = 0
        score = 0
        nstate = 0
        state = player_frame_1
        lock = False
        bg = (0, 150)
        bg1 = (600, 150)
        height = 110
        jumping = False
        slow_motion = False
        nstate = 0
        player = player_frame_1
        state = running
        c1 = (rnd(30, 600), rnd(0, 100))
        c2 = (rnd(50, 600), rnd(0, 100))
        c3 = (rnd(30, 700), rnd(0, 100))
        c4 = (rnd(30, 600), rnd(0, 100))
        obs1 = (rnd(600, 600 + 500), 130)
        obs2 = (rnd(600 + 100 + 500, 1200 + 500), 130)
        obs3 = (rnd(1700, 2000), 130)
        obast1 = choice(obstacles)
        if obast1 in [obstacle4, obstacle5, obstacle6]: obs1 = (obs1[0], 115)
        obast2 = choice(obstacles)
        if obast2 in [obstacle4, obstacle5, obstacle6]: obs2 = (obs2[0], 115)
        obast3 = choice(obstacles)
        if obast3 in [obstacle4, obstacle5, obstacle6]: obs3 = (obs3[0], 115)
        crashed = not crashed
        start = not start
    else:
        action = agent.choose_action(state)

        # Implement the action logic
        if action == 1 and height >= 110:
            jumping = True
            state = jumping
            player = player_frame_2
            nstate = 1
        elif action == 2:
            slow_motion = True
            state = crouch
            player = player_frame_5
            nstate = 2
        else:
            slow_motion = False
            state = running
            nstate = 0
            player = next(running)

        if isinstance(player, bool):
            print("Player is unexpectedly a boolean!")
            player = player_frame_1

            # Update game state
        next_state = agent.discretize_state(height, obs1[0], obs2[0], obs3[0])

        #object collision
        if (obs1_cub[0] <= player_stading_cub[2] - 10 <= obs1_cub[2] and obs1_cub[1] <= player_stading_cub[3] - 10 <=
            obs1_cub[3] - 5) or \
                (obs2_cub[0] <= player_stading_cub[2] - 10 <= obs2_cub[2] and obs2_cub[1] <= player_stading_cub[
                    3] - 10 <= obs2_cub[3] - 5) or \
                (obs3_cub[0] <= player_stading_cub[2] - 10 <= obs3_cub[2] and obs3_cub[1] <= player_stading_cub[
                    3] - 10 <= obs3_cub[3] - 5):
            reward = -1
            crashed = True
        else: #other things that don't involve object collision
            if height <= 100 and action == 1:
                reward = -.5
            elif action == 1:
                if obs1[0] - 100 < 200 or obs2[0] - 100 < 200 or obs3[0] - 100 < 200:
                    reward = 1
                else: reward = -.5
            elif running and not jumping:
                if action == 2:
                    reward = -.2
                else:
                    reward = .85
            else:
                reward = .85
        agent.update(nstate, action, reward, next_state)

    gameDisplay.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            start = False
            Running = False
            print("crashed")
        if event.type == pygame.KEYDOWN:
            if not crashed:
                start = True
            if event.key == pygame.K_DOWN:
                slow_motion = True
                state = crouch
            if event.key == pygame.K_UP:
                if height >= 110:
                    jumping = True
        if event.type == pygame.KEYUP:
            slow_motion = False
            if event.key == pygame.K_DOWN:
                state = running

    gameDisplay.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, 'RGBA'), c1)
    gameDisplay.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, 'RGBA'), c2)
    gameDisplay.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, 'RGBA'), c3)
    gameDisplay.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, 'RGBA'), c4)
    c1 = (c1[0] - 1, c1[1])
    c2 = (c2[0] - 1, c2[1])
    c3 = (c3[0] - 1, c3[1])
    c4 = (c4[0] - 1, c4[1])

    # Reset clouds when they go off-screen
    if c1[0] <= -50:
        c1 = (640, c1[1])
    if c2[0] <= -50:
        c2 = (700, c2[1])
    if c3[0] <= -50:
        c3 = (600, c3[1])
    if c4[0] <= -50:
        c4 = (800, c4[1])

    gameDisplay.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), bg)
    gameDisplay.blit(pygame.image.fromstring(ground.tobytes(), ground.size, 'RGBA'), bg1)

    # Jumping and height management
    if jumping:
        if height >= 110 - 100:
            height -= 4
        if height <= 110 - 100:
            jumping = False
    if height < 110 and not jumping:
        if slow_motion:
            height += 1.5
        else:
            height += 3

    player = gameDisplay.blit(pygame.image.fromstring(player.tobytes(), player.size, 'RGBA'), (5, height))
    gameDisplay.blit(pygame.image.fromstring(obast1.tobytes(), obast1.size, 'RGBA'), obs1)
    gameDisplay.blit(pygame.image.fromstring(obast2.tobytes(), obast2.size, 'RGBA'), obs2)
    gameDisplay.blit(pygame.image.fromstring(obast3.tobytes(), obast3.size, 'RGBA'), obs3)

    # Handle obstacles going off-screen
    if obs1[0] <= -50:
        obs1 = (rnd(600, 600 + 500), 130)
        obast1 = choice(obstacles)
        if obast1 in [obstacle4, obstacle5, obstacle6]:
            obs1 = (obs1[0], 115)
    if obs2[0] <= -50:
        obs2 = (rnd(600 + 100 + 500, 1200 + 500), 130)
        obast2 = choice(obstacles)
        if obast2 in [obstacle4, obstacle5, obstacle6]:
            obs2 = (obs2[0], 115)
    if obs3[0] <= -50:
        obs3 = (rnd(1700, 2000), 130)
        obast3 = choice(obstacles)
        if obast3 in [obstacle4, obstacle5, obstacle6]:
            obs3 = (obs3[0], 115)

    player_stading_cub = (5, height, 5 + 43, height + 46)
    #print(player_stading_cub)
    if height < 100:
        if not crashed:
            start = True

    if start:
        obs1 = (obs1[0] - speed, obs1[1])
        obs2 = (obs2[0] - speed, obs2[1])
        obs3 = (obs3[0] - speed, obs3[1])
        obs1_cub = (obs1[0], obs1[1], obs1[0] + obast1.size[0], obs1[1] + obast1.size[1])
        obs2_cub = (obs2[0], obs2[1], obs2[0] + obast2.size[0], obs2[1] + obast2.size[1])
        obs3_cub = (obs3[0], obs3[1], obs3[0] + obast3.size[0], obs3[1] + obast3.size[1])

        if not lock:
            bg = (bg[0] - speed, bg[1])
            if bg[0] <= -600:
                lock = 1
        if -bg[0] >= 600 and lock:
            bg1 = (bg1[0] - speed, bg1[1])
            bg = (bg[0] - speed, bg[1])
            if -bg1[0] >= 600:
                bg = (600, 150)
        if -bg1[0] >= 600 and lock:
            bg = (bg[0] - speed, bg1[1])
            bg1 = (bg1[0] - speed, bg1[1])

            # Check for collisions
        if (obs1_cub[0] <= player_stading_cub[2] - 10 <= obs1_cub[2] and obs1_cub[1] <= player_stading_cub[3] - 10 <=
            obs1_cub[3] - 5) or \
                (obs2_cub[0] <= player_stading_cub[2] - 10 <= obs2_cub[2] and obs2_cub[1] <= player_stading_cub[
                    3] - 10 <= obs2_cub[3] - 5) or \
                (obs3_cub[0] <= player_stading_cub[2] - 10 <= obs3_cub[2] and obs3_cub[1] <= player_stading_cub[
                    3] - 10 <= obs3_cub[3] - 5):
            start = False
            crashed = True
            state = player_frame_4

        pygame.display.update()
        #clock.tick(1) for testing purposes
        clock.tick(120)
        frameCounter += 1
