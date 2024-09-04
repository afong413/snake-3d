import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from random import seed, randint
from time import time

from math import pi, sin, cos

seed()

# glClearDepth(1.0)
# glDepthFunc(GL_LESS
# glEnable(GL_DEPTH_TEST)

# glDepthFunc(GL_LESS)
# glEnable(GL_DEPTH_TEST)

screenWidth = 1000
screenHeight = 750

gameWidth = 20
gameHeight = 20
boxWidth = 20

snake = [[2, 0], [1, 0], [0, 0]]
snakeDirection = 0
snakeHeadExact = [2, 0]
snakeHead = [2, 0]

eye = [0, 0, 0]
eyeDirection = 0

score = 0

gameOver = False


def removeRepeats(inputList):
    outputList = []

    for i in inputList:
        if i not in outputList:
            outputList.append(i)

    return outputList


def square(
    p0,
    p1,
    p2,
    p3,
    lines=True,
    lineWidth=5,
    lineColor=(1, 1, 1),
    filled=False,
    faceColor=(0, 0, 0),
):
    verticies = (p0, p1, p2, p3)

    edges = ((0, 1), (1, 2), (2, 3), (3, 0))

    # if filled:
    #    glBegin(GL_QUADS)
    #    glColor3fv(faceColor)
    #    for vertex in verticies:
    #        glVertex3fv(vertex)
    #    glEnd()

    if lines:
        glBegin(GL_LINES)
        glColor3fv(lineColor)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(verticies[vertex])
        glEnd()

    if filled:
        glBegin(GL_QUADS)
        glColor3fv(faceColor)
        for vertex in verticies:
            glVertex3fv(vertex)
        glEnd()


def cube(
    x,
    y,
    z,
    sideLength,
    lines=True,
    lineWidth=5,
    lineColor=(1, 1, 1),
    filled=False,
    faceColor=(0, 0, 0),
):
    sL = sideLength
    verticies = [
        (x, y, z),
        (x + sL, y, z),
        (x, y + sL, z),
        (x + sL, y + sL, z),
        (x, y, z - sL),
        (x + sL, y, z - sL),
        (x, y + sL, z - sL),
        (x + sL, y + sL, z - sL),
    ]

    faces = [
        (0, 1, 3, 2),
        (0, 1, 5, 4),
        (0, 2, 6, 4),
        (1, 3, 7, 5),
        (2, 3, 7, 6),
        (4, 5, 7, 6),
    ]

    for face in faces:
        square(
            verticies[face[0]],
            verticies[face[1]],
            verticies[face[2]],
            verticies[face[3]],
            lines=lines,
            lineColor=lineColor,
            filled=filled,
            faceColor=faceColor,
        )


def drawBoard(gameWidth, gameHeight, boxWidth):
    for col in range(0, gameWidth):
        for row in range(0, gameHeight):
            p0 = (col * boxWidth, 0, -row * boxWidth)
            p1 = (col * boxWidth + boxWidth, 0, -row * boxWidth)
            p2 = (col * boxWidth + boxWidth, 0, -row * boxWidth - boxWidth)
            p3 = (col * boxWidth, 0, -row * boxWidth - boxWidth)
            square(p0, p1, p2, p3, filled=True, faceColor=(1, 0.5, 0))


