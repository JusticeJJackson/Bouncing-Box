import os
import time
import math
import random
import pygame

# create a 2d square grid of ' ' strings that is 10 x 10 in size that codes it in a simple way

# TODO add changing colors to the square
"""
TODO New Methods

Move Box
-- Initialize Grid --
Handle Colisions
Randomize Velo
Animate
Which Walls
Distance To Walls
"""


class Box:
    def __init__(
        self, initialY, initialX, veloY, veloX, boxStr: str
    ) -> None:
        self.yPos = initialY
        self.xPos = initialX
        self.xVelo = veloX
        self.yVelo = veloY
        self.str = boxStr


class Grid:
    def __init__(self, sizeY, sizeX) -> None:
        self.sizeY = sizeY
        self.sizeX = sizeX
        self.grid = []
        for y in range(self.sizeY):
            self.grid.append([])
            for x in range(self.sizeX):
                self.grid[y].append(" ")

    def printGrid(self, iterationNumber: int):
        print(iterationNumber)

        # Calculate the width of the widest number in the grid
        max_num_width = len(str(max([num for row in self.grid for num in row])))

        # Calculate the number of digits in the number of rows
        num_row_digits = len(str(len(self.grid)))

        # Create the spacer string with spaces equal to the maximum number width
        spacer = " " * max_num_width

        # Create the top boundary of the grid
        top_boundary = "_" * (
            (max_num_width + 2) * len(self.grid[0]) + num_row_digits + 3
        )

        # Create the bottom boundary of the grid
        bottom_boundary = "‾" * (
            (max_num_width + 2) * len(self.grid[0]) + num_row_digits + 3
        )

        # Print the top boundary of the grid
        print(top_boundary)

        # Loop through each row in the grid
        for i, row in enumerate(self.grid):
            # Create the row string
            row_string = "▓ "
            for num in row:
                num_string = str(num)
                num_string = " " * (max_num_width - len(num_string)) + num_string
                row_string += num_string + " "
            row_string += " ▓"

            # Add extra space for row numbers with fewer digits than the max number of digits
            num_spaces = " " * (num_row_digits - len(str(i)))
            if i < 10:
                row_num_string = f"row {num_spaces}{i}:"
            else:
                row_num_string = f"row {i}:"

            # Print the row
            print(f"{row_num_string} {spacer}{row_string}")

        # Print the bottom boundary of the grid
        print(bottom_boundary)

    def setGrid(self, box: Box):
        self.grid[box.yPos][box.xPos] = box.str

    def clearGrid(self, box: Box):
        self.grid[box.yPos][box.xPos] = " "


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def isNegative(num: int):
    if num >= 0:
        return 1
    else:
        return -1


def whereIsColision(grid: list, box: Box) -> tuple[bool, bool, bool, bool, bool, bool]:
    return (
        # Checks East Wall
        box.xPos + box.xVelo > len(grid[0]) - 1,
        # Checks West Wall
        box.xPos + box.xVelo < 0,
        # Checks North Wall
        box.yPos + box.yVelo < 0,
        # Checks South Wall
        box.yPos + box.yVelo > len(grid) - 1,
        # Checks if its hitting on the y-axis
        box.yPos + box.yVelo < 0 or box.yPos + box.yVelo > len(grid) - 1,
        # Checks if its hitting on the x-axis
        box.xPos + box.xVelo > len(grid[0]) - 1 or box.xPos + box.xVelo < 0,
    )


