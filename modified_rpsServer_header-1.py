#############################################################################
# Program:
#    Lab PythonRPS_Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Mark Kportufe
# Summary:
#    A rock paper scissors game between a client and a server. 
#
#
#*****************************************************************************
#
# RPS (rock/paper/scissors) Protocol 
# By executing the server the user will be prompt to specify a port number which has to 
# be an integer value strictly greater than zero.  After submitting the script runs a little 
# validation and checks if the value is within the defined range and sets the port value.
# The server accepts an input stream from both clients. Once the players have sent their packets, 
# the program computes a result based on the user inputs (R – rock , S – scissors , P - paper ) 
# and the following rule set. Rock beats scissors, scissors beats paper, paper beats rock.
# ----------------------------------------------
#
#
##############################################################################
# Note: Take-2 header goes here
#The server accepts an input stream from both clients. Once the players have sent their packets,
# the program computes a result based on the user inputs (R – rock , S – scissors , P - paper )
# and the following rule set. Rock beats scissors, scissors beats paper, paper beats rock.
# ----------------------------------------------
#
# This is just a slightly modified version of the TCPServer.py code from
# section 2.7 of the book that was used in class. 
#
import sys
from socket import *
import random

DEFAULT_VALUE = 6789

serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_VALUE

# serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.bind(('', serverPort))
# serverSocket.listen(1)
# serverSocket.accept()
print('The Server is ready to receive')


#This function ensures that the players(clients) connect smoothly and checks for any erros. 

def connectPlayers(serverSocket, playerOneSocket, secondsToBreak=30, timeout=10):
   # serverSocket.settimeout(timeout)

   # See "RPS Protocol code" above for reason for '0'
   # waitMessage = "0"
   # playerOneSocket.send(waitMessage.encode('ascii'))

   try:

      playerTwoSocket, addr = serverSocket.accept()

      # playerTwoMessage = playerTwoSocket.recv(1024).decode('ascii')

      # serverSocket.settimeout(None)

      # print(playerTwoMessage)

      return playerTwoSocket

   except:
      if secondsToBreak <= timeout:
         print("Could not find a match for the client.")
         playerOneSocket.send(
             "2~Could not find another player.\n".encode('ascii'))
         playerOneSocket.close()
         return
      else:
         connectPlayers(serverSocket, playerOneSocket,
                        secondsToBreak - timeout, timeout)

   serverSocket.settimeout(None)
   return 0

rps = {
    'r' : 0,
    'p' : 1,
    's' : 2
}

def resolveResultTokens(token1, token2):
    # If any of the players return 'q', then quit:
    if token1 == 'q' or token2 == 'q':
        return ('q', 'q')
    
    # If 2 tokens are the same, it's a draw:
    elif (token1 == token2):
        return ('d', 'd')
    
    # If 2 tokens are different and no one quit, calculate
    #   result using game logic
    else:
        # If token2 is right after token1 in the dictionary,
        #    then player 1 lost, player 2 won
        # ...and vice versa
        if (rps[token1] + 1) % len(rps) == rps[token2]:
            return ('l', 'w')
        else:
            return ('w', 'l')

#This fuctions officially starts the game in the server 
def startGame(playerOneSocket, playerTwoSocket):
   print(1)
   # Get the message from both players
   playerOneMessage = playerOneSocket.recv(1024).decode('ascii')
   playerTwoMessage = playerTwoSocket.recv(1024).decode('ascii')

   result = resolveResultTokens(playerOneMessage, playerTwoMessage)
   # Send the message to the other player (Game logic happens at the client)
   playerOneSocket.send(result[0].encode('ascii'))
   playerTwoSocket.send(result[1].encode('ascii'))

   return result


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


try:
   while 1:
      playerOneSocket, addr = serverSocket.accept()

      # Wait for the second player to join
      print("Searching for another client")
      playerTwoSocket = connectPlayers(serverSocket, playerOneSocket)
      
      print("got here!")

      # If another player has connected (I didn't want to put this in the while loop below)
      if (playerTwoSocket != 0):
         playerOneSocket.send("1".encode('ascii'))
         playerTwoSocket.send("1".encode('ascii'))
      else:
         # If another player has not connected
         print("Could not find another player.")
         print("Disconnecting from original client.\n")

      # If another player has connected
      keepPlaying = True
      while (keepPlaying):
         try:
            result = startGame(playerOneSocket, playerTwoSocket)
            if (result[0] == 'q' or result[1] == 'q'):
               keepPlaying = False
            print(2)

         except:
            print("A client has disconnected.\n")
            break

      playerOneSocket.close()
      playerTwoSocket.close()

except KeyboardInterrupt:
   print("\nClosing Server")
   serverSocket.close()







