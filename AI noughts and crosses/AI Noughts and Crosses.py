#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      micha
#
# Created:     19/10/2021
# Copyright:   (c) micha 2021
# Licence:     <your licence>
# Code version 5
#-------------------------------------------------------------------------------
import random
board = 0
row  = 0
column = 0
winner = "tie"
firstRandom = True

board =[["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

def displayBoard():
    #print(board)
    for i in range(len(board)):
     print (board[i])
     for i in range(len(board)):
       if i == 9:
        print("No winner, Tie")
    for j in [board]:
     if j == "-":
        return True
        print("No winner, Tie")

def Turn(): #OLD to delete
  playerOne = True  #Boolean = true if its player one's turn
  while True: # may check later: moves < 9
    if playerOne:
       print("Player one turn")
       ValidateRowsColumns()#input and validate rows and cols
       displayBoard()
       if board [row][column] == '-':  # space is empty
          board [row][column] = 'X'
          print("Space taken by Player one:")
          displayBoard()
          playerOne = not playerOne  # flip true to false
    else:# playerOne is false, we are playerTwo
       print ("Player two turn")
       ValidateRowsColumns()#input and validate rows and cols
       displayBoard()
       if board[row][column] == '-':  # space is empty
          board[row][column] = 'O'
          print("Space taken by Player two:")
          playerOne = not playerOne  # flip false to true
          if (i == 9):
           print("No winner, Tie")
def gameSign():

 gamesign = input("Choose Between Noughts or Crosses")

 if gamesign =='Crosses':

       print("PlayerOne has selected Crosses")
 elif gamesign == 'Noughts':

  print("PlayerOne has selected Noughts")

 else:
  print("Invalid Choice")


def ValidateRowsColumns():
    global row, column
    valid = False

    while not(valid):
         row_str = input("Please choose an existing row from 1-3")
         column_str = input("Please choose an existing column from 1-3")

         if row_str.isnumeric():
           if column_str.isnumeric():

             row = int(row_str)
             column = int(column_str)
             row = row - 1
             column = column - 1

             if (row >= 0) and (row <= 2):
               if (column >= 0) and (column <= 2):
                   valid = True

def ValidateRowsColumns_Computer():
    global row, column
    valid = False

    while not(valid):
         row =    random.randint(0,2)
         column = random.randint(0,2)
         print("row and column generated")
         if (row >= 0) and (row <= 2):
            if (column >= 0) and (column <= 2):
               valid = True

def isWin():
    global winner
    global board
    #check rows, columns and diagonals for player one:
    for i in range(3):
      if ( board[i][0] == board[i][1] == board[i][2] == 'X' ):
        winner = "Player one"
        return True

    for j in range(3):
      if ( board[0][j] == board[1][j] == board[2][j] == 'X' ):
        winner = "Player one"
        return True

    if ( board[0][0] == board[1][1] == board[2][2] == 'X' or \
         board[0][2] == board[1][1] == board[2][0] == 'X' ):
       winner = "Player one"
       return True

    #check rows, columns ad diagonals for player two:
    for i in range(3):
      if ( board[i][0] == board[i][1] == board[i][2] == 'O' ):
        winner = "Player two"
        return True

    for j in range(3):
      if ( board[0][j] == board[1][j] == board[2][j] == 'O' ):
        winner = "Player two"
        return True

    if ( board[0][0] == board[1][1] == board[2][2] == 'O' or \
         board[0][2] == board[1][1] == board[2][0] =='O' ):
       winner = "Player two"
       return True


    if (i == 9):
     print("No winner, Tie")
    # winner not found:
    return False

# --------------------------
def Game():
 global board
 global winner
 global row, column
 global firstRandom
 i=0
 playerOne = True
 while (isWin()==False) and (i < 9):
    if playerOne:
       print("Player one computer turn")
       if (firstRandom):
         ValidateRowsColumns_Computer() # use random input and validate it
         firstRandom = False
       else:
         selected = False
         for i in range(3):  # for all 3 rows, row=0,1,2
           if board[i] == ["-", "O", "O"]:     # -OO
              # select -
              row = i
              column = 0
              selected = True

         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["X", "-", "-"], ["-", "-", "-"], ["-", "-", "X"]]:
               firstRandom = False
               board[2][2] = 'X'
               print("GG WP")
               selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["X", "-", "X"], ["-", "-", "-"], ["-", "-", "-"]]:
                firstRandom = False
                board[1][2] = 'X'
                print("GG WP")
                selected = True

         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "X", "X"], ["-", "-", "-"], ["-", "-", "-"]]:
                firstRandom = False
                board[1][1] = 'X'
                print("GG WP")
                selected = True

         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["X", "X", ""], ["-", "-", "-"], ["-", "-", "-"]]:
                firstRandom = False
                board[1][3] = 'X'
                print("GG WP")
                selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "-", "-"], ["-", "-", "X"], ["-", "-", "X"]]:
                firstRandom = False
                board[1][3] = 'X'
                print("GG WP")
                selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "-", "-"], ["-", "-", "-"], ["X", "-", "X"]]:
               firstRandom = False
               board[3][2] = 'X'
               print("GG WP")
               selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "X", "-"], ["-", "-", "-"], ["-", "X", "-"]]:
                firstRandom = False
                board[2][2] = 'X'
                print("GG WP")
                selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "-", "-"], ["-", "X", "-"], ["-", "X", "-"]]:
                firstRandom = False
                board[1][2] = 'X'
                print("GG WP")
                selected = True

         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["X", "-", "-"], ["-", "X", "-"], ["-", "-", "-"]]:
                firstRandom = False
                board[3][2] = 'X'
                print("GG WP")
                selected = True





         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "-", "-"], ["-", "X", "-"], ["-", "-", "X"]]:
                firstRandom = False
                board[1][1] = 'X'
                print("GG WP")
                selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "X", "-"], ["-", "X", "-"], ["-", "-", "X"]]:
                firstRandom = False
                board[3][2] = 'X'
                print("GG WP")
                selected = True



         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "-", "-"], ["-", "X", "-"], ["-", "-", "X"]]:
                firstRandom = False
                board[1][1] = 'X'
                print("GG WP")
                selected = True



















         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
            if board[i] == [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]:
                # select -
               selected = True
            if (i == 9):
               return False
               print("There is no winner")

         if (selected == False):
           ValidateRowsColumns_Computer() # use random input and validate it

         displayBoard()
         if board [row][column] == '-':  # space is empty
            board [row][column] = 'X'
            print("Space taken by Player one Computer:")
            displayBoard()
            playerOne = not playerOne  # flip true to false
         else: # space occupied, this selection should not count
            i = i - 1  # this will keep i unchanged if space occupied
    else:# playerOne is false, we are playerTwo
       print ("Player two turn")
       ValidateRowsColumns() #input and validate rows and cols
       displayBoard()
       if board[row][column] == '-':  # space is empty
          board[row][column] = 'O'
          print("Space taken by Player two:")
          displayBoard()
          playerOne = not playerOne  # flip false to tru
       else: # space occupied, this selection should not count
          i = i - 1  # this will keep i unchanged if space occupied
    if( isWin() ):
      print("Winner is", winner)
    else:
      i = i + 1
 #if (i == 9):
    #print("No winner, Tie")

