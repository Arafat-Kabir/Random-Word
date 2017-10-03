import os
from random import randint
from shutil import copyfile
from glob import glob


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
        print ' Current dict:',dictname
    else:
        print " No word selected yet"
    print ''



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
        print " What do you understand by '"+curword+"'\n"
    else:
        close("No more words left")



def selectWord():
    global curword,means,sents,inp,loc
    word = ''
    # read second argument as the selected word
    if len(inp)>1:
        inp[1] = inp[1].strip()
        if inp[1] == '':
            word = raw_input(" Enter the word: ")
            print ''
        else:
            word = inp[1]
    else:
        word = raw_input(" Enter the word: ")
        print ''
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
        print " What do you understand by '"+curword+"'\n"
        #remove it from the wordlist
        wordfile = curword.lower()+'.txt'
        if wordfile in wordList:
            wordList.remove(wordfile)
    else:
        print " No such word in the selected dictionary\n"
	#end of selectWord()



def showRemaining():
    global inp
    print ' Remaining words in the dictionary are:'
    cols = 4  #default number of columns
    # read the second argument as the number of columns
    if len(inp)>1:
        inp[1] = inp[1].strip()
        if inp[1].startswith('-c'):
            #print 'starts with -c'
            inp[1] = inp[1][2:]  #srip off the -c 
            if inp[1].isdigit():
                #print 'is digit'
                inp[1] = int(inp[1])
                if inp[1]<=15 and inp[1]>0:
                    #print 'assigned cols =', inp[1]
                    cols = inp[1]
        else:
            word = inp[1]
    #print the remaining words
    i = 0
    for w in wordList:
        print '   %-15s' %w.replace('.txt','').capitalize(),
        i += 1
        if i==cols:
            print ''
            i=0
    print '\n\n Total remaining:',len(wordList),'words\n'



def relateFile():
    """Scans the meanings field and searches for the matches mentioned in the arguments"""
    global inp;
    cols = 4  #default no of columns
    #process the arguments
    for i in range(len(inp)-1,0,-1):
        inp[i] = inp[i].strip()
        if inp[i] == '':
            #print 'deleted',i
            del inp[i]
        elif inp[i].startswith('-c'):   #set the column number
            #print 'starts with -c'
            inp[i] = inp[i][2:]  #srip off the -c 
            if inp[i].isdigit():
                #print 'is digit'
                inp[i] = int(inp[i])
                if inp[i]<=10 and inp[i]>0:
                    #print 'assigned cols =', inp[1]
                    cols = inp[i]
                    del inp[i]
    #---check, search and print the matches---
    if len(inp)<2:
        print " Enter keywords to search\n"
    else:
        fileList = glob(dictname+'\\*')   #load files list
        searchResult = {}
        #search through the files
        for f in fileList:
            content = open(f).read().lower()
            content = clean(content)
            content = extract(content,'m')  #extract the meanings only
            for keyword in inp[1:]:
                if searchResult.has_key(keyword) == False:
                    searchResult[keyword] = []  #add an empty list
                if keyword.lower() in content:
                    temp = len(dictname)+1
                    temp = f[temp:-4]     #extract the file name only
                    searchResult[keyword].append(temp)
        #---print the search result---
        #print searchResult
        for key in searchResult:
            print " Related to",key.upper()+': ',str(len(searchResult[key])),'results'
            i = 0
            for r in searchResult[key]:
                print '   %-15s' %r.capitalize(),
                i += 1
                if i==cols:
                    i = 0
                    print ''
            print '\n'
	#end of relateFile()


def showHint():
    if curword=='':
        print " No word selected yet\n"
        return
    if len(sents)>0:
        temp = sents.pop(randint(0,len(sents)-1)).strip()
        if temp != '':
            print ' Hint: ',temp+'\n'
        else:
            print ' Sorry?\n'
    else:
        print " No more hints left\n"
	#end of showHint()



def showMeaning():
    if curword=='':
        print " No word selected yet\n"
        return    
    for m in means:
        print '',m.strip()
    print ''



def markHard():   
    """Copies the currenly selected file to the 'hard' dictionary"""
    #error handling 
    if curword=='':
        print " No word selected yet\n"
        return         
    if os.path.exists(loc)==False:
        print " File not found:",loc+'\n'
        return
    dest = loc.replace(dictname,'hard')
    if os.path.exists(dest):
        print " Word is already marked as hard\n"
        return
    if os.path.exists('hard\\')==False:
        os.mkdir('hard')
    #copy the file
    copyfile(loc, dest)
    print " '"+curword+"'","added to the 'hard' dictionary\n"



def unmarkHard():
    #error handling 
    if curword=='':
        print " No word selected yet"
        return         
    dest = loc.replace(dictname,'hard')
    if os.path.exists(dest)==False:
        print " '"+curword+"' is not in the 'hard' dictionary\n"
        return
    #delete the file
    os.remove(dest)
    print " '"+curword+"'","removed from the 'hard' dictionary\n"



def printHelp():
    print """ Following commands are Available:
    help:      prints this help message
    next:      select a new word randomly
    hint:      shows a sentence using the current word
    reveal:    reveals the meanings of current word
    this:      shows select word and dictionary name
    mark-hard: Copies the current word into the 'hard' dictionary
    not-hard:  Removes the current word from the 'hard' dictionary
    clear:     Clear the screen
    select:    Select a word by typing it
    relate:    relates specified keywords with the dictionary words
    remaining: Shows the remaining words in the dictionary
    exit:      exit the program
    """



def clearScreen():
    os.system('cls')


#------ Main Program ------
os.system('cls')
dictList = loadDictNames()        #loads available dictionary names for selection prompt
dictname = selectDict(dictList)   #selects and specify the selected dictionary
cmdList = {'help':printHelp, 'next':nextWord, 'hint':showHint,'reveal':showMeaning, 'this':currentWord, 'mark-hard':markHard, 'not-hard':unmarkHard, 'clear':clearScreen,'remaining':showRemaining, 'select':selectWord,'relate':relateFile, 'exit':exit}

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
    inp = raw_input("command> ").strip().split(' ')
    inp[0] = inp[0].strip().lower()
    if(inp[0]==''):
        continue
    if cmdList.has_key(inp[0]):
        print ""
        cmdList.get(inp[0])()
    else:
        print " Invalid Command\n"
