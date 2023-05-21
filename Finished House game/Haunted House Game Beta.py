import random
from datetime import datetime
import time
#import matplotlib.pyplot as plt
#import matplotlib.image as img
rooms = ["startRoom", "hallWay1Room", "gamesRoom", "livingRoom", "hauntedRoom", "hallway2Room", "finishRoom"]
roomIndex = 0
#CurrentHP = 100
verbose = True
hasWon = False
ghostKeyLivRoomTaken = False
#tipCounter= 0
ghostKeyHallW2RoomTaken = False
randomGhostRoomName = "not set"
class house():

    def __init__(self, houseName):
        self.houseName = houseName
        self.rooms = []


    def addRoom(self, roomName, roomDescription):
        newRoom = room(roomName, roomDescription)        #append object(room) to the array
        self.rooms.append(newRoom)


    def getRoom(self, roomName):
        for r in self.rooms:
            if r.getName().upper() == roomName.upper():
                return r

    def addWall(self, roomName, wallName):
        r = self.getRoom(roomName)
        r.addWall(wallName)

    def addDoor(self, roomName, wallName, connectingRoomName):
        # a door connects two walls, in this method the wall of the
        # joining room is chosen for you
        mainRoom = self.getRoom(roomName)
        connectRoom = self.getRoom(connectingRoomName)
        mainRoom.addDoor(wallName, connectRoom)


class room():
      def __init__(self, roomName, roomDescription):
          self.roomName = roomName
          self.roomDescription = roomDescription
          print(roomName,  " has been created. ", roomDescription)
          self.walls = []
          self.doorsInRoom = []

      def getName(self):
          return self.roomName

      def addWall(self, wallName):
          newWall = wall(wallName)
          self.walls.append(newWall)       # append object(wall) to the array

      def getWall(self, wallName):
          for w in self.walls:
              if w.getName().upper() == wallName.upper():
                  return w

      def getRoomDescription(self):
          return self.roomDescription

      def addDoor(self, wallName, connectingRoom):
          w = getwall(wallName)
          w.addDoor(connectingRoom)

      def addDoorToRoom(self, roomObject, connectingRoomObject):
          # assume 2 doors per room: going forwards and backwards
          newDoor = door(roomObject, connectingRoomObject)
          self.doorsInRoom.append(newDoor)

      def printDoorsInRoom(self):
          for d in self.doorsInRoom:
             print(d.room1.roomName, "to", d.room2.roomName)

class wall:
    def __init__(self, wallName):
        self.wallName = wallName
        self.doors = []

    def addDoor(self, connectingRoomObject):
        newDoor = door(connectingRoomObject)
        self.doors.append(newDoor)

    def getName(self):
        return self.wallName

class door:
    def __init__(self, roomObject, connectingRoomObject):
        self.room1 = roomObject
        self.room2 = connectingRoomObject

    def getOtherRoom(self, knownRoomObject):
    # A door connects two rooms, this sub is given a room instance
    # and returns the room this door connects to
        if knownRoomObject.getName() == self.room1.getName():
            output("Door- " + self.room2.getName())
            return self.room2   #other room object
        else:
            output("Door- " + self.room1.getName())
            return self.room1   #other room object

