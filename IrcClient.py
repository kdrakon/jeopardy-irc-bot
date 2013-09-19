# based on code referenced from http://thomasfischer.biz/?p=633

import socket

class IrcClient:
    
    __sock = socket.socket()
    __sockFile = False
    
    def __init__(self, server, port=6667, nick="jt8945"):
        
        print server + ":" + str(port)
        self.__sock.connect((server, port))
        self.__sock.send("NICK " + nick + "\r\n")
        self.__sock.send("USER F00bar F00bar F00bar :F00bar\r\n")
       
        self.__sockFile = self.__sock.makefile('r', 4096)
    
    def readClient(self):
        
        line = self.__sockFile.readline().strip()
        if line.find('PING') != -1:
            print "GOT PING!"
            self.__sock.send('PONG :' + line.split(':')[1])
            return self.readClient()
        else:
            return line
    
    def joinChannel(self, channel):
		print "JOINING CHANNEL!"
		self.__sock.send("JOIN " + channel + "\r\n")
		self.__channel = channel
    
    def getStdout(self):        
        return self.__sockFile
