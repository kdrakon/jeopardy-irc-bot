#!/usr/bin/python

from TriviaBot import TriviaBot
from IrcClient import IrcClient
import threading
import time

bot = TriviaBot(IrcClient("irc.teksavvy.ca"))
bot.start()    
