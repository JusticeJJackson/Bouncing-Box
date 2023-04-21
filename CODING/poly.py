import os
import time
import math
import random

# create a 2d square grid of ' ' strings that is 10 x 10 in size that codes it in a simple way

# TODO add changing colors to the square
sizeY = 12
sizeX = 7

grid = []
for x in range(sizeX):
    grid.append([])
    for y in range(sizeY):
        grid[x].append(" ")


# print the array so it looks like a grid
def printGrid1():
    for row in range(len(grid)):
        # to make the output print equally, if a digit is longer than 1, add a space to the spacer
        # for every digit over 1, i.e if a digit is 10, the spacer will be ' ' if the digit is
        # 100 the sapcer will be '  '
        spacer = " " * (len(str(len(grid))) - len(str(row)))
        print("row " + str(row) + ": " + spacer + str(grid[row]))


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def printGrid(grid):
    # Calculate the width of the widest number in the grid
    max_num_width = len(str(max([num for row in grid for num in row])))

    # Calculate the number of digits in the number of rows
    num_row_digits = len(str(len(grid)))

    # Create the spacer string with spaces equal to the maximum number width
    spacer = " " * max_num_width

    # Create the top boundary of the grid
    top_boundary = "_" * ((max_num_width + 2) * len(grid[0]) + num_row_digits + 3)

    # Create the bottom boundary of the grid
    bottom_boundary = "‾" * ((max_num_width + 2) * len(grid[0]) + num_row_digits + 3)

    # Print the top boundary of the grid
    print(top_boundary)

    # Loop through each row in the grid
    for i, row in enumerate(grid):
        # Create the row string
        row_string = "▓ "
        for num in row:
            num_string = str(num)
            num_string = " " * (max_num_width - len(num_string)) + num_string
            row_string += num_string + " "
        row_string += "▓"

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


def isNegative(num: int):
    if num >= 0:
        return 1
    else:
        return -1


def move1(initialX: int, initialY: int, fps: int, veloX: int, veloY: int):
    grid[initialY][initialX] = "■"
    currX: int = initialX
    currY: int = initialY
    for x in range(60 * 15):
        clear_terminal()
        # each loop clear the output of terminal

        print(x)
        printGrid(grid)
        grid[currY][currX] = " "

        # move the 1 to position currX + veloX, same with y, if the new position is out of bounds,
        # reverse the velocity

        """
        if currX + veloX < 0 or currX + veloX > len(grid[0]) - 1:
            veloX *= -1
        if currY + veloY < 0 or currY + veloY > len(grid) - 1:
            veloY *= -1
        """

        """
        if the new position has one of the 1 is out of bounds on the x or y
        have the 1 just hit the wall, then reverse its velocity, have the 
        other cordinate only move the amount proportinal to how the other
        value moved
        """

        if (
            currX + veloX < 0
            or currX + veloX > len(grid[0]) - 1
            or currY + veloY < 0
            or currY + veloY > len(grid) - 1
        ):
            # seeing if the obj is near the x walls or y walls
            xWall = currX + veloX < 0 or currX + veloX > len(grid[0]) - 1
            yWall = currY + veloY < 0 or currY + veloY > len(grid) - 1

            # counts the difference of the obj to the walls (how close they are)
            yToWall = 0
            xToWall = 0

            # signals what wall its near
            xEast = False
            xWest = False
            ySouth = False
            yNorth = False

            if currY >= (len(grid) // 2):
                yToWall = len(grid) - currY - 1
                if yWall:
                    ySouth = True
            else:
                yToWall = currY
                if yWall:
                    yNorth = True
            if currX >= (len(grid[0]) // 2):
                xToWall = len(grid[0]) - currX - 1
                if xWall:
                    xEast = True
            else:
                xToWall = currX
                if xWall:
                    xWest = True

            # If the next movement will result in a corner
            # bump, set values to the corners
            if xWall and yWall:
                if veloX < 0:
                    currX = 0
                else:
                    currX = len(grid[0]) - 1
                if veloY < 0:
                    currY = 0
                else:
                    currY = len(grid) - 1

                addedVeloX = random.random()
                addedVeloY = random.random()

                if bool(random.getrandbits(1)):
                    addedVeloX = addedVeloX * -1

                if bool(random.getrandbits(1)):
                    addedVeloY = addedVeloY * -1

                if abs(veloY * (1 + addedVeloY)) <= 1:
                    veloY = 1 * isNegative(veloY)
                else:
                    veloY = -1 * int(veloY * (1 + addedVeloY))

                if abs(veloX * (1 + addedVeloX)) <= 1:
                    veloX = 1 * isNegative(veloX)
                else:
                    veloX = -1 * int(veloX * (1 + addedVeloX))

                """veloY = -1 * max(1, int(veloY * (1 + addedVeloY)))
                veloX = -1 * max(1, int(veloX * (1 + addedVeloX)))"""
            else:
                if xWall:
                    # what percent of the way will the obj move before it hits the all i.e
                    # an object is 3 away from the wall but has a velo of 6 will only make it half the way
                    xRatio = abs(xToWall / veloX)
                    yRatio = abs(yToWall / veloY)

                    if xEast:
                        currX = len(grid[0]) - 1
                    else:
                        currX = 0

                    if xToWall == 0:
                        currY = currY
                    elif veloY > 0:
                        currY = min(int(currY + round(veloY * xRatio)), len(grid))
                    elif veloY < 0:
                        currY = max(int(currY + round(veloY * xRatio)), 0)

                else:
                    # what percent of the way will the obj move before it hits the all i.e
                    # an object is 3 away from the wall but has a velo of 6 will only make it half the way
                    xRatio = abs(xToWall / veloX)
                    yRatio = abs(yToWall / veloY)

                    if ySouth:
                        currY = len(grid) - 1
                    else:
                        currY = 0

                    if yToWall == 0:
                        currX = currX
                    if veloX > 0:
                        currX = min(int(currX + round(veloX * yRatio)), len(grid[0]))
                    elif veloX < 0:
                        currX = max(int(currX + round(veloX * yRatio)), 0)

                if not (xWall and yWall):
                    if xWall:
                        veloX = veloX * -1
                    if yWall:
                        veloY = veloY * -1
        else:
            currX += veloX
            currY += veloY

        grid[currY][currX] = "■"

        # wait one frame length before continuing
        time.sleep(1 / fps)


move1(3, 3, 20, 2, 3)