def distanceToWall(box: Box, grid: list):
    if box.yPos >= (len(grid) // 2):
        yield len(grid) - box.yPos - 1

    else:
        yield box.yPos

    if box.xPos >= (len(grid[0]) // 2):
        yield len(grid[0]) - box.xPos - 1

    else:
        yield box.xPos


# Pun Intented
def cornerCase(box: Box, grid: list):
    if box.xVelo < 0:
        box.xPos = 0
    else:
        box.xPos = len(grid[0]) - 1
    if box.yVelo < 0:
        box.yPos = 0
    else:
        box.yPos = len(grid) - 1

    addedVeloX = random.random()
    addedVeloY = random.random()

    if bool(random.getrandbits(1)):
        addedVeloX = addedVeloX * -1

    if bool(random.getrandbits(1)):
        addedVeloY = addedVeloY * -1

    if abs(box.yVelo * (1 + addedVeloY)) <= 1:
        box.yVelo = 1 * isNegative(box.yVelo)

    else:
        box.yVelo = -1 * int(box.yVelo * (1 + addedVeloY))

    if abs(box.xVelo * (1 + addedVeloX)) <= 1:
        box.xVelo = 1 * isNegative(box.xVelo)

    else:
        box.xVelo = -1 * int(box.xVelo * (1 + addedVeloX))


def singleColision(box: Box, grid: list):
    xEast, xWest, yNorth, ySouth, yWall, xWall = whereIsColision(grid, box)

    # counts the difference of the obj to the walls (how close they are)
    yDistanceToWall, xDistanceToWall = distanceToWall(box, grid)

    if xWall:
        # what percent of the way will the obj move before it hits the all i.e
        # an object is 3 away from the wall but has a velo of 6 will only make it half the way
        xRatio = abs(xDistanceToWall / box.xVelo)
        yRatio = abs(yDistanceToWall / box.yVelo)
        if xEast:
            box.xPos = len(grid[0]) - 1
        else:
            box.xPos = 0
        if xDistanceToWall == 0:
            box.yPos = box.yPos
        elif box.yVelo > 0:
            box.yPos = min(int(box.yPos + round(box.yVelo * xRatio)), len(grid))
        elif box.yVelo < 0:
            box.yPos = max(int(box.yPos + round(box.yVelo * xRatio)), 0)
    else:
        # what percent of the way will the obj move before it hits the all i.e
        # an object is 3 away from the wall but has a velo of 6 will only make it half the way
        xRatio = abs(xDistanceToWall / box.xVelo)
        yRatio = abs(yDistanceToWall / box.yVelo)
        if ySouth:
            box.yPos = len(grid) - 1
        else:
            box.yPos = 0
        if yDistanceToWall == 0:
            box.xPos = box.xPos
        if box.xVelo > 0:
            box.xPos = min(int(box.xPos + round(box.xVelo * yRatio)), len(grid[0]))
        elif box.xVelo < 0:
            box.xPos = max(int(box.xPos + round(box.xVelo * yRatio)), 0)
    if not (xWall and yWall):
        if xWall:
            box.xVelo = box.xVelo * -1
        if yWall:
            box.yVelo = box.yVelo * -1


def handleColision(box: Box, grid: list):
    # calculates what walls they are near
    xEast, xWest, yNorth, ySouth, yWall, xWall = whereIsColision(grid, box)

    # If the next movement will result in a corner
    # bump, set values to the corners
    if xWall and yWall:
        cornerCase(box, grid)

    else:
        singleColision(box, grid)

    changeBoxColor(box)


def isColision(box: Box, grid: list) -> bool:
    walls = whereIsColision(grid, box)

    return walls[0] or walls[1] or walls[2] or walls[3]


def changeBoxColor(box: Box, color=None):
    boxes = [
        "■",
        "□",
        "▢",
        "▣",
        "▤",
        "▥",
        "▦",
        "▧",
        "▨",
        "▩",
    ]

    if color == None:
        box.str = boxes[random.randint(0, len(boxes) - 1)]
    else:
        box.str = boxes[color]


def draw_grid(grid, screen, box_size, box):
    screen.fill((0, 0, 0))
    for y, row in enumerate(grid.grid):
        for x, cell in enumerate(row):
            if cell == box.str:
                pygame.draw.rect(screen, (255, 255, 255), (x * box_size, y * box_size, box_size, box_size))
    pygame.display.flip()

def polyrhythm(initialY: int, initialX: int, beat: int, bpm: int, box: Box, grid: Grid):
    xLen = grid.sizeX
    yLen = grid.sizeY

    beatsPerSecond = bpm / 60

    timePerBeat = 1 / beatsPerSecond

    # timePerMeasure = 4 * timePerBeat

    timePerBounce = (4 / beat) * timePerBeat

    xBounceDistance = xLen / beat

    xVelo = xBounceDistance // timePerBounce

    yVelo = yLen // timePerBounce

    return xVelo, yVelo

def main(
    gridSizeY: int,
    gridSizeX: int,
    initialY: int,
    initialX: int,
    fps: int,
    yVelocity: int,
    xVelocity: int,
    disco: bool,
):
    pygame.init()
    box_size = 10
    screen = pygame.display.set_mode((gridSizeX * box_size, gridSizeY * box_size))
    pygame.display.set_caption("Bouncing Box Simulation")
    clock = pygame.time.Clock()

    grid = Grid(gridSizeY, gridSizeX)
    box = Box(initialY, initialX, yVelocity, xVelocity, "■")
    #x , y = polyrhythm(0, 0 , 4, 120 , box, grid)
    #box.yVelo, box.xVelo = x, y
    grid.setGrid(box)

    running = True
    frame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if disco:
            changeBoxColor(box)

        grid.clearGrid(box)

        if isColision(box, grid.grid):
            handleColision(box, grid.grid)
        else:
            box.xPos += box.xVelo
            box.yPos += box.yVelo

        grid.setGrid(box)
        draw_grid(grid, screen, box_size, box)

        frame += 1
        clock.tick(fps)

    pygame.quit()


main(50, 70, 2, 3, 45, 2, -4, True)




#polyrhythm(0, 0, 4, 120, Box(1, 1, 1, 1, " "), Grid(8, 8))
