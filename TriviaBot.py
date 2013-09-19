
import threading
from IrcClient import IrcClient
from TriviaGame import TriviaGame
from GameTimer import GameTimer
from AnswerChecker import AnswerChecker
import time

# settings
commandPrefix = '%'
roundTime = 10

class TriviaBot(threading.Thread):

    __ircClient = False
    __ircStdout = False
    __clientGame = False
    __curCategory = ""
    __curQuestion = ""
    __curAnswer = ""
    __gameTimer = False
    
    def __init__(self, ircClient):
        self.__ircClient = ircClient
        self.__ircStdout = ircClient.getStdout()
        
    def run(self):
        
        while True:
            line = ircClient.readClient()
            self.reason(line, self.__ircStdout)

    def reason(self, readLine, stdout):
        
        if self.checkAnswer(readLine):
            stdout.write("correct!")
            stdout.flush()
            return
        
        command = self.isCommand(readLine)
        if (command == 'newgame'):
            self.startNewGame(stdout)
        
        elif (command == 'repeat'):
            if len(self.__curQuestion) > 0:
                stdout.write(self.__curQuestion)
                stdout.flush()
                
        elif (command == 'channel'):
            self.__ircClient.joinChannel("jtest")
                
    def checkAnswer(self, readLine):
        
        if len(self.__curAnswer) == 0:
            return False
        
        answerChecker = AnswerChecker()
        return answerChecker.check(readLine, self.__curAnswer)

    def isCommand(self, readLine):
        
        readLine = readLine.strip().lower()
        
        if len(readLine) <= 0:
			return False
        
        if (readLine[0] == commandPrefix):
            command = str(readLine[1:len(readLine)])
            return command
        else:
            return False

    def startNewGame(self, stdout):
        
        if self.__gameTimer:
            self.__gameTimer.setRunning(False)
        
        self.__clientGame = TriviaGame()
        while not self.__clientGame.isReady():
            # wait
            time.sleep(1)
            
        nextQuestion = self.getNextQuestion()
        if nextQuestion:
            stdout.write("New game ready!\n")
            stdout.write(nextQuestion)
            stdout.flush()    
            self.startNewGameTimer(stdout)
        
    def startNextQuestion(self, stdout):
        
        if self.__gameTimer.isRunning():
            nextQuestion = self.getNextQuestion()
            if nextQuestion:
                stdout.write(nextQuestion)
                stdout.flush()
                self.startNewGameTimer(stdout)
            else:
                self.__curQuestion = "No more questions! Please start a new game.\n"
                stdout.write(self.__curQuestion)
                stdout.flush()

    def getNextQuestion(self):
        
        response = ""
        
        newTrivia = self.__clientGame.getRandomTrivia()
        
        if not newTrivia:
            # have to start a new game
            return False
        
        self.__curCategory = newTrivia[0]
        self.__curQuestion = newTrivia[1]
        self.__curAnswer = newTrivia[2]
        
        response += "The category is: " + self.__curCategory + "\n"
        response += self.__curQuestion + "\n"
        
        return response
        
    def startNewGameTimer(self, stdout):
        
        self.__gameTimer = GameTimer()
        self.__gameTimer.setup(stdout, roundTime, self.__curAnswer, self.startNextQuestion)
        self.__gameTimer.start()