def drawWalls(gameWidth, gameHeight, boxWidth):
    for col in range(0, gameWidth):
        p0 = (col * boxWidth, 0, 0)
        p1 = (col * boxWidth + boxWidth, 0, 0)
        p2 = (col * boxWidth + boxWidth, boxWidth, 0)
        p3 = (col * boxWidth, boxWidth, 0)
        p4 = (col * boxWidth, 0, -1 * gameHeight * boxWidth)
        p5 = (col * boxWidth + boxWidth, 0, -1 * gameHeight * boxWidth)
        p6 = (col * boxWidth + boxWidth, boxWidth, -1 * gameHeight * boxWidth)
        p7 = (col * boxWidth, boxWidth, -1 * gameHeight * boxWidth)
        square(p0, p1, p2, p3, filled=True, faceColor=(1, 0, 1))
        square(p4, p5, p6, p7, filled=True, faceColor=(1, 0, 1))
    for row in range(0, gameHeight):
        p0 = (0, 0, -1 * row * boxWidth)
        p1 = (0, 0, -1 * row * boxWidth - boxWidth)
        p2 = (0, boxWidth, -1 * row * boxWidth - boxWidth)
        p3 = (0, boxWidth, -1 * row * boxWidth)
        p4 = (gameWidth * boxWidth, 0, -1 * row * boxWidth)
        p5 = (gameWidth * boxWidth, 0, -1 * row * boxWidth - boxWidth)
        p6 = (gameWidth * boxWidth, boxWidth, -1 * row * boxWidth - boxWidth)
        p7 = (gameWidth * boxWidth, boxWidth, -1 * row * boxWidth)
        square(p0, p1, p2, p3, filled=True, faceColor=(0, 0, 1))
        square(p4, p5, p6, p7, filled=True, faceColor=(0, 0, 1))


def placeApple(gameWidth, gameHeigth):
    global apple

    apple = snake[0]
    while apple in snake:
        apple = [randint(0, gameWidth - 1), randint(0, gameHeight - 1)]


def drawApple(boxWidth):
    global apple

    cube(
        boxWidth * apple[0],
        0,
        -1 * boxWidth * apple[1],
        boxWidth,
        filled=True,
        faceColor=(1, 0, 0),
    )


def getApple(gameWidth, gameHeight):
    global score

    score += 1
    placeApple(gameWidth, gameHeight)


def drawSnakeEdge(x, y, angle):
    if angle == 0:
        p1 = (x - (boxWidth / 2), y - (boxWidth / 2))
        p2 = (x + (boxWidth / 2), y - (boxWidth / 2))
    if angle == 90:
        p1 = (x + (boxWidth / 2), y - (boxWidth / 2))
        p2 = (x + (boxWidth / 2), y + (boxWidth / 2))
    if angle == 180:
        p1 = (x + (boxWidth / 2), y + (boxWidth / 2))
        p2 = (x - (boxWidth / 2), y + (boxWidth / 2))
    if angle == 270:
        p1 = (x - (boxWidth / 2), y + (boxWidth / 2))
        p2 = (x - (boxWidth / 2), y - (boxWidth / 2))

    glBegin(GL_LINES)
    glColor3fv((1, 1, 1))
    glVertex3fv(p1)
    glVertex3fv(p2)
    glEnd()


def drawSnakeCorner(x, y, angle):
    a1 = (angle + 180) % 360
    a2 = (angle - 90) % 360
    a3 = angle

    drawSnakeEdge(x, y, a1)
    drawSnakeEdge(x, y, a2)
    drawSnakeEdge(x, y, a3)


def drawSnake(boxWidth):
    global snake

    # snakeEdges = []
    # for segment in snake

    for segment in snake:
        cube(
            boxWidth * segment[0],
            0,
            -1 * boxWidth * segment[1],
            boxWidth,
            filled=True,
            faceColor=(0, 1, 0),
        )


def radian(degree):
    return pi * (degree / 180)


def goTo(eyeX, eyeY, eyeZ, direction):
    global eye
    global eyeDirection

    glTranslatef(eye[0], eye[1], eye[2])
    glRotatef(-1 * (direction - eyeDirection), 0, 1, 0)
    glTranslatef(-1 * eye[0], -1 * eye[1], -1 * eye[2])

    glTranslatef(
        -1 * (eyeX - eye[0]), -1 * (eyeY - eye[1]), -1 * (eyeZ - eye[2])
    )

    eye = [eyeX, eyeY, eyeZ]
    eyeDirection = direction


