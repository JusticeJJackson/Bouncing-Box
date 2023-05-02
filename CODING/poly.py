import os
import time
import math
import random
import pygame
from pygame import mixer
import soundfile as sf
import numpy as np
from collections import defaultdict
from threading import Timer


pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)
pygame.mixer.set_num_channels(26)

'''
how the speakers are spreadout

1  2  3  4  5  6     4 == 12
11 11 11 10 11 12
13 14 15 16 17 18
19 20 21 22 23 24


1 19 9 23 2 
16        10
8         3
15        11
7         4
14        12
6 22 13 26 5

x = 5 y = 7

'''
SILENCE = 'silence.wav'
BOX_SIZE = 10
'''
record each box as its own 26 channel file, combine later,
allows for one track to play at a time,


add logic to only play audio if in a certain region
add play sound continously while moving
add a gui so I can add and remove items, maybe have it so it add boxes on beats
'''
sample_rate = 44100
bit_depth = -16

NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4 
CORNER = -1


chanPerWall = [[]] * 5
chanPerWall[NORTH] = [1, 19, 9, 23, 2]
chanPerWall[SOUTH] = [6, 22, 13, 26, 5]
chanPerWall[EAST] = [2 , 10, 3, 11, 4, 12, 5]
chanPerWall[WEST] = [1, 16, 8, 15, 7, 14, 6]


'''
1 19 9 23 2 
16        10
8         3
15        11
7         4
14        12
6 22 13 26 5
'''


cardinalRelativeToChan = []
cardinalRelativeToChan.append(defaultdict(lambda: (-1))) # 0 Index placeholder
cardinalRelativeToChan.append({0: 1, 1: 19, 2: 9, 3: 23, 4: 2}) # 1 Index NORTH
cardinalRelativeToChan.append({0: 6, 1: 22, 2: 13, 3: 26, 4: 5}) # 2 Index SOUTH
cardinalRelativeToChan.append({0: 2, 1: 10, 2: 3, 3: 11, 4: 4, 5: 12, 6: 5}) # 3 Index EAST
cardinalRelativeToChan.append({0: 1, 1: 16, 2: 8, 3: 15, 4: 7, 5: 14, 6: 6}) # 4 Index WEST

cardinalListChanToRelative = [
    {value: key for key, value in cardinal_dict.items()} for cardinal_dict in cardinalRelativeToChan
]


mixer.init()
mixer.pre_init(sample_rate, bit_depth, 26)
class Box:
    def __init__(
        self, initialY, initialX, veloY, veloX, boxColor: tuple, sound_file: str, canPlayTheseWalls: list, multiplier = float(1), chords = None
    ) -> None:
        self.yPos = initialY 
        self.xPos = initialX
        self.xVelo = veloX
        self.yVelo = veloY
        self.color = boxColor
        self.sound = mixer.Sound(sound_file)
        self.playWalls = canPlayTheseWalls
        self.multiplier = multiplier
        self.channel = pygame.mixer.Channel(0)
        self.chords = chords if chords is None else self.chordCaller()
     
    def canPlayWall(self, wall: int):
        return wall in self.playWalls
    
    def chordCaller(self):
        directory = "sounds"

        # get list of files in directory
        files = os.listdir(directory)

        # filter to only include .wav files
        wav_files = [f for f in files if f.endswith('.wav')]

        # load each sound and store in a list
        sounds = []
        for f in wav_files:
            path = os.path.join(directory, f)
            sound = pygame.mixer.Sound(path)
            sounds.append(sound)
                
        return sounds

    def onePlay(self):
        if self.chords:
            # pick a random chord from the list of chords
            chord_idx = random.randint(0, len(self.chords) - 1)
            chord = self.chords[chord_idx]
            
            # play the chord
            chord.play()
        else:
            self.sound.play()

"""class ChordBox(Box):
    def __init__(self, initialY, initialX, veloY, veloX, boxColor: tuple, sound_file: str, canPlayTheseWalls: list, multiplier = float(1)):
        super().__init__(initialY, initialX, veloY, veloX, boxColor, sound_file, canPlayTheseWalls)
                # set path to directory containing the wav files
        directory = "sounds"

        # get list of files in directory
        files = os.listdir(directory)

        # filter to only include .wav files
        wav_files = [f for f in files if f.endswith('.wav')]

        # load each sound and store in a list
        sounds = []
        for f in wav_files:
            path = os.path.join(directory, f)
            sound = pygame.mixer.Sound(path)
            sounds.append(sound)
                
        self.allChords = sounds
        self.chordSize = len(self.allChords)

        def onePlay(self):
            # pick a random chord from the list of chords
            chord_idx = random.randint(0, self.chordSize - 1)
            chord = self.allChords[chord_idx]
            print(chordbox)
            # play the chord
            chord.play()
            """



