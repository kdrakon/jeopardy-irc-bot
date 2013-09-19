
import threading
import time

class GameTimer(threading.Thread):
    
    __stdout = None
    __timeout = 10
    __curAnswer = ""
    __startNextQuestionCallback = None
    __running = False
    
    def setup(self, stdout, timeout, curAnswer, startNextQuestionCallback):
        
        self.__stdout = stdout
        self.__timeout = timeout
        self.__curAnswer = curAnswer
        self.__startNextQuestionCallback = startNextQuestionCallback
    
    def run(self):
        
        self.__running = True
        time.sleep(self.__timeout)
        
        if self.__running:
            self.endGame(False)
            self.__startNextQuestionCallback(self.__stdout)
    
    def setRunning(self, running):
        
        self.__running = running
        if not running:
            self.endGame(True)
        
    def isRunning(self):
        return self.__running
        
    def endGame(self, forced):
	
        if not forced:
            self.__stdout.write("Time's up! The answer is:\n" + self.__curAnswer + "\n")
            self.__stdout.flush()
        
        self.__curAnswer = ""