def setupHouse(): # call all methods and add rooms/descriptions/doors/walls
    hauntedHouse.addRoom("startRoom", "The game opening room")  #roomName,+ roomdescription
    hauntedHouse.addRoom("hallWay1Room", "hallway1Room leads to the game room")
    hauntedHouse.addRoom("gamesRoom", "Defeat the ghost to obtain a key and open the door to livingRoom")
    hauntedHouse.addRoom("livingRoom", "Leads to the haunted room")
    hauntedHouse.addRoom("hauntedRoom", "Defeat the ghost to obtain a key and open the door to hallway 2")
    hauntedHouse.addRoom("hallWay2Room", "Leads to finishRoom")
    hauntedHouse.addRoom("finishRoom", "Has a chest with a throphy + key inside to escape")
    print("\n" * 5)
    print("-----------------------------------------------------------------------------------------------------------------------------------|")
    print(" READ THE ROOM DESCRIPTIONS ABOVE TO PLAY THE GAME                                                                                 |")
    print("                                                                                                                                   |")      
    print("IN GAME INSTRUCTIONS / TIPS:                                                                                                       |")
    print("                                                                                                                                   |")
    print("1. Navigate your way through the house and reach the exit (FinishRoom) and obtain the trophy and key to escape                     |")
    print("2. Be careful as this house is haunted and ghosts may lurk around each room                                                        |")
    print("3. If your door is locked you need to look for the ghost                                                                           |")
    print("4. Once the ghost is in your room you need to use the pickup object option in the menu and vacuum the ghost up to obtain the key   |")
    print("                                                                                                                                   |")
    print(" Good Luck Reginald Augustus Chadwick III!                                                                                         |")                         
    print("-----------------------------------------------------------------------------------------------------------------------------------|")

    #*******************************************************************************************************************************

    #hauntedHouse.addWall("startRoom", "StartToGameWall")
    #hauntedHouse.addWall("gamesRoom", "StartToGameWall") # wall shared between both rooms (RoomName, Wallname)

    #hauntedHouse.addWall("startRoom", "StartToHallWay1Wall")
    #hauntedHouse.addWall("hallWay1Room", "StartToHallWay1Wall")

    #hauntedHouse.addWall("startRoom", "StartToHallWay1Wall")
    #hauntedHouse.addWall("hallWay1Room", "StartToHallWay1Wall")   #roomname , wallname

    #hauntedHouse.addWall("gamesRoom", "GameToLivingWall")
    #hauntedHouse.addWall("livingRoom", "GameToLivingWall")

    #hauntedHouse.addWall("livingRoom", "LivingToHauntedWall")
    #hauntedHouse.addWall("hauntedRoom", "LivingToHauntedWall")

    #hauntedHouse.addWall("hauntedRoom", "HauntedToHallway2Wall")
    #hauntedHouse.addWall("hauntedRoom", "HauntedToHallway2Wall")

    #**************************************************************************************************
    #hauntedHouse.addDoor("startRoom", "StartToHallWay1Wall", "StairCase", "hallWay1Room") #roomname , wall name , door name, conn room name
    startRoomObject = hauntedHouse.getRoom("startRoom")
    connectingRoomObject = hauntedHouse.getRoom("hallWay1Room")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject) #goes forward to hallWay1Room

    startRoomObject = hauntedHouse.getRoom("hallWay1Room") # goes forward to gamesRoom
    connectingRoomObject = hauntedHouse.getRoom("gamesRoom")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject)

    startRoomObject = hauntedHouse.getRoom("hallWay1Room")
    connectingRoomObject = hauntedHouse.getRoom("startRoom")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject) # goes back to startRoom

    startRoomObject = hauntedHouse.getRoom("gamesRoom")
    connectingRoomObject = hauntedHouse.getRoom("livingRoom")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject) # goes back to startRoom

    startRoomObject = hauntedHouse.getRoom("gamesRoom")
    connectingRoomObject = hauntedHouse.getRoom("hallWay1Room")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject) # goes back to startRoom

    startRoomObject = hauntedHouse.getRoom("livingRoom")
    connectingRoomObject = hauntedHouse.getRoom("gamesRoom")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject) # goes back to startRoom

    startRoomObject = hauntedHouse.getRoom("livingRoom")
    connectingRoomObject = hauntedHouse.getRoom("hauntedRoom")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject) # goes back to startRoom

    startRoomObject = hauntedHouse.getRoom("hauntedRoom")
    connectingRoomObject = hauntedHouse.getRoom("hallWay2Room")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject)

    startRoomObject = hauntedHouse.getRoom("hallWay2Room")
    connectingRoomObject = hauntedHouse.getRoom("finishRoom")
    startRoomObject.addDoorToRoom(startRoomObject, connectingRoomObject)

    #TO DO doors: !!!!!!!!!!!!!!!!!!!!!
           #hauntedRoom => hallWay2Room
           #hallWay2Room => finishRoom

class character:
    def __init__(self, characterName):
        self.roomLocation = 0       # initialised to zero/null object
        self.characterName = characterName
        self.inventory = []

    def moveRoom(self, newRoomObject):   # will place/move character to a room
        self.roomLocation = newRoomObject
        #roomIndex = roomIndex + 1   # holds number of rooms in use

    def getRoom(self):
        return self.roomLocation

    def getName(self):
        return self.characterName
#-----------------------------------
chad = character("Reginald Augustus Chadwick III")
print("_____________________________________________________")
hauntedHouse = house("Haunted House")
def main():
    global roomIndex, rooms, chad, hauntedHouse, hasWon
    setupHouse()
    greetings()

    chad.moveRoom(hauntedHouse.getRoom("startRoom"))

    # Main game loop
    while not(hasWon):
        turnMenu()