def draw_lines(screen, grid_width, grid_height, box_size, num_vertical_lines, num_horizontal_lines, line_color=(255, 255, 255)):
    for i in range(num_vertical_lines + 1):
        x = int(i * (grid_width * box_size / num_vertical_lines))
        pygame.draw.line(screen, line_color, (x, 0), (x, grid_height * box_size))

    for i in range(num_horizontal_lines + 1):
        y = int(i * (grid_height * box_size / num_horizontal_lines))
        pygame.draw.line(screen, line_color, (0, y), (grid_width * box_size, y))

    
# If you dont want the wall to play a sound pass in empty sound
class Grid:
    def __init__(self, sizeY, sizeX, yNorthSound=None, ySouthSound=None, xEastSound=None, xWestSound=None) -> None:
        self.sizeY = sizeY 
        self.sizeX = sizeX 
        self.yNorthSound = None if yNorthSound is None else mixer.Sound(yNorthSound)
        self.ySouthSound = None if ySouthSound is None else mixer.Sound(ySouthSound)
        self.xEastSound = None if xEastSound is None else mixer.Sound(xEastSound)
        self.xWestSound = None if xWestSound is None else mixer.Sound(xWestSound)

    def soundOnWall(self, wall: int):
        if wall == 0:
            return False
        if wall == 1:
            return self.yNorthSound is not None
        if wall == 2:
            return self.ySouthSound is not None
        if wall == 3:
            return self.xEastSound is not None
        if wall == 4:
            return self.xWestSound is not None
        else:
            print("INCORRECT VALUE")
            return None
    def playWall(self, wall: int, chan = -1):
        if chan != -1 and chan in chanPerWall[wall]:
            if wall == NORTH and self.yNorthSound is not None:
                self.yNorthSound.play()
            elif wall == SOUTH and self.ySouthSound is not None:
                self.ySouthSound.play()
            elif wall == EAST and self.xEastSound is not None:
                self.xEastSound.play()
            elif wall == WEST and self.xWestSound is not None:
                self.xWestSound.play()
            else:
                print("ERROR INVALID NUMBER")
                return None
        else:
            if wall == NORTH and self.yNorthSound is not None:
                self.yNorthSound.play()
            elif wall == SOUTH and self.ySouthSound is not None:
                self.ySouthSound.play()
            elif wall == EAST and self.xEastSound is not None:
                self.xEastSound.play()
            elif wall == WEST and self.xWestSound is not None:
                self.xWestSound.play()

        
    


    def draw_grid(self, screen, box_size, boxes, num_vertical_lines, num_horizontal_lines):
        screen.fill((0, 0, 0))
        for box in boxes:
            x, y = int(box.xPos * box_size), int(box.yPos * box_size)
            pygame.draw.rect(screen, (box.color[0], box.color[1], box.color[2]), (x, y, box_size, box_size))
        
        # Draw lines
        draw_lines(screen, self.sizeX, self.sizeY, box_size, num_vertical_lines, num_horizontal_lines)

        pygame.display.flip()




    


def create_box(initial_y, initial_x, timeInterval, time_signature, grid_size_y, grid_size_x, sound_file, tup, canPlayTheseWalls= None, multiplier = float(1)):
    

    velocityX = ((grid_size_x*BOX_SIZE)/(time_signature[0])) / (timeInterval*(4/time_signature[0]))
    velocityY = (grid_size_y*BOX_SIZE) / (timeInterval*(4/time_signature[0]))
    
    if canPlayTheseWalls is None:
        canPlayTheseWalls = []
    
    return Box(initial_y, initial_x, velocityY, velocityX, tup, sound_file, canPlayTheseWalls, multiplier)


def flash_screen(screen, num_flashes=3, duration=4):
    flash_interval = duration / (2 * num_flashes)
    for i in range(num_flashes):
        screen.fill((255, 255, 255))  # Set the screen to white
        pygame.display.flip()
        pygame.time.delay(int(flash_interval * 1000))
        
        screen.fill((0, 0, 0))  # Set the screen to black
        pygame.display.flip()
        pygame.time.delay(int(flash_interval * 1000))

