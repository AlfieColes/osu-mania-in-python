import pygame
import time
from pathlib import Path

pygame.init()
pygame.mixer.init()
pygame.font.init()

########## globals ##########
font = pygame.font.SysFont("Arial", 30)
screenWidth = 1920
screenHeight = 1080
notesArray = [] #list of all notes
lane1 = [] #list of all notes in lane 1 etc
lane2 = []
lane3 = []
lane4 = []
LNcover = [] #stores 4 LNcover surfaces and a boolean for each one, which flags if they should be blit or not
combo = 0
accuracy = 0
judgement = ["", (0,0,0)] #array for judgement where [0] is judgement text and [1] is text colour
scoresArray = [0,0,0,0,0,0,(200,200,255),(200,200,0),(0,200,0),(0,0,200),(160,30,240),(200,0,0), "Flawless", "Perfect", "Great", "Good", "Ok", "Miss"] #every judgement count and colour
base_dir = Path(__file__).parent #this is a constant of the file path to get to the folder this program is in, so it works on every computer
LNtop = pygame.image.load(base_dir / "skin/LN top.png")
LNbody = pygame.image.load(base_dir / "skin/LN body.png")
noteImage = pygame.image.load(base_dir / "skin/note.png") 

########## screen ###########
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
screen.fill((0,0,0))

########## gameplay mods ##########
scrollSpeed = 33 #pixels per frame
framerate = 60
rateMod = 1

################idk how to better do this############
frameRatio = framerate/60
scrollSpeed /= frameRatio

#################### classes ####################

class Note():
    def __init__(self, lane, xcoord, ycoord, notesArray, laneList):
        self.lane = lane
        self.xcoord = xcoord
        self.ycoord = ycoord
        notesArray.append(self)
        laneList.append(self)
        self.image = pygame.image.load(base_dir / "skin/note.png")


class LongNote(Note):
    def __init__(self, lane, xcoord, ycoord, notesArray, laneList, start): #ycoord is end of ln
        super().__init__(lane, xcoord, ycoord, notesArray, laneList)
        self.start = start
        self.isHit = False
        self.isHeld = False

    def makeImage(self):

        #have to do this bc get_height doesnt work with paths
        #LNtop = pygame.image.load(base_dir / "skin/LN top.png") #had to make these global
        #LNbody = pygame.image.load(base_dir / "skin/LN body.png")
        #note = pygame.image.load(base_dir / "skin/note.png")

        surfaceHeight = abs(self.ycoord - (self.start + noteImage.get_height())) #calculating height of surface, this seems confusing bc theyre negative numbers so adding is subtracting

        if surfaceHeight < noteImage.get_height():
            surfaceHeight = noteImage.get_height()

        surface = pygame.Surface((noteImage.get_width(), surfaceHeight), pygame.SRCALPHA) #scralpha makes the surface transparent

        LNheight = (surface.get_height() - (LNtop.get_height())) - ((noteImage.get_height())/2) #gets how long the ln body is
        if LNheight < 0: #this is to make it so that if a ln is really short it doesnt crash
            LNheight = 0

        newLNbody = pygame.transform.scale(LNbody, (LNbody.get_width(), LNheight)) #stretches ln body to the correct height

        ########## blitting all parts of ln to the surface ##########

        surface.blit (LNtop, (0, 0))
        surface.blit (newLNbody, (0, LNtop.get_height()))
        surface.blit(noteImage, (0, surface.get_height() - noteImage.get_height()))

        self.image = surface

    def getHit(self):
        self.isHit = True

    def holding(self):
        self.isHeld = True



class Receptor():
    def __init__(self,xcoord):
        self.xcoord = xcoord
        self.ycoord = 800
        self.image = pygame.image.load(base_dir / "skin/hit receptor.png")

    def updateImage(self, keydown):
        if keydown == 1:
            self.image = pygame.image.load(base_dir / "skin/hit receptor keydown.png")
        elif keydown == 0:
            self.image = pygame.image.load(base_dir / "skin/hit receptor.png")
        else:
            self.image = pygame.image.load(base_dir / "skin/note.png")


#################### functions ####################

