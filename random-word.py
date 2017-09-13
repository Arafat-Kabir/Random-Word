import os
from random import randint

def clean(text):
    """Removes the comments and redundant spaces and returns a list of lines"""
    lines = text.split('\n')

    indx = range(len(lines))
    indx.reverse()
    for i in indx:
        temp = lines[i].strip()
        if temp == '' or temp.startswith('#'):
            del lines[i]
        else:
            lines[i] = temp    

    return lines


def extract(data, key):
    """Returns the line starting with the 'key'"""
    for d in data:
        if d.startswith(key):
            return d.replace(key+':','').strip()   #remove the parser tag then remove the spaces

def close(message):
    print message
    print 'Closing program...'
    exit()

def loadDictNames():
    """Read the dictionary listing file and return the dictionary names as a list"""
    txt = open('./dictionary-names.txt').read()
    lst = clean(txt)
    if(len(lst)<=0):
        close('No Dictionary found')
        exit()
    return lst


def selectDict(dictNames):
    print "Available Dictionaries:\n\t|"
    i = 1
    for d in dictNames:
        print '\t|--',str(i)+'.',d
        i += 1
    dselect = raw_input('\nChoose a Dictionary [1-'+str(i-1)+']: ')
    if dselect.isdigit():
        dselect = int(dselect)-1  #index is 0 based
        if(dselect<len(dictNames)):
            return dictNames[dselect]
        else:
            close(" Invalid input")
    else:
        close(" Invalid input")


def currentWord():
    if curword != '':
        print ' Current Word:',curword
    else:
        print " No word selected yet"


def nextWord():
    global curword,means,sents
    wleft = len(wordList)
    if wleft>0:
        indx = randint(0,wleft-1)
        txt = open(dictname+'\\'+wordList[indx]).read()
        data = clean(txt)
        curword = extract(data,'w')
        means = extract(data,'m').split(';')
        sents = extract(data,'s').split('.')
        del wordList[indx]
        print " What do you understand by '"+curword+"'"
    else:
        close(" No more words left")


def showHint():
    if curword=='':
        print " No word selected yet"
        return
    if len(sents)>0:
        print ' Hint:',sents.pop().strip()
    else:
        print " No more hints left"


def showMeaning():
    if curword=='':
        print "No word selected yet"
        return    
    for m in means:
        print '',m.strip()


def printHelp():
    print """Following commands are Available:
    help:   prints this help message
    next:   show a new random word
    hint:   shows a sentences using the current word
    reveal: reveals the meanings
    this:   shows current word
    clear:  Clear the screen
    exit:   exit the program"""

def clearScreen():
    os.system('cls')

#------ Main Program ------
os.system('cls')
dictList = loadDictNames()
dictname = selectDict(dictList)
cmdList = {'help':printHelp, 'next':nextWord, 'hint':showHint,'reveal':showMeaning, 'this':currentWord, 'clear':clearScreen, 'exit':exit}

print "Selected dictionary:",dictname

wordList = os.listdir(os.getcwd()+'\\'+dictname)
curword = ''
means = []
sents = []

print ''
printHelp()
while True:
    inp = raw_input("\ncommand$> ")
    inp = inp.strip().lower()
    if(inp==''):
        continue
    if cmdList.has_key(inp):
        print ""
        cmdList.get(inp)()
    else:
        print " Invalid Command"