def findChannelBounds(countOfXDivisions: int, countOfYDivisions: int, grid: Grid) :
        channelPositions = []
        for yChan in range(countOfYDivisions):
            row = []
            for xChan in  range(countOfXDivisions):
                xPos = (xChan % countOfXDivisions) * (grid.sizeX / countOfXDivisions)
                yPos = (yChan % countOfYDivisions) * (grid.sizeY / countOfYDivisions)
                row.append((yPos, xPos))    
            channelPositions.append(row)
        return channelPositions


def find_nearest_walls(y, x, grid_height, grid_width):
    distance_to_walls = {
        NORTH: y,
        SOUTH: grid_height - y,
        WEST: x,
        EAST: grid_width - x
    }

    nearest_y_wall = min([NORTH, SOUTH], key=lambda wall: distance_to_walls[wall])
    nearest_x_wall = min([WEST, EAST], key=lambda wall: distance_to_walls[wall])
    return nearest_y_wall, nearest_x_wall 


def checkIfInZone(box: Box, grid: Grid, divX, divY, targetChannel, walls):
    chanWidthY = gridSizeY / divY
    chanWidthX = gridSizeX / divX
    boolReturn = False
    if EAST in walls or WEST in walls:
        try:
            target_chunk_y = cardinalListChanToRelative[EAST if EAST in walls else WEST][targetChannel]
        except KeyError:
            print(f"KeyError: targetChannel {targetChannel} not found in the dictionary.")
            target_chunk_y = -1

        if target_chunk_y != -1 and is_box_in_chunk(box, grid, divX, divY, target_chunk_y=target_chunk_y):
            box.onePlay()
            boolReturn = True

    if (NORTH or SOUTH) in walls:
        #print('north or south relative =', cardinalListChanToRelative[NORTH if NORTH in walls else SOUTH][targetChannel])
        try:
            target_chunk_x = cardinalListChanToRelative[NORTH if NORTH in walls else SOUTH][targetChannel]
        except KeyError:
            print(f"KeyError: targetChannel {targetChannel} not found in the dictionary.")
                # Provide a default value or handle the error appropriately
            target_chunk_x = -1
        if target_chunk_x != 1 and is_box_in_chunk(box, grid, divX, divY, target_chunk_x=target_chunk_x):
            box.onePlay()
            boolReturn = True

    return boolReturn



def is_box_in_chunk(box: Box, grid: Grid, num_chunks_x, num_chunks_y, target_chunk_x=None, target_chunk_y=None):
    chunk_width = grid.sizeX / num_chunks_x
    chunk_height = grid.sizeY / num_chunks_y
    print("targetChunk",target_chunk_y if target_chunk_y is not None else target_chunk_x)
    print("chunkHeight =", chunk_height)
    print("chunk_width =", chunk_width)

    chunk_x = math.floor(box.xPos / chunk_width)
    chunk_y = math.floor(box.yPos / chunk_height)
    print('chunkX =', chunk_x)
    print('chunkY =', chunk_y)

    in_x_chunk = target_chunk_x is not None and chunk_x == target_chunk_x
    in_y_chunk = target_chunk_y is not None and chunk_y == target_chunk_y
    print(in_x_chunk or in_y_chunk)
    return in_x_chunk or in_y_chunk
'''
if its hitting a wall, check to see what speaker that wall belongs to, if its equal to our channel, play the sound

1 19 9 23 2 
16        10
8         3
15        11
7         4
14        12
6 22 13 26 5

'''

'''
def playSoundIfInZone(grid: Grid, channel: int, box: Box, divX, divY, wall: int, wallsColiding: list):
    relativeChanPosition = -1
    for walls in wallsColiding:
        if channel in chanPerWall[walls] and box.canPlayWall(walls):
            grid.playWall(walls)
    if NORTH in wallsColiding:
        if channelDict[channel] == CORNER:
            if find_nearest_walls(box.yPos, box.xPos, grid.sizeY, grid.sizeY)[1] == EAST:
                relativeChanPosition = 4
            else:
                relativeChanPosition = 0    
            if relativeChanPosition * (gridSizeX / divX) <= box.xPos:
                return
        else:
            relativeChanPosition = channelDict[channel]
'''      
            
        
def addBoxes(boxes: list[Box], box: Box):
    boxes.append(box)

def removeBoxes(boxes, box):
    boxes.remove(box)

def changeWallSound(cardinal, sound: pygame.mixer.Sound, grid: Grid):
    if cardinal == NORTH:
        grid.yNorthSound = sound
    elif cardinal == SOUTH:
        grid.ySouthSound = sound
    elif cardinal == EAST:
        grid.xEastSound = sound
    elif cardinal == WEST:
        grid.xWestSound = sound