def noteHit(combo, notesArray, lane, scoresArray, judgement): #function that determines if a note is hit when a key is pressed
    #might have to make this a method of note class

    #Judgements (ms): 16.5, 43.5, 76.5, 106.5, 130.5, 167
    note = lane[0]

    #gets where the timing should be from, incase its the beginning of an ln
    if type(note) is LongNote:
        if note.isHit == False:
            position = note.start #start of ln
        else:
            position = note.ycoord #end of ln

    else:
        position = note.ycoord #normal note

    noteTiming = ((800 - position) / scrollSpeed) * (1000/framerate)
    if type(note) is LongNote and position == note.ycoord:
        noteTiming /= 1.5 #makes timing for end of ln more forgiving

    if noteTiming <= 16.5 and noteTiming >= -16.5: #marvellous
        combo += 1
        scoresArray[0] = scoresArray[0] + 1
        judgement[0] = "Flawless"
        judgement[1] = scoresArray[6]

        if position == note.ycoord: #checks to see if it should remove the note, this is so it doesnt remove an ln when its hit at the beginning
            notesArray.remove(note)
            lane.remove(note)
        else:
            note.getHit() #this is so that the ln doesnt get removed if you hit the beginning



    elif noteTiming <= 43.5 and noteTiming >= -43.5: #perfect
        combo += 1
        scoresArray[1] = scoresArray[1] + 1
        judgement[0] = "Perfect"
        judgement[1] = scoresArray[7]
        if position == note.ycoord:
            notesArray.remove(note)
            lane.remove(note)
        else:
            note.getHit()

    elif noteTiming <= 76.5 and noteTiming >= -76.5: #great
        combo += 1
        scoresArray[2] = scoresArray[2] + 1
        judgement[0] = "Great"
        judgement[1] = scoresArray[8]
        if position == note.ycoord:
            notesArray.remove(note)
            lane.remove(note)
        else:
            note.getHit()

    elif noteTiming <= 106.5 and noteTiming >= -106.5: #good
        combo += 1
        scoresArray[3] = scoresArray[3] + 1
        judgement[0] = "Good"
        judgement[1] = scoresArray[9]
        if position == note.ycoord:
            notesArray.remove(note)
            lane.remove(note)
        else:
            note.getHit()

    elif noteTiming <= 130.5 and noteTiming >= -130.5: #ok
        combo += 1
        scoresArray[4] = scoresArray[4] + 1
        judgement[0] = "Ok"
        judgement[1] = scoresArray[10]
        if position == note.ycoord:
            notesArray.remove(note)
            lane.remove(note)
        else:
            note.getHit()


    elif noteTiming <= 167 or (noteTiming > 167 and type(note) is LongNote and position == note.ycoord): #miss
        combo = 0
        notesArray.remove(note)
        lane.remove(note)
        scoresArray[5] = scoresArray[5] + 1
        judgement[0] = "Miss"
        judgement[1] = scoresArray[11]



    return combo, lane, scoresArray, notesArray, judgement


def keys(eventList, combo, notesArray, lane1, lane2, lane3, lane4, scoresArray, judgement, LNcover): #function that updates receptor sprites and calls the noteHit function

    if len(lane1) > 0: #need to do this for ln
        note1 = lane1[0]
    else:
        note1 = False
    if len(lane2) > 0:
        note2 = lane2[0]
    else:
        note2 = False
    if len(lane3) > 0:
        note3 = lane3[0]
    else:
        note3 = False
    if len(lane4) > 0:
        note4 = lane4[0]
    else:
        note4 = False

    for event in eventList:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and len(lane1) > 0:

                combo, lane1, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane1, scoresArray, judgement)

            if event.key == pygame.K_x and len(lane2) > 0:

                combo, lane2, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane2, scoresArray, judgement)

            if event.key == pygame.K_PERIOD and len(lane3) > 0:

                combo, lane3, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane3, scoresArray, judgement)

            if event.key == pygame.K_SLASH and len(lane4) > 0:

                combo, lane4, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane4, scoresArray, judgement)


    keys = pygame.key.get_pressed()

################# lane 1 #################

    if keys[pygame.K_z]:
        receptor1.updateImage(1)
        if type(note1) is LongNote: #ln hold
            if note1.isHit is True and ((800 - note1.ycoord) / scrollSpeed) * (1000/framerate) >= -130.5: #checks if the ln is held down
                receptor1.updateImage(2)
                LNcover[4] = True #makes the respective LNcover True


    elif type(note1) is LongNote:
        if note1.isHit is True: #ln release
            combo, lane1, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane1, scoresArray, judgement)
        receptor1.updateImage(0)
    else:
        receptor1.updateImage(0) #release with no ln

################# lane 2 #################

    if keys[pygame.K_x]:
        receptor2.updateImage(1)
        if type(note2) is LongNote:
            if note2.isHit is True and ((800 - note2.ycoord) / scrollSpeed) * (1000/framerate) >= -130.5:
                receptor2.updateImage(2)
                LNcover[5] = True


    elif type(note2) is LongNote:
        if note2.isHit is True:
            combo, lane2, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane2, scoresArray, judgement)
        receptor2.updateImage(0)

    else:
        receptor2.updateImage(0)

