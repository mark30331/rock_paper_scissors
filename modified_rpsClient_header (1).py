#############################################################################
# Program:
#    Lab PythonRPS_Client, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Mark kportufe
# Summary:
#    creates a connection to the server on the local host at the default port 6789. 
# If the connection has been successfully established the script prompts the user to
#  choose a correspondent character to (R)ock, (P)aper or (S)cissors.After sending the 
# character to the server via the TCP protocol the client waits for a reply from the 
# server and a notification will be dumped.
# Once the client receives a response from the server the message will be printed 
# to the screen and the connection will be closed.
#
##############################################################################
# Note: Take-2 header goes here
#After sending the
# character to the server via the TCP protocol the client waits for a reply from the
# server and a notification will be dumped.
# Once the client receives a response from the server the message will be printed
# to the screen and the connection will be closed.

#
# This is just a slightly modified version of the TCPClient.py code from
# section 2.7 of the book that was used in class. 
#
import sys
import os
from socket import *
serverName = 'localhost'
serverPort = 6789
# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((serverName, serverPort))

#This constitutes the players contecnt of the rock, paper, scissors game. 
def getContent():
    content = input('Rock(r), Paper(p), Scissors(s) or Quit(q) (Enter only 1 lowercase letter): ')

    while (1):
        #For simplicity, let's just allow r, p, s, or q
        # Valid input
        if ((content == "r") or (content == "p") or (content == "s") or (content == "q")):
            return content

        else:
            print("Invalid input. Please Try again.\n")


#  Since we got rid of a few initialization steps,
#  there's no need for this function
#This function is to get the feedback from the other player
def getFeedback():
    clientSocket.settimeout(30)

    try:
        feedback = clientSocket.recv(1024).decode('ascii')

        splitResponse = feedback.split('~')
        RPSPCode = splitResponse[0]
        response = splitResponse[1]

        print("From Server: ", response)

        return int(RPSPCode)
    except:
        print("\nSomething has gone wrong. Exiting Game.")
        return 2

#Don't need this function. The server should do this according to protocol
#This funcitons determines who is the real winner of the rock, paper, scissors game. 
def determineWinner(contentOne1, contentTwo2):
    # Takes both inputs, strips it down to their first letter, and uppercases it
    contentOne = contentOne1[:1].upper()
    contentTwo = contentTwo2[:1].upper()

    if (contentOne == "Q" or contentTwo == "Q"):
        # Stops the game from restarting too quickly for one or both players
        clientSocket.send("3~Continue Game".encode('ascii'))

        # 4 is the code to end the game
        return 4
    #This checks the logic of hte game. 
    else:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("You picked          :", contentOne1)
        print("Your opponent picked:", contentTwo2)

        # You picked the same thing
        if (contentOne == contentTwo):
            print("Draw")
        # You picked Rock
        elif (contentOne == 'R'):
            if (contentTwo == 'P'):
                print("You lose.")
            if (contentTwo == 'S'):
                print("You win!")
        # You picked Paper
        elif (contentOne == 'P'):
            if (contentTwo == 'S'):
                print("You lose.")
            if (contentTwo == 'R'):
                print("You win!")
        # You picked Scissors
        elif (contentOne == 'S'):
            if (contentTwo == 'R'):
                print("You lose.")
            if (contentTwo == 'P'):
                print("You win!")
        # 3 is the code to restart the game
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        # Stops the game from restarting too quickly for one or both players
        clientSocket.send("3~Continue Game".encode('ascii'))
        return 3

#This function should look very similar to my client's game loop
#This function calls the playgame. This will execute the game
def playGame():
    # # RPSPCode = Rock-Paper-Scissors Protocol Code
    # RPSPCode = getFeedback()

    # # Code 0 = Wait
    # while(RPSPCode == 0):
    #     RPSPCode = getFeedback()

    # Code 1 = Initiate Game
    # if (RPSPCode == 1):
    keepPlaying = True
    while keepPlaying:

        userInput = getContent()
        clientSocket.send(userInput.encode('ascii'))
        
        if (userInput == 'q'):
            keepPlaying = False
        
        else:
            print("Awaiting response.\n")

            #Instead of receiving the other player's token,
            #  we now expect to receive the game result
            gameResult = clientSocket.recv(1024).decode('ascii')

            
            # RPSPCode = determineWinner(messageOne, messageTwo)
            if (gameResult == 'q'):
                print("Your opponent has left the game. Exiting...")
                keepPlaying = False
            elif (gameResult == 'w'):
                print("You WON!")
            elif (gameResult == 'l'):
                print("You LOST!")
            elif (gameResult == 'd'):
                print("It's a Draw!")
            
    

#This is where connection of the sockets starts
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print("Connected to server")


connectionCode = int(clientSocket.recv(1024).decode('ascii'))

if (connectionCode != 1):
    print("Connection failed")
    sys.exit(1)
#Executes the game once the code received is 1
playGame()
clientSocket.close()