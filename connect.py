import pygame
import random
import math

pygame.init()

space = 1

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("connect")

black = (0, 0, 0)
screen.fill(black)
button_img = pygame.image.load(r"restart.png")


# player1
player1img = pygame.image.load(r"red.png")
player1x = 130
player1y = 200
player1x_change = 0
player1y_change = 0

# player2
player2img = pygame.image.load(r"blue.png")
player2x = 600
player2y = 200
player2x_change = 0
player2y_change = 0

obstacleimg = []
obstaclex = []
obstacley = []
obstacley_change = []
num_of_obstacle = 2

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10

game_over_font = pygame.font.Font("freesansbold.ttf", 64)

# obstacle
for i in range(num_of_obstacle):
    obstacleimg.append(pygame.image.load("ob.png"))
    obstaclex.append(random.randint(50, 750))
    obstacley.append(800)
    obstacley_change.append(-00.8)


def reset_game():
    obstacleimg[:] = []
    obstaclex[:] = []
    obstacley[:] = []
    obstacley_change[:] = []
    for i in range(num_of_obstacle):
        obstacleimg.append(pygame.image.load("ob.png"))
        obstaclex.append(random.randint(50, 750))
        obstacley.append(800)
        obstacley_change.append(-00.8)
    return obstacleimg, obstaclex, obstacley, obstacley_change


def player1(x, y):
    screen.blit(player1img, (x, y))


def player2(x, y):
    screen.blit(player2img, (x, y))


def edgecollider(x1, y1, x2, y2):
    pygame.draw.line(screen, (244, 244, 244, 244), (x1 + 20, y1), (x2 + 24, y2), 5)
    pygame.display.flip()


def obstacle(x, y, i):
    screen.blit(obstacleimg[i], (x, y))


def iscollition(player1x, player1y, player2x, player2y, obstaclex, obstacley):
    # disctance between player1 & obstacle
    distance_1o = math.sqrt(
        (math.pow(player1x - obstaclex, 2)) + (math.pow(player1y - obstacley, 2))
    )
    distance_2o = math.sqrt(
        (math.pow(player2x - obstaclex, 2)) + (math.pow(player2y - obstacley, 2))
    )
    if player2x - player1x - 64 != 0:
        y_e = (player1y + 32) + (
            ((player2y + 32 - player1y - 32) / (player2x - player1x - 64))
            * (obstaclex - player1x - 64)
        )
        distance_eo = math.sqrt((math.pow(y_e - obstacley, 2)))
        if (
            distance_1o < 59
            or distance_2o < 59
            or (
                distance_eo < 5
                and (
                    (player1x < obstaclex and player2x > obstaclex)
                    or (player1x > obstaclex and player2x < obstaclex)
                )
            )
        ):
            return True
        else:
            return False


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


button = Button(350, 300, button_img)
game_over = False
# game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space = space + 1

        if event.type == pygame.KEYDOWN:
            if space % 2 == 0:
                if event.key == pygame.K_LEFT:
                    player1x_change = -1.5
                if event.key == pygame.K_RIGHT:
                    player1x_change = 1.5
                if event.key == pygame.K_DOWN:
                    player1y_change = 1.5
                if event.key == pygame.K_UP:
                    player1y_change = -1.5

            elif space % 2 != 0:
                if event.key == pygame.K_LEFT:
                    player2x_change = -1.5
                if event.key == pygame.K_RIGHT:
                    player2x_change = 1.5
                if event.key == pygame.K_DOWN:
                    player2y_change = 1.5
                if event.key == pygame.K_UP:
                    player2y_change = -1.5

        if event.type == pygame.KEYUP:
            if (
                event.key == pygame.K_LEFT
                or event.key == pygame.K_RIGHT
                or event.key == pygame.K_DOWN
                or event.key == pygame.K_UP
            ):
                player1x_change = 0
                player1y_change = 0
                player2x_change = 0
                player2y_change = 0

    player1x = player1x + player1x_change
    player1y = player1y + player1y_change

    player2x = player2x + player2x_change
    player2y = player2y + player2y_change

    for i in range(num_of_obstacle):
        obstacley[i] += obstacley_change[i]
        # collision
        collision = iscollition(
            player1x, player1y, player2x, player2y, obstaclex[i], obstacley[i]
        )
        if collision:
            for j in range(num_of_obstacle):
                obstacley[j] = 10000
            player1y = 200
            player1x = 130
            player2x = 600
            player2y = 200
            game_over = True
        if game_over == True:
            if button.draw() == True:
                game_over = False
                obstacleimg, obstaclex, obstacley, obstacley_change = reset_game()

        obstacle(obstaclex[i], obstacley[i], i)
        if obstacley[i] < -128:
            obstacley[i] = 800
            obstaclex[i] = random.randint(50, 750)
            score_value = score_value + 2

    if player1x < 0:
        player1x = 0
    elif player1x >= 736:
        player1x = 736
    if player1y < 0:
        player1y = 0
    elif player1y >= 736:
        player1y = 736

    if player2x < 0:
        player2x = 0
    elif player2x >= 736:
        player2x = 736
    if player2y < 0:
        player2y = 0
    elif player2y >= 736:
        player2y = 736

    player1(player1x, player1y)
    player2(player2x, player2y)
    show_score(textx, texty)
    edgecollider(player1x + 64, player1y + 32, player2x, player2y + 32)

    pygame.display.update()