# winner not found:
 return False



def Gamewin():

 global board
 global winner
 global row, column
 global firstRandom
 i=0
 playerOne = True
 while (isWin()==False) and (i < 9):
    if playerOne:
       print("Player one computer turn")
       if (firstRandom):
         ValidateRowsColumns_Computer() # use random input and validate it
         firstRandom = False
       else:
         selected = False
         for i in range(3):  # for all 3 rows, row=0,1,2
           if board[i] == ["-", "0", "0"]:     # -xx
              # select -
              row = i
              column = 0
              selected = True
         selected = False
         for i in range(3):  # for all 3 rows, row=0,1,2
           if board[i] == [["X", "-", "-"], ["X", "-", "-"]]:      # -OO
              # select -
            row = 1
            column = 3
            selected = True
         #[["-", "-", "X"], ["-", "X", "-"], ["X", "-", "-"]]  <-- Diagonal win


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
             if board[i] == [["-", "-", "X"], ["-", "X", "-"]]:     # x-x
                # select -
                row = 1
                column = 3
                selected = True


         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
             if board[i] == [["-", "X", "-"], ["-", "X", "-"]]:     # x-x
                # select -
                row = 2
                column = 3
                selected = True

         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
             if board[i] == ["X", "-", "-"]:     # x-x
                # select -
                row = 2
                column = 2
                selected = True

         if (selected == False):
           for i in range(3):  # for all 3 rows, row=0,1,2
             if board[i] == ["X", "X", "-"]:     # OO-
                # select -
                row = i
                column = 2
                selected = True

         if (selected == False):
           ValidateRowsColumns_Computer() # use random input and validate it

         displayBoard()
         if board [row][column] == '-':  # space is empty
            board [row][column] = 'X'
            print("Space taken by Player one Computer:")
            displayBoard()
            playerOne = not playerOne  # flip true to false
         else: # space occupied, this selection should not count
            i = i - 1  # this will keep i unchanged if space occupied
    else:# playerOne is false, we are playerTwo
       print ("Player two turn")
       ValidateRowsColumns() #input and validate rows and cols
       displayBoard()
       if board[row][column] == '-':  # space is empty
          board[row][column] = 'X'
          print("Space taken by Player two:")
          displayBoard()
          playerOne = not playerOne  # flip false to tru
       else: # space occupied, this selection should not count
          i = i - 1  # this will keep i unchanged if space occupied
    if( isWin() ):
      print("Winner is", winner)
    else:
      i = i + 1
 if (i == 9):
    print("No winner, Tie")
    return False





def Main():
 print("Welcome to Noughts and Crosses ")
 displayBoard()





def Main():
 print("Welcome to Noughts and Crosses ")
 displayBoard()
 Game()
 Gamewin()
Main()











