import os
from random import randint
from shutil import copyfile


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
    print 'Closing program'
    raw_input('Press Enter to continue...')
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
            close("Invalid input")
    else:
        close("Invalid input")



def currentWord():
    if curword != '':
        print ' Current Word:',curword
    else:
        print " No word selected yet"



def nextWord():
    global curword,means,sents,loc
    wleft = len(wordList)
    if wleft>0:
        indx = randint(0,wleft-1)
        loc = dictname+'\\'+wordList[indx]
        txt = open(loc).read()
        data = clean(txt)
        curword = extract(data,'w')
        means = extract(data,'m').split(';')
        sents = extract(data,'s').split('.')
        del wordList[indx]
        print " What do you understand by '"+curword+"'"
    else:
        close("No more words left")



def selectWord():
    global curword,means,sents,inp,loc
    word = ''
    # read second argument a the selected word
    if len(inp)>1:
        inp[1] = inp[1].strip()
        if inp[1] == '':
            word = raw_input(" Enter the word: ")
        else:
            word = inp[1]
    else:
        word = raw_input(" Enter the word: ")
    #process the input
    word = word.strip().lower()
    if word == '':
        return        
    word = dictname+'\\'+word+'.txt'
    #read the word from file
    if os.path.exists(word):
        loc = word
        txt = open(word).read()
        data = clean(txt)
        curword = extract(data,'w')
        means = extract(data,'m').split(';')
        sents = extract(data,'s').split('.')
        print " What do you understand by '"+curword+"'"
    else:
        print " No such word in the selected dictionary"



def showRemaining():
    print ' Remaining words in the dictionary are:\n'
    i = 0
    for w in wordList:
        print '   %-15s' %w.replace('.txt',''),
        i += 1
        if i==4:
            print ''
            i=0
    print '\n\n Total remaining:',len(wordList),'words'



def showHint():
    if curword=='':
        print " No word selected yet"
        return
    if len(sents)>0:
        print ' Hint:',sents.pop(randint(0,len(sents)-1)).strip()
    else:
        print " No more hints left"



def showMeaning():
    if curword=='':
        print " No word selected yet"
        return    
    for m in means:
        print '',m.strip()



def markHard():   
    #error handling 
    if curword=='':
        print " No word selected yet"
        return         
    if os.path.exists(loc)==False:
        print " File not found:",loc
        return
    dest = loc.replace(dictname,'hard')
    if os.path.exists(dest):
        print " Word is already marked as hard"
        return
    if os.path.exists('hard\\')==False:
        os.mkdir('hard')
    #copy the file
    copyfile(loc, dest)
    print " '"+curword+"'","added to the 'hard' dictionary"



def printHelp():
    print """Following commands are Available:
    help:      prints this help message
    next:      select a new word randomly
    hint:      shows a sentences using the current word
    reveal:    reveals the meanings of current word
    this:      shows current word
    mark-hard: Copies the current word into the hard dictionary
    clear:     Clear the screen
    select:    Select a word by typing it
    remaining: Shows the remaining words in the dictionary
    exit:      exit the program"""



def clearScreen():
    os.system('cls')



#------ Main Program ------
os.system('cls')
dictList = loadDictNames()
dictname = selectDict(dictList)
cmdList = {'help':printHelp, 'next':nextWord, 'hint':showHint,'reveal':showMeaning, 'this':currentWord, 'mark-hard':markHard, 'clear':clearScreen,'remaining':showRemaining, 'select':selectWord, 'exit':exit}

print "Selected dictionary:",dictname

wordList = os.listdir(os.getcwd()+'\\'+dictname)
loc = ''
curword = ''
means = []
sents = []
inp = []

print ''
printHelp()
while True:
    inp = raw_input("\ncommand> ").split(' ')
    inp[0] = inp[0].strip().lower()
    if(inp[0]==''):
        continue
    if cmdList.has_key(inp[0]):
        print ""
        cmdList.get(inp[0])()
    else:
        print " Invalid Command"
