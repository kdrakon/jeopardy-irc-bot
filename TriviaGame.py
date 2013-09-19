
import random
import subprocess
import lxml.html as html
import lxml.etree as etree
import urllib2
import re
import time

# settings
resourceUrl = 'http://www.j-archive.com/showgame.php?game_id='
lastEpisode = 4287
questionPattern = re.compile("'clue_D?J_(.+)_.+', 'clue_.*', '(.+)'")
answerPattern = re.compile('<em class="correct_response">(.+)</em>')

class TriviaGame:
    
    __game = None
    
    def __init__(self):
        self.__game = self.getRandomTriviaGame()
        
    def isReady(self):
        return self.__game != False
    
    def getRandomTrivia(self):
        
        if len(self.__game) <= 0:
            #no more trivia
            return False
        
        random.seed()
        questionNum = random.randint(0, len(self.__game) - 1)
        try:
            trivia = self.__game[questionNum]
            del self.__game[questionNum]
            return trivia
        except:
            return getRandomTrivia()
    
    def getRandomTriviaGame(self):
        
        episodeNum = self.generateEpisodeNum()
        page = self.getWebpage(resourceUrl + str(episodeNum))
        while not page:
            time.sleep(5)
            print "trying again..."
            episodeNum = self.generateEpisodeNum()
            page = self.getWebpage(resourceUrl + str(episodeNum))
        
        categories = self.parseCategoryNames(page)
        triviaGame = self.parseRandomTrivia(page, categories)
        
        return triviaGame
        
    def generateEpisodeNum(self):
        
        random.seed()
        return random.randint(1, lastEpisode)    
        
    def getWebpage(self, url):
        
        pageCon = urllib2.urlopen(url)
        try:
            page = pageCon.read().decode('utf-8')
            pageCon.close()
            return page
            
        except UnicodeDecodeError:
            return False
        
    def parseCategoryNames(self, page):
        
        pageTree = html.document_fromstring(page)
        categories = pageTree.xpath('//div[@id="jeopardy_round"]//td[@class="category_name"]')
        
        categoriesList = list()
        for category in categories:
            categoriesList.append(category.text_content())
            
        return categoriesList
        
    def parseRandomTrivia(self, page, categories):
        
        pageTree = html.document_fromstring(page)
        trivias = pageTree.xpath('//td[@class="clue"]/table//div')    
        
        triviaList = list()
        for trivia in trivias:
            triviaTriple = self.parseQuestion(trivia, categories)
            triviaTriple.append(self.parseAnswer(trivia))
            triviaList.append(triviaTriple)
            
        return triviaList

    def parseQuestion(self, trivia, categories):

        questionMatch = questionPattern.findall(trivia.attrib['onmouseout'])
        if (questionMatch):
            categoryNum = questionMatch[0][0]
            category = categories[int(categoryNum) - 1]
            question = questionMatch[0][1]
        else:
            category = "?"
            question = "?"
            
        return [category, question]

    def parseAnswer(self, trivia):
        
        answerMatch = answerPattern.findall(trivia.attrib['onmouseover'])
        if (answerMatch):
            answer = answerMatch[0]
        else:
            answer = "?"
            
        return answer
