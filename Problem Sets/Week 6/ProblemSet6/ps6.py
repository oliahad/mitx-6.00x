# 6.00x Problem Set 6
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


#-----------------------------------------------------------------------
#
# Problem Set 6

#======================
# Code for retrieving and parsing RSS feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret
#======================

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self,guid, title, subject, summary, link):
        self.guid=guid
        self.title=title
        self.subject=subject
        self.summary=summary
        self.link=link
    def getGuid(self):
        return self.guid
    def getTitle(self):
        return self.title
    def getSubject(self):
        return self.subject
    def getSummary(self):
        return self.summary
    def getLink(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self,word):
        Trigger.__init__(self)
        self.word=word.lower()

    def isWordin(self,text):
        self.text=text.lower()
        for s in string.punctuation:
            self.text=self.text.replace(s,' ')
        return self.word in self.text.split(' ')
        

class TitleTrigger(WordTrigger):     
    #def __init__(self,word):
        #WordTrigger.__init__(self,word)

    def evaluate(self,news):
        return self.isWordin(news.getTitle())
        
class SubjectTrigger(WordTrigger):
    #def __init__(self,word):
        #WordTrigger.__init__(self,word)

    def evaluate(self,news):
        return self.isWordin(news.getSubject())

class SummaryTrigger(WordTrigger):
    #def __init__(self,word):
        #WordTrigger.__init__(self,word)

    def evaluate(self,news):
        return self.isWordin(news.getSummary())


# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self,T):
        self.T=T
        Trigger.__init__(self)

    def evaluate(self,news):
        return not(self.T.evaluate(news))
        
class AndTrigger(Trigger):
    def __init__(self,T1,T2):
        self.T1=T1
        self.T2=T2
        Trigger.__init__(self)

    def evaluate(self,news):
        return self.T1.evaluate(news) and self.T2.evaluate(news)

class OrTrigger(Trigger):
    def __init__(self,T1,T2):
        self.T1=T1
        self.T2=T2
        Trigger.__init__(self)

    def evaluate(self,news):
        return self.T1.evaluate(news) or self.T2.evaluate(news)

# Question 9

class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.phrase=phrase

    def isPhrasein(self,text):
        self.text=text
        return self.phrase in self.text

    def evaluate(self,news):
        return self.isPhrasein(news.getTitle()) or self.isPhrasein(news.getSubject()) or self.isPhrasein(news.getSummary())




#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    res=[]
    for trigger in triggerlist:
        for news in stories:
            if trigger.evaluate(news):
                res.append(news)
    return res

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(triggerMap, triggerType, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    triggerMap: dictionary with names as keys (strings) and triggers as values
    triggerType: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies triggerMap, adding a new key-value pair for this trigger.

    Returns: None
    """
    if triggerType=='TITLE':
        triggerMap[name]=TitleTrigger(params[0])
        return triggerMap[name]
    elif triggerType=='SUBJECT':
        triggerMap[name]=SubjectTrigger(params[0])
        return triggerMap[name]
    elif triggerType=='SUMMARY':
        triggerMap[name]=SummaryTrigger(params[0])
        return triggerMap[name]
    elif triggerType=='AND':
        triggerMap[name]=AndTrigger(triggerMap[params[0]],triggerMap[params[1]])
        return triggerMap[name]
    elif triggerType=='OR':
        triggerMap[name]=OrTrigger(triggerMap[params[0]],triggerMap[params[1]])
        return triggerMap[name]
    elif triggerType=='NOT':
        triggerMap[name]=NotTrigger(triggerMap[params[0]])
        return triggerMap[name]
    elif triggerType=='PHRASE':
        triggerMap[name]=PhraseTrigger(' '.join([i for i in params]))
        return triggerMap[name]
def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    triggerMap = {}

    # Be sure you understand this code - we've written it for you,
    # but it's code you should be able to write yourself
    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])

    return triggers
    
import thread

SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        
        # TODO: Problem 11
        # After implementing makeTrigger, uncomment the line below:
        # triggerlist = readTriggerConfig("triggers.txt")

        # from here is about drawing
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()