################# lane 3 #################

    if keys[pygame.K_PERIOD]:
        receptor3.updateImage(1)
        if type(note3) is LongNote:
            if note3.isHit is True and ((800 - note3.ycoord) / scrollSpeed) * (1000/framerate) >= -130.5:
                receptor3.updateImage(2)
                LNcover[6] = True


    elif type(note3) is LongNote:
        if note3.isHit is True:
            combo, lane3, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane3, scoresArray, judgement)
        receptor3.updateImage(0)

    else:
        receptor3.updateImage(0)

################# lane 4 #################

    if keys[pygame.K_SLASH]:
        receptor4.updateImage(1)
        if type(note4) is LongNote:
            if note4.isHit is True and ((800 - note4.ycoord) / scrollSpeed) * (1000/framerate) >= -130.5:
                receptor4.updateImage(2)
                LNcover[7] = True


    elif type(note4) is LongNote:
        if note4.isHit is True:
            combo, lane4, scoresArray, notesArray, judgement = noteHit(combo, notesArray, lane4, scoresArray, judgement)
        receptor4.updateImage(0)

    else:
        receptor4.updateImage(0)

###################################################
    return combo, notesArray, lane1, lane2, lane3, lane4, scoresArray, judgement, LNcover

def center(image, lane): #centers an image horizontally based on its dimensions and screen size
    if lane in (1,4):
        multiplier = 1.5
    else:
        multiplier = 0.5
    if lane in (1,2):
        return ((screenWidth / 2) - (multiplier*image.get_height())) - (0.5*image.get_height()) #returns xcoord of image
    else:
        return ((screenWidth / 2) + (multiplier*image.get_height())) - (0.5*image.get_height())




def readFile(fileName, notesArray, lane1, lane2, lane3, lane4, scrollSpeed, framerate, rateMod):

    file = open(fileName, "r")
    fileList = file.readlines()#stores the whole file as an array, where each new line is a seperate index
    #noteImage = pygame.image.load(base_dir / "skin/note.png")
    for line in fileList:
        line = line.rstrip("\n")
        line = line.split(",")#makes line a list with each item being what is between each ,
        line[5] = line[5].partition(":")[0] #removes everything after the colon, the[0] is there as partition returns a tuple
        lane = int(line[0])

        if lane == 64: #1
            lane = 1
            laneList = lane1


        elif lane == 192: #2
            lane = 2
            laneList = lane2


        elif lane == 320: #3
            lane = 3
            laneList = lane3


        else: #4
            lane = 4
            laneList = lane4

        xcoord = center(noteImage, lane)
        if int(line[3]) == 128: #if its an ln then it makes the ycoord the end of the ln, this is so it can be easily blit
            ycoord = -abs(int(line[5]))

        else:
            ycoord = -abs(int(line[2]))

        ycoord /= (1000/framerate) #turning ms to ycoord
        ycoord *= scrollSpeed
        ycoord /= rateMod
        ycoord += receptor1.ycoord #this is basically to treat the receptor ycoords as 0, so the music sint offset

        # lane, xcoord, ycoord, notesArray, laneList, length    
        if int(line[3]) == 128: #if its an ln
            start = -abs(int(line[2]))
            start /= (1000/framerate)
            start *= scrollSpeed
            start /= rateMod
            start += receptor1.ycoord
            note = LongNote(lane, xcoord, ycoord, notesArray, laneList, start)
            note.makeImage()
        else:
            note = Note(lane, xcoord, ycoord, notesArray, laneList)




    file.close()

def calcAccuracy(scoresArray):
    totalScore = 0
    total = 0
    totalScore += (6 * scoresArray[0]) + (6 * scoresArray[1])
    totalScore += 4 * scoresArray[2]
    totalScore += 2 * scoresArray[3]
    totalScore += scoresArray[4]

    total = scoresArray[0] + scoresArray[1] + scoresArray[2] + scoresArray[3] + scoresArray[4] + scoresArray[5]
    total *= 6
    try:
        accuracy = (totalScore/total) * 100
    except:
        accuracy = 100
    accuracy = round(accuracy, 2)
    return accuracy


def endScreen(scoresArray, accuracy, eventList):
    screen.fill((0,0,0))
    running = True
    if accuracy >= 95:
        rank = "S"
    elif accuracy >= 90:
        rank = "A"
    elif accuracy >= 85:
        rank = "B"
    elif accuracy >= 80:
        rank = "C"
    elif accuracy >= 75:
        rank  = "D"
    else:
        rank = "F"

    rankText = font.render("Your rank: "+str(rank), False, (255,255,255))
    accuracyText = font.render("Your accuracy: "+ str(accuracy)+"%", False, (255,255,255))
    quitText = font.render("(Esc to quit)", False, (150,150,150))
    screen.blit(rankText, (400, 100))
    screen.blit(accuracyText, (400, 150))
    screen.blit(quitText, (450, 900))
    for x in range (0,6): #how many of each judgement
        counter = font.render(str(scoresArray[x+12])+": "+str(scoresArray[x]), False, scoresArray[x+6])
        #screen.blit(counter, ((1+(x%2)*300, 200+(50*x))) #300, 600
        screen.blit(counter, (450, 200+(50*x)))

    pygame.display.flip()



    while running == True:
        print("E")

        keys = pygame.key.get_pressed() #idk why this doesnt work
        if keys[pygame.K_q]:
            running = False

    return running


