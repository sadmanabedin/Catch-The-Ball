import pygame
import sys 
from random import randint


pygame.init()
mainClock = pygame.time.Clock()
width = 800
height = 600

font = pygame.font.SysFont('arial', 50)

score = 0
total = 0

fail_cnt = 2
lives = 10
screen_top = 70

pygame.mixer.init()

def play_music(filename):
  pygame.mixer.music.load(filename)
  pygame.mixer.music.set_volume(0.2)
  pygame.mixer.music.play()

paddle = {
  "x": 400,
  "y": 550,
  "width": 100,
  "height": 20,
  "speed": 10
}

ball = {
  "x": randint(0,width),
  "y": screen_top,
  "ySpeed": 2,
  "xSpeed": randint(-2,2),
  "radius": 15,
}
# create a bonus ball
bonusBall = {
  "x": randint(0,width),
  "y": screen_top,
  "ySpeed": 2,
  "xSpeed": randint(-2,2),
  "radius": 15,
}
 
screen = pygame.display.set_mode((width, height))
 
print("The game has started")

paddle_drop = 1

#setting font settings
font = pygame.font.SysFont(None, 30)
 
"""
A function that can be used to write text on our screen and buttons
"""
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
# A variable to check for the status later
click = False
 

# Main container function that holds the buttons and game functions
def main_menu():
    while True:
 
        screen.fill((0,190,255))
        draw_text('Main Menu', font, (0,0,0), screen, 350, 40)
 
        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(300, 200, 200, 50)
        # button_2 = pygame.Rect(200, 180, 200, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game_loop()
        # if button_2.collidepoint((mx, my)):
        #     if click:
        #         options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        # pygame.draw.rect(screen, (255, 0, 0), button_2)
 
        #writing text on top of button
        draw_text('PLAY', font, (255,255,255), screen, 370, 215)
        # draw_text('OPTIONS', font, (255,255,255), screen, 250, 195)


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)

#this is so the game runs forever
def game_loop():
  global paddle_drop
  global score
  global total
  global fail_cnt
  global lives
  global screen_top

  while True:
    pygame.time.delay(10)
    screen.fill((255,255,255))

    # color red upto 10 units height from top
    pygame.draw.rect(screen, (255,0,0), (0,0, width, screen_top))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        break
  
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      paddle["x"] = paddle["x"] - paddle["speed"]
      # ensure paddle doesn't go off the screen
      if paddle["x"] < 0:
        paddle["x"] = 0
    if keys[pygame.K_RIGHT]:
      paddle["x"] = paddle["x"] + paddle["speed"]
      # ensure paddle doesn't go off the screen
      if paddle["x"] > width - paddle["width"]:
        paddle["x"] = width - paddle["width"]


    #draw paddle
    pygame.draw.rect(screen, (0,255,0), (paddle["x"],paddle["y"] , paddle["width"], paddle["height"]))

    #ball movement
    ball["y"] = ball["y"] + ball["ySpeed"]
    ball["x"] = ball["x"] + ball["xSpeed"]
    #bonus ball movement
    bonusBall["y"] = bonusBall["y"] + bonusBall["ySpeed"]
    bonusBall["x"] = bonusBall["x"] + bonusBall["xSpeed"]

    #if ball hits a wall
    if ball["x"] < 0 or ball["x"] > width:
      ball["xSpeed"] = -ball["xSpeed"]

    #if bonus ball hits a wall
    if bonusBall["x"] < 0 or bonusBall["x"] > width:
      bonusBall["xSpeed"] = -bonusBall["xSpeed"]

    #draw ball
    pygame.draw.circle(screen, (0,0,255), (ball["x"], ball["y"]), ball["radius"])

    if paddle_drop % 5 == 0:
      pygame.draw.circle(screen, (255,0,255), (bonusBall["x"], bonusBall["y"]), bonusBall["radius"])
    
    #check if the ball hit the paddle
    if ball["y"] + ball["radius"] >= paddle["y"] and ball["y"]+ ball["radius"] <= paddle["y"] + 5:
      if ball["x"] > paddle["x"] and ball["x"] < paddle["x"] + paddle["width"]:
        #print("Ball has hit paddle")
        ball["ySpeed"] = -ball["ySpeed"]
        score += 1
        paddle_drop += 1
        # play sound
        play_music('bounce.mp3')
        
    
    #check if the bonus ball hit the paddle
    if bonusBall["y"] + bonusBall["radius"] >= paddle["y"] and bonusBall["y"]+ bonusBall["radius"] <= paddle["y"] + 5:
      if bonusBall["x"] > paddle["x"] and bonusBall["x"] < paddle["x"] + paddle["width"]:
        #print("Ball has hit paddle")
        #change the code in here so that the ball bounces off the paddle and does not teleport back up to the top
        bonusBall["ySpeed"] = -bonusBall["ySpeed"]
        score += 10
        # play sound
        play_music('bonus.mp3')

    
    #check if ball hits top of screen
    if ball["y"] < screen_top:
      ball["ySpeed"] = -ball["ySpeed"]

    # check if bonus ball hits top of screen
    if bonusBall["y"] < screen_top:
      bonusBall["ySpeed"] = -bonusBall["ySpeed"]

    #check if the ball is below the bottom of the screen
    if ball["y"] + ball["radius"] > height:
      fail_cnt = fail_cnt + 1
      lives = lives - 1
      ball["y"] = screen_top
      ball["x"] = randint(0,width)
      ball["xSpeed"] = randint(-fail_cnt,fail_cnt)
      # play sound
      play_music('fail.mp3')

    #check if the bonus ball is below the bottom of the screen
    if bonusBall["y"] + bonusBall["radius"] > height:
      bonusBall["y"] = screen_top
      bonusBall["x"] = randint(0,width)
      bonusBall["xSpeed"] = randint(-fail_cnt,fail_cnt)
      bonusBall["isVisable"] = False


    textsurface = font.render("Score: {0} Lives:{1}".format(score, lives), False, (0,0,0))
    screen.blit(textsurface, (10,10))

    # create a textsurface object at the upper right corner, clicking on it will quit the game
    textsurface = font.render("Quit", False, (0,0,0))
    screen.blit(textsurface, (width-100,10))
    if pygame.mouse.get_pressed()[0]:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] > width-100 and mouse_pos[0] < width-10 and mouse_pos[1] > 10 and mouse_pos[1] < 50:
        score = 0
        lives = 10
        fail_cnt = 0
        paddle_drop = 1

        break

    # color the text red if the mouse is over it
    if pygame.mouse.get_pos()[0] > width-100 and pygame.mouse.get_pos()[0] < width-10 and pygame.mouse.get_pos()[1] > 10 and pygame.mouse.get_pos()[1] < 50:
      textsurface = font.render("Quit", False, (255,255,255))
      screen.blit(textsurface, (width-100,10))


    if lives == 0:
      textsurface = font.render("Game Over! Your Score {0}".format(score), False, (0,0,0))
      screen.blit(textsurface, (400,300))
      play_music('gameover.mp3')
      pygame.time.delay(3000)
      break

    pygame.display.update()


main_menu()