def main(
    gridSizeY: int,
    gridSizeX: int,
    fps: int,
    boxes: list,
    currChan: int,
    oneChannel = True
):

    
    def mute_all_sounds(sound_objects, mute=True):
        for sound in sound_objects:
            if sound is not None:
                if mute:
                    sound.set_volume(0)
                else:
                    sound.set_volume(1)
    screen = pygame.display.set_mode((gridSizeX*BOX_SIZE, gridSizeY*BOX_SIZE))
    pygame.display.set_caption("Bouncing Box Simulation")
    clock = pygame.time.Clock()

    grid = Grid(gridSizeY, gridSizeX, yNorthSound="DEEPDOWN-BIG-H1.wav")
    running = True
    frame = 0
    startSound = mixer.Sound('race-start-beeps-125125.mp3')
    #startSound.play()
    #flash_screen(screen)
    #clock.tick_busy_loop(20)
    
    sound_objects = [box.sound for box in boxes] + [grid.yNorthSound, grid.ySouthSound, grid.xEastSound, grid.xWestSound]
    
    pingPong = create_box(0, 0, 4, (4, 4), gridSizeY, gridSizeX, '2.mp3',(137, 207, 240), [NORTH, EAST])
    fasterPingPong = create_box(0, 0, 4, (12, 4), gridSizeY, gridSizeX, '2.mp3',(137, 207, 240), [NORTH])
    detroit1 = create_box(0, 0, 4, (2,4), 70,50,"detroit wav.wav", (123,112,23), [NORTH], multiplier= .15)
    detroit2 = create_box(0, 0, 4, (3,4), 70,50,"detroit 2.wav", (123,210,223), [NORTH], multiplier= .15)
    detroit3 = create_box(0, 0, 4, (5,4), 70,50,"detroit 3.wav", (123,12,123), [NORTH], multiplier= .15)
    detroit = create_box(0, 0, 4, (2,4), 70,50,"detroit wav.wav", (123,112,23), [NORTH, EAST], multiplier= .15)
    detroi = create_box(0, 0, 4, (3,4), 70,50,"detroit 2.wav", (123,210,223), [NORTH, EAST], multiplier= .15)
    detro = create_box(0, 0, 4, (3,4), 70,50,"detroit 3.wav", (123,12,123), [NORTH, EAST], multiplier= .15)
    congo1 = create_box(56, 32, 4, (4, 4), gridSizeY, gridSizeX, 'WavePoint-Bongo_Conga_Mute1.wav',(137, 207, 240), [NORTH, EAST])
    congo2 = create_box(56, 52, 4, (8, 4), gridSizeY, gridSizeX, 'WavePoint-Bongo_Conga_Mute4.wav',(137, 207, 240), [NORTH, EAST, WEST], multiplier=.5)
    congo3 = create_box(56, 12, 4, (12, 4), gridSizeY, gridSizeX, 'WavePoint-Bongo_Conga4.wav',(137, 207, 240), [NORTH, EAST])
    chordbox = Box(0,0,15, 18, (255,255,255), SILENCE, [NORTH, SOUTH], chords=True)
    laser = Box(25,27,7,2, (123,21,222), "WavePoint-LaserB.wav", [])
    kickSnare = Box(14, 10, 5,6, (213,111,93), "WavePoint-KickShort.wav", [])
    snareBuildup = Box(30,30, 1,2, (255,255,255), "WavePoint-SnareBuildUp5-123bpm.wav", [] )

    def set_detroidSounds():    
        detroit2.sound.set_volume(.3)
        detroit3.sound.set_volume(.3)
        detroit1.sound.set_volume(.3)
    
        
    def firstActions():
        addBoxes(boxes, pingPong)
        addBoxes(boxes, fasterPingPong)
        removeBoxes(boxes, box2)
    
    def secondActions():
        removeBoxes(boxes, box1)
        removeBoxes(boxes, fasterPingPong)
        removeBoxes(boxes, box2)
    
    def thirdAction():
        changeWallSound(EAST, mixer.Sound("BIG WET KICK 01.wav"), grid)
        changeWallSound(WEST, mixer.Sound("BIG WET KICK 01.wav"), grid)

    def fourthAction():
        set_detroidSounds()
        addBoxes(boxes, detroit1)
        addBoxes(boxes, detroit2)
        addBoxes(boxes, detroit3)
    
    def fifthAction():
        detroit.sound.set_volume(.15)
        detroi.sound.set_volume(.15)
        detro.sound.set_volume(.15)
        addBoxes(boxes, detroit)
        addBoxes(boxes, detroi)
        addBoxes(boxes, detro)
    

    def sixthAction():
        addBoxes(boxes, congo1)
        addBoxes(boxes, congo2)
        addBoxes(boxes, congo3)
    
    def seventhAction():
        removeBoxes(boxes, detroit)
        removeBoxes(boxes, detro)
    
    def eigthAction():
        addBoxes(boxes, chordbox)
    
    def ninthAction():
        addBoxes(boxes, laser)
        addBoxes(boxes, kickSnare)
        addBoxes(boxes, snareBuildup)
    
    t = Timer(13, firstActions)
    i = Timer(15, secondActions)
    j = Timer(18, lambda: changeWallSound(NORTH, mixer.Sound("MINTFLOOR-ROOM-S1.wav"), grid))
    h = Timer(20, thirdAction)
    k = Timer(30, lambda: boxes.clear())
    d = Timer(36, fourthAction)
    y = Timer(50, lambda: boxes.clear())
    q = Timer(55, fifthAction)
    e = Timer(65, sixthAction)
    p = Timer(73, seventhAction)
    n = Timer(90, eigthAction)
    l = Timer(100, ninthAction)

    t.start()
    i.start()
    j.start()
    h.start()
    k.start()
    d.start()
    y.start()
    q.start()
    e.start()
    p.start()
    n.start()
    l.start()
    
    eigthAction()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for box in boxes:
            
            box.xPos += (box.xVelo / fps) * box.multiplier
            box.yPos += (box.yVelo / fps) * box.multiplier
            wallColide = 0
            wallsColiding = []
            if box.xPos < 0:
                wallColide = WEST
                wallsColiding.append(wallColide)
                box.xPos = 0  # Add this line to keep the box within the grid
            elif box.xPos > gridSizeX - 1:
                wallColide = EAST
                box.xPos = gridSizeX - 1  # Add this line to keep the box within the grid
                wallsColiding.append(wallColide)
            if box.yPos < 0:
                wallColide = NORTH
                wallsColiding.append(wallColide)
                box.yPos = 0  # Add this line to keep the box within the grid
            elif box.yPos > gridSizeY - 1:
                wallColide = SOUTH
                wallsColiding.append(wallColide)
                box.yPos = gridSizeY - 1  # Add this line to keep the box within the grid

            if wallColide == WEST or wallColide == EAST:
                box.xVelo = -box.xVelo
                if oneChannel:
                    checkIfInZone(box,grid,5,7,currChan,wallsColiding)
                else: #for debugging and music making
                    box.onePlay()
            if wallColide == NORTH or wallColide == SOUTH:
                box.yVelo = -box.yVelo
                if oneChannel: #for debugging and 
                    checkIfInZone(box,grid,5,7,currChan,wallsColiding)
                else: 
                    box.onePlay()

            if box.canPlayWall(wallColide) and grid.soundOnWall(wallColide):
                if oneChannel and currChan in chanPerWall[wallColide]:
                    grid.playWall(wallColide, currChan)
                else:
                    grid.playWall(wallColide)



            #print(box.xPos, box.yPos)
        grid.draw_grid(screen, BOX_SIZE, boxes, 5, 7)

        
        frame += 1
        elapsed_time = clock.tick_busy_loop(fps)
        '''
        if frame == 1000:
            mute_all_sounds(sound_objects, mute=True)
        if frame == 1200:
            mute_all_sounds(sound_objects, mute=False)
        '''
            
        

    pygame.quit()


gridSizeY = 70
gridSizeX = 50
runningFps = 120

box1 = create_box(30, 20,4, (8, 4), gridSizeY, gridSizeX, '1.wav', (255, 255, 0))
box2 = create_box(0, 0, 4, (4, 4), gridSizeY, gridSizeX, '2.mp3',(137, 207, 240), [NORTH], .66)
sound_file = "C:/Users/Justice/OneDrive - Virginia Tech/Documents/School/Sound in Space/Jungle Jungle - 1989 to 1999 Samplepack/Bass/19 Bass.wav"
box3 = create_box(0,0,4,(5,4),gridSizeY, gridSizeX, sound_file, (3,223, 143), multiplier= .1)
reverseBass = create_box(0, 0, 4, (1, 4), gridSizeY, gridSizeX, 'Gosh Bass.wav',(255, 255, 255), multiplier=.2)

boxes = [box1, box2]

main(gridSizeY, gridSizeX, 120, boxes, 11, oneChannel=False)
