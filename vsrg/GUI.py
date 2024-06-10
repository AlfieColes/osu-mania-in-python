import pygame
import time
import os
from pathlib import Path

pygame.init()
pygame.mixer.init()
pygame.font.init()


#screenWidth = 1000##
#screenHeight = 800##
buttonList = []
Arial = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()
base_dir = Path(__file__).parent 


#screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)##
#screen.fill((0,0,0))##

#make a gui ig
#comboText = font.render(str(combo), False, (255,255,255))
#screen.blit(receptor1.image, (receptor1.xcoord, receptor1.ycoord))




class Button():
    def __init__(self, values, image, font, text, colour):
        self.values = values #xcoord, ycoord, width, height
        self.image = image #image can either be an image file or text
        self.font = font
        self.text = text
        self.colour = colour
        self.rect = pygame.Rect(self.values[0], self.values[1], self.values[2], self.values[3])
        buttonList.append(self)
        if self.image is None:
            self.image = self.font.render(self.text, True, self.colour)

    def makeImage(self):
        surface = pygame.Surface((self.values[2], self.values[3]))
        pygame.draw.rect(surface, (255,255,255), (0,0,self.values[2],self.values[3]), 1)
        surface.blit(self.image, (0,10))
        self.image = surface


def scroll(direction, buttonList): #direction is the value to be moved by
    for button in buttonList:
        button.values[1]+= direction
        button.rect = button.rect.move(0, direction)


def buttonClick(song):
    mouseCoords  =  pygame.mouse.get_pos()
    for button in buttonList:
        if button.rect.collidepoint(mouseCoords): #checks if the mouse is within the button
            song = button.text
    return song





def keys(eventList, buttonList, song):
    for event in eventList:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:#scroll up
                scroll(-40, buttonList)
            if event.button == 5:#scroll down
                scroll(40, buttonList)
            if event.button == 1: #left click
                song = buttonClick(song)
    return song


def displayButtons(buttonList, screen): #also checks to move buttons out when mouse is hovered, for efficiency
    mouseCoords  =  pygame.mouse.get_pos()
    for button in buttonList:
        screen.blit(button.image, (button.values[0], button.values[1]))

        ################### checking for mouse and moving buttons ###########################
        if button.rect.collidepoint(mouseCoords):
            if button.values[0] == 0:
                button.values[0] += 20
        

        else:
            button.values[0] = 0

def getSongs(path):
    songList = os.listdir(path)
    counter = 0
    for song in songList.copy():
        if song.split(".",1)[1] != "txt":
            songList.remove(song)
        else:
            songList[counter] = song.split(".",1)[0]
            counter += 1
    return songList

def makeButtons(songList):
    counter  = 0
    for song in songList:
        button = Button([0,(counter*50), 500, 50], None, Arial, song, (255,255,255))
        button.makeImage()
        counter += 1




def main(screen):
    makeButtons(getSongs(base_dir/"songs"))
    song = False

    while song == False:
        clock.tick(60)
        screen.fill((0,0,0))
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        song = keys(eventList, buttonList, song)
        displayButtons(buttonList, screen)
        pygame.display.flip()
    return song

#song = main()
#print(song)

#pygame.quit()