def make_LNcover():
    LNcover = []
    for x in range(0,4):
        surface = pygame.Surface((noteImage.get_width(), 400))
        surface.fill((0,0,0))
        LNcover.append(pygame.Surface((noteImage.get_width(), 400)))
    for x in range(4):
        LNcover.append(False)
    return LNcover


receptorImage = pygame.image.load(base_dir / "skin/hit receptor.png")
receptor1 = Receptor(center(receptorImage, 1))
receptor2 = Receptor(center(receptorImage, 2))
receptor3 = Receptor(center(receptorImage, 3))
receptor4 = Receptor(center(receptorImage, 4))


screen.blit(receptor1.image, (receptor1.xcoord, receptor1.ycoord))
screen.blit(receptor2.image, (receptor2.xcoord, receptor2.ycoord))
screen.blit(receptor3.image, (receptor3.xcoord, receptor3.ycoord))
screen.blit(receptor4.image, (receptor4.xcoord, receptor4.ycoord))



LNcover = make_LNcover()

pygame.mixer.music.load(base_dir / "songs/polyriddim.mp3")
pygame.mixer.music.set_volume(0)


running = True
clock = pygame.time.Clock()

pygame.display.flip()
readFile(base_dir / "songs/altale.txt", notesArray, lane1, lane2, lane3, lane4, scrollSpeed, framerate, rateMod)


time.sleep(2)
pygame.mixer.music.play()

while running:

    clock.tick(framerate)
    screen.fill((0,0,0))
    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False

    ########## keys ##########

    combo, notesArray, lane1, lane2, lane3, lane4, scoresArray, judgement, LNcover = keys(eventList, combo, notesArray, lane1, lane2, lane3, lane4, scoresArray, judgement, LNcover)

    ########## moving all notes down ##########

    for note in notesArray: 
        note.ycoord += scrollSpeed
        if type(note) is LongNote:
            note.start += scrollSpeed
        screen.blit(note.image, (note.xcoord, note.ycoord))

        if note.ycoord >= 800 + ((130.5/(1000/framerate)) * scrollSpeed): #miss if note isnt hit
            judgement[0] = "Miss"
            judgement[1] = (200,0,0)
            notesArray.remove(note)
            combo = 0
            scoresArray[5] = scoresArray[5] + 1
            if note.lane == 1:
                lane1.remove(note)
            elif note.lane == 2:
                lane2.remove(note)
            elif note.lane == 3:
                lane3.remove(note)
            else:
                lane4.remove(note)

    ########## LNcovers being blit ##########

    for x in range(4):
        if LNcover[x+4] == True:
            screen.blit(LNcover[x], (center(noteImage, x+1), receptor1.ycoord + (noteImage.get_height() / 2))) #will have to change this for receptor.get_height in the future
            #receptor1 is used as they are all same size
            LNcover[x+4] = False #resets the LNcover, probably inneficient to do this every time but way easier

    ########## accuracy and texts being made and blit ##########            

    accuracy = calcAccuracy(scoresArray) #this might cause lag

    comboText = font.render(str(combo), False, (255,255,255)) #combo display
    accuracyText = font.render(str(accuracy)+"%", False, (255,255,255))
    judgementText = font.render(str(judgement[0]), False, judgement[1])

    for x in range (0,6):
        counter = font.render(str(scoresArray[x]), False, scoresArray[x+6])
        screen.blit(counter, (50, 200+(50*x)))


    screen.blit(judgementText, ((screenWidth/2)-50,500))
    screen.blit(comboText, (screenWidth/2,400))
    screen.blit(accuracyText, (screenWidth-100, 100))



    screen.blit(receptor1.image, (receptor1.xcoord, receptor1.ycoord))
    screen.blit(receptor2.image, (receptor2.xcoord, receptor2.ycoord))
    screen.blit(receptor3.image, (receptor3.xcoord, receptor3.ycoord))
    screen.blit(receptor4.image, (receptor4.xcoord, receptor4.ycoord))


    pygame.display.flip()

    ########## checking if map is finished ##########

    if len(notesArray) == 0 and running == True:
        running = endScreen(scoresArray, accuracy, eventList)

pygame.quit()