def updateCamera(boxWidth):
    global snakeHeadExact
    global snakeDirection

    vx = cos(radian(snakeDirection))
    vy = 2
    vz = -1 * sin(radian(snakeDirection))

    center = (
        boxWidth * snakeHead[0] + (boxWidth / 2),
        boxWidth / 2,
        -1 * boxWidth * snakeHead[1] - (boxWidth / 2),
    )

    x = center[0] + (boxWidth / 2) * cos(radian(snakeDirection))
    y = center[1]
    z = center[2] - (boxWidth / 2) * sin(radian(snakeDirection))

    goTo(x, y, z, snakeDirection)

    # gluLookAt(0, 0, 0, center[0], center[1], center[2], 0, 1, 0)
    # gluLookAt(0,0,0,0,0,-1,0,1,0)
    # gluLookAt(0,0,10,0,0,5,0,1,9)


def updateSnake():
    global snakeHeadExact
    global snakeHead
    global snake
    global snakeDirection
    global nextDirection
    global apple
    global gameWidth
    global gameHeight

    snakeHeadExact[0] += 0.06 * cos(radian(snakeDirection))
    snakeHeadExact[1] += 0.06 * sin(radian(snakeDirection))

    newSnakeHead = [round(snakeHeadExact[0]), round(snakeHeadExact[1])]

    if newSnakeHead != snakeHead:
        snakeHead = newSnakeHead
        if snakeHead == apple:
            getApple(gameWidth, gameHeight)
            snake.insert(0, snakeHead)
        else:
            for i in range(0, len(snake)):
                n = len(snake) - i - 1
                if n > 0:
                    snake[n] = snake[n - 1]
                else:
                    snake[n] = snakeHead

    # if snakeHead[0] % 1 == 0 and snakeHead[1] % 1 == 0:
    #    snakeDirection = nextDirection


def main():
    global gameOver
    global snakeDirection
    global nextDirection
    global boxWidth
    global gameWidth
    global gameHeight
    global score

    nextDirection = snakeDirection

    pygame.init()
    screen = pygame.display.set_mode(
        (screenWidth, screenHeight), DOUBLEBUF | OPENGL
    )
    pygame.display.set_caption("Snake 3D 1.1")
    gluPerspective(75, screenWidth / screenHeight, 0.1, 500.0)
    glRotatef(90, 0, 1, 0)
    placeApple(gameWidth, gameHeight)

    clock = pygame.time.Clock()
    while not gameOver:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                oldDirection = snakeDirection
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snakeDirection += 90
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snakeDirection -= 90

                if [
                    round(snakeHead[0] + cos(radian(snakeDirection))),
                    round(snakeHead[1] - sin(radian(snakeDirection))),
                ] == snake[2]:
                    snakeDirection = oldDirection

        keys = pygame.key.get_pressed()

        up = keys[pygame.K_UP] or keys[pygame.K_w]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        upDown = snakeDirection == 90 or 270
        leftRight = snakeDirection == 0 or snakeDirection == 180

        updateSnake()

        if snake.count(snakeHead) > 2:
            gameOver = True

        if (
            snakeHead[0] < 0
            or snakeHead[0] > gameWidth - 1
            or snakeHead[1] < 0
            or snakeHead[1] > gameHeight - 1
        ):
            gameOver = True

        if gameOver == True:
            break

        updateCamera(boxWidth)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        drawBoard(gameWidth, gameHeight, boxWidth)
        drawWalls(gameWidth, gameHeight, boxWidth)
        drawApple(boxWidth)
        drawSnake(boxWidth)

        pygame.display.flip()

    printScore = f"*   SCORE: {score}   *"
    print()
    print()
    for i in range(0, len(printScore)):
        print("*", end="")
    print()
    print("*", end="")
    for i in range(0, len(printScore) - 2):
        print(" ", end="")
    print("*")
    print(printScore)
    print("*", end="")
    for i in range(0, len(printScore) - 2):
        print(" ", end="")
    print("*")
    for i in range(0, len(printScore)):
        print("*", end="")
    print()
    print()
    print()


main()