def greetings():
    global roomIndex, rooms, chad
    print("\n" * 3)
    print("-------------------------------------------------")
    print(" *** GREETINGS", chad.getName(), "***")

def turnMenu():
    global roomIndex, rooms, chad, hasWon, ghostKeyTaken, randomGhostRoomName, ghostKeyLivRoomTaken, ghostKeyHallW2RoomTaken
    print("\n" * 2)
    print("You are in the: ", chad.getRoom().getName())
    print("\n" * 2)
    print("Forward and Backward door choices:")
    print(chad.getRoom().printDoorsInRoom()) # will print names
    print("\n What would you like to do?")
    if( chad.getRoom().getName() == "hauntedRoom"):
        print("The ghost is in the current Haunted room")
    else:
        print("1 - Look for ghost")
    print("2 - Pickup Object")
    print("3 - Move to next room")
    print("4 - Move back to previous room")
    print("5 - Global House Map")
    choice = input("Enter option >")

    if choice == "1":
        print("\n" * 15)
        print("You are in the", chad.getRoom().getName())
        print("Current room: ", chad.getRoom().getRoomDescription())
        ghostRoomIndex = random.randint(1,4)
        randomGhostRoomName = rooms[ghostRoomIndex]
        print("Ghost is now in room: ", randomGhostRoomName)

    if choice == "2":
        print("Pickup object:")
        if (chad.getRoom().getName() == "hallWay1Room" or
            chad.getRoom().getName() == "gamesRoom" or
            chad.getRoom().getName() == "livingRoom"):
            print("Objects to pick up:")
            print("1 - Exit Key: NOT AVAILABLE")
            if (chad.getRoom().getName() == randomGhostRoomName):
               print("2 - Vacuum gun: URGENT ACTION NEEDED !!!")
               choice = input("Enter option >")
               if choice == "2":
                   ghostKeyLivRoomTaken = True
                   print("SUCCESS: Vacuum sucked the ghost, you have the Ghost key for the Living room")
        elif (chad.getRoom().getName() == "hauntedRoom"):
              print("Objects to pick up:")
              print("1 - Exit Key: NOT AVAILABLE")
              print("2 - Vacuum gun: URGENT ACTION NEEDED !!!")
              choice = input("Enter option >")
              if choice == "2":
                 ghostKeyHallW2RoomTaken = True
                 print("SUCCESS: Vacuum sucked the ghost, you have the Ghost key for the hallWay2Room room")

                 if choice == "3":
                    choice = input("Enter option >")
                    print(" You have now gained +50Hp your current HP =")
            
                           
                      
                    

                   
        elif (chad.getRoom().getName() == "hauntedRoom"):
              print("Objects to pick up:")
              print("1 - Exit Key: NOT AVAILABLE")
              print("2 - Vacuum gun: URGENT ACTION NEEDED !!!")
              print("3 - Healing Potion - URGENT")
              choice = input("Enter option >")
              if choice == "2":
                 ghostKeyHallW2RoomTaken = True
                 print("SUCCESS: Vacuum sucked the ghost, you have the Ghost key for the hallWay2Room room")
              if choice == "3":
                  print(" You have now healed and your have gained 50 hitpoints - Current HP 100/100")
        elif (chad.getRoom().getName() == "finishRoom"):
              print("Objects to pick up:")
              print("1 - Chest Trophy and key to exit")
              choice = input("Enter option >")
              if choice == "1":
                 print("FINAL SUCCESS: You have the Chest Trophy and key to exit")
                 print("FINAL SUCCESS: You have won the game")
                 print("\n" * 2)

                 print("                                                        ")
                 print("      Reginald Augustus Chadwick III has escaped....    ")
                 print("                                                        ")                                                  
                 print("                                        _               ")                                                       
                 print("         ___ ___  _ __   __ _ _ __ __ _| |_ ___         ")
                 print("        / __/ _ \| '_ \ / _` | '__/ _` | __ / __|       ")
                 print("       | (_| (_) | | | | (_| | | | (_| | |_\__ \        ")
                 print("        \___\___/|_| |_|\__, |_|  \__,_|\__|___/        ")
                 print("                         _ / |                          ")
                 print("                        |____/                          ")
                 print("                                                        ")
                 print("                                     ghost Key          ")                     
                 print("                 Trophy                                 ")
                 print("               ___________           .--.               ")
                 print("              '._==_==_=_.'         /.-. '----------.   ")
                 print("              .-\:      /-.         \'-' .--'--''-'-'   ")
                 print("             | (|:.     |) |         '--'               ")
                 print("              '-|:.     |-'                             ")
                 print("                \::.    /                               ")
                 print("                 '::. .'                                ")         
                 print("                   ) (                                  ")
                 print("                 _.' '._                                ")
                 print("                `-------`                               ")
                 print("                                                        ")
                 print("                                                        ")
                 print("         Developed By: Michael Kalaydjiyski             ")                                  
                
                 
                 hasWon = True
    if choice == "3":
        print("\n" * 15)
        print("Moving forward:")
        if (chad.getRoom().getName() == "startRoom"):
           chad.moveRoom(hauntedHouse.getRoom("hallWay1Room"))
        elif (chad.getRoom().getName() == "hallWay1Room"):
           chad.moveRoom(hauntedHouse.getRoom("gamesRoom"))
           
        elif (chad.getRoom().getName() == "gamesRoom"):
           if (ghostKeyLivRoomTaken == True):
              print("SUCCESS: You have the key to livingRoom")
              chad.moveRoom(hauntedHouse.getRoom("livingRoom"))
           else:
              #tipCounter += 1
              print("livingRoom is locked, please take the ghost Key for livingRoom")
              tips = input(" Would you like help completing Room? Yes/No" )
              if tips == "No":
                    print("Good Luck Reginald Augustus Chadwick III")
                    print("\n" * 2)
              else:
                   tips == "Yes"
                   print("\n" * 2)
                   print("IN GAME TIP!: ")
                   print("To defeat the ghost and obtain the key you need to find it first")
                   print("Try pressing the (1 - look for ghost) until the ghost is in the same room as you.")
                   print("Once the ghost is in the same room press(2- pickup object) and select the vacuum.")
                   print("\n" * 2)
                     
        elif(chad.getRoom().getName() == "livingRoom"):
           chad.moveRoom(hauntedHouse.getRoom("hauntedRoom"))
        elif(chad.getRoom().getName() == "hauntedRoom"):
           if (ghostKeyHallW2RoomTaken == True):
              print("SUCCESS: You have the key to hallway2Room")
              chad.moveRoom(hauntedHouse.getRoom("hallWay2Room"))
           else:
              print("hallWay2Room is locked, please take the ghost Key for hallWay2Room")
              #tipCounter += 1
              tips = input(" Would you like help completing Room? Yes/No" )
              if tips == "No":
                    print("Good Luck Reginald Augustus Chadwick III")
                    print("\n" * 2)
              else:
                   tips == "Yes"
                   print("\n" * 2)
                   print("IN GAME TIP!: ")
                   print("To defeat the ghost and obtain the key you need to find it first")
                   print("Try pressing the (1 - look for ghost) until the ghost is in the same room as you.")
                   print("Once the ghost is in the same room press(2- pickup object) and select the vacuum.")
                   print("\n" * 2)
              
        elif(chad.getRoom().getName() == "hallWay2Room"):
           chad.moveRoom(hauntedHouse.getRoom("finishRoom"))
        print("You entered", chad.getRoom().getName())
        print("Current room: ", chad.getRoom().getRoomDescription())
    if choice == "4":
        print("Moving backward:")
        if (chad.getRoom().getName() == "hallWay1Room"):
           chad.moveRoom(hauntedHouse.getRoom("startRoom"))
        elif (chad.getRoom().getName() == "gamesRoom"):
           chad.moveRoom(hauntedHouse.getRoom("hallWay1Room"))
        elif (chad.getRoom().getName() == "livingRoom"):
              chad.moveRoom(hauntedHouse.getRoom("gamesRoom"))
        elif(chad.getRoom().getName() == "hauntedRoom"):
           chad.moveRoom(hauntedHouse.getRoom("livingRoom"))
        elif(chad.getRoom().getName() == "hallWay2Room"):
           chad.moveRoom(hauntedHouse.getRoom("hauntedRoom")) ### to do: in hallway2Room

    if choice == "5":

       print("==============================")
       if (chad.getRoom().getName() == "startRoom"):
           f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\startroom.txt", "br")
           print("Map is loading........")
           print("\n" * 2)
           print("-------------|    |----------------------|")
           print("|           Entrance                     |")
           print("|            |    |                      |")
           print("|            |    |                      |")
           print("|            |    |                      |")
           print("|            |    |                      |")
           print("|           staircase                    |")                ## WORKING IN v17
           print("|            |    |   Room == startRoom  |")
           print("|            |    |                      |")
           print("|            |    |                      |")
           print("|            |    |                      |")
           print("|        hallwayroom1 door               |")
           print("|------------|    |----------------------|")

       if (chad.getRoom().getName() == "hallway1Room"):
           f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\hallway1room.txt", "br")

           print("Map is loading........")
           print("\n" * 2)
           print("|                                        |")
           print("|                                        |")
           print("|   CHADWICK III                          |")            
           print("|                                        |")              ## bugged in v17
           print("|   Room == hallway1Room                 |")
           print("|                         gamesRoom door |")
           print("|--------------------------------|  |----|")

       if (chad.getRoom().getName() == "gamesRoom"):
           f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\Gamesroom.txt", "br")
           print("Map is loading........")
           print("\n" * 2)
           print("|----------------------------------------|")
           print("|      couch          G - GHOST          |")
           print("|      (--)                              |")
           print("|      (--)    /  \ pool table           |")
           print("|              \  /                      |")           ## Working IN v17
           print("|                                        |")
           print("|                                        |")
           print("|   Locked door       Room ==  gamesRoom |")
           print("|-------|\/|-----------------------------|")

       if (chad.getRoom().getName() == "livingRoom"):
          f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\Livingroom.txt", "br")
          print("Map is loading........")
          print("\n" * 2)
          print("|----------------------------------------|")
          print("|     ___                                |")
          print("|    (---)                   couch       |")
          print("|    (---) -- bookshelf      (--)        |")
          print("|    (---)                   (--)        |")
          print("|    {+++}                               |")
          print("|                                        |")            ## Working in v17
          print("|                                        |")
          print("| Room == livingRoom                     |")
          print("|                                        |")
          print("|                                        |")
          print("|                                        |")
          print("|                                        |")
          print("| hauntedRoom door                       |")
          print("|------|    |----------------------------|")

       if (chad.getRoom().getName() == "hauntedRoom"):
          f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\Hauntedroom.txt", "br")
          print("Map is loading........")
          print("\n" * 2)
          print("|                                        |")
          print("|  broken couch                  witch   |")
          print("|      ( ./--)                   _/\_    |")
          print("|       (-./-)                    ('>    |")
          print("|                                /^|     |")
          print("|                          -=>--/__|m--- |")
          print("|                                ^^      |")
          print("|                                        |")             ## Working in v17
          print("| Room == Haunted room                   |")
          print("|                       ,' ',  ,' ',     |")
          print("|                    .,,|RIP|,.|RIP|     |")
          print("|                                        |")
          print("|                         Graves         |")
          print("| hallWay2Room door                      |")
          print("|------|    |----------------------------|")

       if (chad.getRoom().getName() == "hallWay2Room"):
          f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\hallWay2Room.txt", "br")
          print("Map is loading........")
          print("\n" * 2)
          print("|                                        |")
          print("|                           cauldron     |")
          print("|                           | |  |       |")
          print("|                            *..*        |")
          print("|                             _:_        |")
          print("|  CHADWICK III              (   )       |")      ## working in v17
          print("|                             ) (        |")
          print("|     Room == hallWay2Room               |")
          print("|                                        |")
          print("|                                        |")
          print("|                    Finish room door    |")
          print("|-------------------------------|  |-----|")

       if (chad.getRoom().getName() == "finishRoom"):
          f = open("C:\michael\Cirencester College summer task 2021\EXP.WORK\security\OO WORK\Haunted House Task\Finished House game\finishRoom.txt", "br")
          print("Map is loading........")
          print("hleebe")
          print("\n" * 2)
          print("|                        CHADWICK III    |")
          print("|                                        |")
          print("|    Game winning chest:                 |")
          print("|                                        |")
          print("|         __________                     |")
          print("|        /\____;;___\                    |")
          print("|        | / Trophy  /                   |")
          print("|        `. ())oo() .|                   |")
          print("|        |\(%()*^^()^\                   |")
          print("|     %| |-%----------|                  |")
          print("|    % \ | %  EXIT    |                  |")            ## Bugged in v17
          print("|    %  \|%___KEY_____|                  |")
          print("|                                        |")
          print("|                                        |")
          print("|        Room == finishRoom              |")
          print("|                                        |")
          print("|                                        |")
          print("|                                        |")
          print("|                                        |")
          print("|                                        |")
          print("|                         LOCKED         |")
          print("|                    HAUNTEDHOUSE EXIT!! |")
          print("|-------------------------------|/ \|----|")


                     
main()
