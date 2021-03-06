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
    print " Parisng error: could not extract key '"+key+"'"
    print ' File:',loc
    return ''   #so that program execution doesn't stop



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
    print '\t|--','0. Load a saved session'
    for d in dictNames:
        print '\t|--',str(i)+'.',d
        i += 1
    dselect = raw_input('\nChoose an option [0-'+str(i-1)+']: ').strip()
    if dselect.isdigit():
        dselect = int(dselect)-1  #index is 0 based
        if dselect == -1:    #session-load option
            sessionList()
            if sessionLoad()==True:
                return dictname
            else:
                close('Initialization failed')
        if(dselect<len(dictNames)):
            return dictNames[dselect]
        else:
            close("Invalid input")
    else:
        close("Invalid input")



def currentWord():
    if curword != '':
        print ' Current Word :',curword
        print ' Current dict :',dictname
        print ' File location:',loc
    else:
        print " No word selected yet"
    print ''



def nextWord():
    global curword,means,sents,loc
    wleft = len(wordList)
    if wleft>0:
        indx = randint(0,wleft-1)
        loc = dictname+'/'+wordList[indx]
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
    word = dictname+'/'+word+'.txt'
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



def showAll():
    global inp
    print ' Words in the dictionary are:'
    cols = 4  #default number of columns
    classify = False
    # read the rest arguments
    for i in range(1,len(inp)):
        inp[i] = inp[i].strip()
        if inp[i].startswith('-c'):
            #print 'starts with -c'
            inp[i] = inp[i][2:]  #srip off the -c
            if inp[i].isdigit():
                #print 'is digit'
                inp[i] = int(inp[i])
                if inp[i]<=15 and inp[i]>0:
                    #print 'assigned cols =', inp[1]
                    cols = inp[i]
        elif inp[i] == '--classify':
            classify = True
    #print the words
    lst = os.listdir(os.getcwd()+'/'+dictname)
    i = 0
    first = ''
    for w in lst:
        w = w.replace('.txt','').capitalize()
        #classify according to first letter
        if classify:
            if first != w[0]:
                first = w[0]
                i = 0
                head = cols*9
                format = '\n\n  %'+str(head)+'s'
                print format %first
        #Print the word
        print '   %-15s' %w,
        i += 1
        if i==cols:
            print ''
            i=0
    print '\n\n Total words:',len(lst),'words\n'



def showRemaining():
    global inp
    print ' Remaining words in the dictionary are:'
    cols = 4  #default number of columns
    classify = False
    # read the rest arguments
    for i in range(1,len(inp)):
        inp[i] = inp[i].strip()
        if inp[i].startswith('-c'):
            #print 'starts with -c'
            inp[i] = inp[i][2:]  #srip off the -c
            if inp[i].isdigit():
                #print 'is digit'
                inp[i] = int(inp[i])
                if inp[i]<=15 and inp[i]>0:
                    #print 'assigned cols =', inp[1]
                    cols = inp[i]
        elif inp[i] == '--classify':
            classify = True
    #print the remaining words
    i = 0
    first = ''
    for w in wordList:
        w = w.replace('.txt','').capitalize()
        #classify according to first letter
        if classify:
            if first != w[0]:
                first = w[0]
                i = 0
                head = cols*9
                format = '\n\n  %'+str(head)+'s'
                print format %first
        #print the word
        print '   %-15s' %w,
        i += 1
        if i==cols:
            print ''
            i=0
    print '\n\n Total remaining:',len(wordList),'words\n'


#------------- Subset operations ----------------
def showSubset():
    global inp
    cols = 4  #default number of columns
    classify = False
    # read the display options
    indx = range(len(inp))[1:]
    indx.reverse()
    for i in indx:
        inp[i] = inp[i].strip()
        if inp[i].startswith('-c'):
            #print 'starts with -c'
            temp = inp[i][2:]  #srip off the -c
            if temp.isdigit():
                #print 'is digit'
                temp = int(temp)
                if temp<=15 and temp>0:
                    #print 'assigned cols =', inp[1]
                    cols = temp
                    del inp[i]
        elif inp[i] == '--classify':
            classify = True
            del inp[i]
    #extract subset select keys
    keys = inp[1:]
    if len(keys)<=0:
        print ' Provide some valid keys\n'
        return
    for i in range(len(keys)):
        keys[i] = keys[i].lower()
    #print the words in the subset
    print ' Words in the subset are:'
    cnt = 0
    i = 0
    first = ''
    for w in wordList:
        inset = False
        for k in keys:
            if w.startswith(k):
                inset = True
        if inset == False:
            continue
        cnt += 1
        w = w.replace('.txt','').capitalize()
        #classify according to first letter
        if classify:
            if first != w[0]:
                first = w[0]
                i = 0
                head = cols*9
                format = '\n\n  %'+str(head)+'s'
                print format %first
        #print the word
        print '   %-15s' %w,
        i += 1
        if i==cols:
            print ''
            i=0
    if cnt <=0:
        print ' --- No word belongs to your subset ---\n'
    else:
        print '\n\n Subset contains:',cnt,'words\n'



def selectSubset():
    global inp
    #extract subset select keys
    keys = inp[1:]
    if len(keys)<=0:
        print ' Provide some valid keys\n'
        return
    #print the keys
    print ' Subset selection keys:'
    for i in range(len(keys)):
        keys[i] = keys[i].lower()   #convert keys into lowercase
        print '               ',keys[i].upper()  #show in uppercase
    #discard non-matching words
    cnt = 0
    indx = range(len(wordList))
    indx.reverse()  #take a reverse approach
    for i in indx:
        #check if the word is in the subset
        inset = False
        for k in keys:
            if wordList[i].startswith(k):
                inset = True
        #only keep the words belonging to the set
        if inset:
            cnt += 1
        else:
            del wordList[i]
    #show report
    print ' Requested Subset selected successfully!'
    print ' Subset contains',cnt,'words\n'





def relateFile():
    """Scans the meanings and word fields and searches for the matches mentioned in the arguments"""
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
        fileList = glob(dictname+'/*')   #load files list
        searchResult = {}
        #search through the files
        for f in fileList:
            content = open(f).read().lower()
            content = clean(content)
            temp1 = extract(content,'m')  #extract the meanings only
            temp2 = extract(content,'w')  #extract the meanings only
            content = temp2 + ' ' + temp1
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
    if os.path.exists('hard/')==False:
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



#--------- Session Management ---------

def sessionSave():
    """Writes the session variables value into an external file inside the sessions directory"""
    if os.path.exists('sessions/')==False:
        os.mkdir('sessions')
    #error handling
    if curword=='':
        print " No word selected yet\n"
        return
    #name = "session-"+str(randint(0,9))+str(randint(-9,-1))
    name = ''
    # read second argument as the selected session name
    if len(inp)>1:
        inp[1] = inp[1].strip()
        if inp[1] == '':
            name = raw_input(" Enter the session-name: ")
        else:
            name = inp[1]
    else:
        name = raw_input(" Enter the session-name: ")
    #check for error names
    name = name.strip()
    if name == '':
        print ''
        return
    name += '.session'
    if os.path.exists('sessions/'+name):
        #--look for overwrite option--
        if len(inp)>2:
            if inp[2].strip().lower() == '-o':
                print ' Older session will be over-written'
            else:
                print ' Duplicate session name!\n'
                return
        else:
            print ' Duplicate session name!\n'
            return
    #--- record the session data ---
    data = 'dictname:'+dictname+'\n'
    data += 'loc:'+loc+'\n'
    data += 'curword:'+curword+'\n'
    #record words
    data += 'means:'
    for m in means:
        data += m.strip()+';'
    data += '\n'
    #record sentences
    data += 'sents:'
    for s in sents:
        data += s.strip()+'.'
    data += '\n'
    #record word list
    data += 'wordList:'
    for w in wordList:
        data += w+';'
    #print data
    #save the recorded data
    f = open('sessions/'+name,'w')
    f.write(data)
    f.close()
    print ' Session data saved successfully\n'



def sessionLoad():
    """Loads the specified session file"""
    if os.path.exists('sessions/')==False:
        os.mkdir('sessions')
    #name = "session-"+str(randint(0,9))+str(randint(-9,-1))
    name = ''
    # read second argument as the selected session name
    if len(inp)>1:
        inp[1] = inp[1].strip()
        if inp[1] == '':
            name = raw_input(" Enter the session-name: ")
        else:
            name = inp[1]
    else:
        name = raw_input(" Enter the session-name: ")
    #check for error names
    name = name.strip()
    if name == '':
        print ''
        return
    name += '.session'
    if os.path.exists('sessions/'+name)==False:
        print ' No such session exists!'
        sessionList()
        return
    else:
        if parseSessionData(open('sessions/'+name).read())==True:
            print ' Session loaded successfully\n'
            return True
        else:
            print " Session wasn't loaded!\n"
            return False



def parseSessionData(data):
    global dictname,loc,curword,means,sents,wordList
    data = data.split('\n')
    #print data,'\n'
    #--load dicname--
    if data[0].startswith('dictname:'):
        d = data[0].replace('dictname:','')
    else:
        print ' Session file corrupted'
        return False
    #print 'dict:',d
    #--load loc--
    if data[1].startswith('loc:'):
        lc = data[1].replace('loc:','')
    else:
        print ' Session file corrupted'
        return False
    #print 'loc:',lc
    #--load curword--
    if data[2].startswith('curword:'):
        cw = data[2].replace('curword:','')
    else:
        print ' Session file corrupted'
        return False
    #print 'curword:',cw
    #--load means--
    if data[3].startswith('means:'):
        mn = data[3].replace('means:','').split(';')
        mn = mn[0:-1]  #there is a blank at the end
    else:
        print ' Session file corrupted'
        return False
    #print 'means:',mn
    #--load sents--
    if data[4].startswith('sents:'):
        st = data[4].replace('sents:','').split('.')
        st = st[0:-1]  #there is a blank at the end
    else:
        print ' Session file corrupted'
        return False
    #print 'sents:',st
    #--load wordList--
    if data[5].startswith('wordList:'):
        wl = data[5].replace('wordList:','').split(';')
        wl = wl[0:-1]  #there is a blank at the end
    else:
        print ' Session file corrupted'
        return False
    #print 'wordList:',wl
    #--Assign global data--
    dictname = d
    loc = lc
    curword = cw
    means = mn
    sents = st
    wordList = wl
    return True



def sessionDelete():
    """Deletes the specified session file"""
    if os.path.exists('sessions/')==False:
        os.mkdir('sessions')
    #name = "session-"+str(randint(0,9))+str(randint(-9,-1))
    name = ''
    # read second argument as the selected session name
    if len(inp)>1:
        inp[1] = inp[1].strip()
        if inp[1] == '':
            name = raw_input(" Enter the session-name: ")
        else:
            name = inp[1]
    else:
        name = raw_input(" Enter the session-name: ")
    #check for error names
    name = name.strip()
    if name == '':
        print ''
        return
    name += '.session'
    if os.path.exists('sessions/'+name)==False:
        print ' No such session exists!'
        sessionList()
        return
    else:
        os.remove('sessions/'+name)
        print ' Session file removed successfully\n'



def sessionList():
    """Lists the saved sessions"""
    if os.path.exists('sessions/')==False:
        os.mkdir('sessions')
    lst = os.listdir(os.getcwd()+'/sessions')
    if(len(lst)<1):
        print " No saved sessions found"
    else:
        print " Available sessions:"
        for l in lst:
            print '   ',l.replace('.session','')
    print ''



def systemCommands():
    """Executes the system commands"""
    if len(inp)<2:
        print " provide the system command to be executed\n"
        return
    else:
        cmd = ' '.join(inp[1:])
        #print cmd
        os.system(cmd)
        print ''




def printHelp():
    print """ Following commands are Available:
    help:      Prints this help message
    next:      Select a new word randomly
               Short-hand: n
    hint:      Shows a sentence using the current word.
               Short-hand: h
    reveal:    Reveals the meanings of current word
               Short-hand: r
    this:      Shows selected word and dictionary name
    mark-hard: Copies the current word into the 'hard' dictionary
    not-hard:  Removes the current word from the 'hard' dictionary
    clear:     Clear the screen
    select:    Select a word by typing it
    relate:    Relates specified keywords with the dictionary words

    remaining: Shows the remaining words in the dictionary
      [ -cxx]     : Specifies the number of columns to be printed
      [--classify]: Classify the words by the first letter

    all:       Shows all the words in the dictionary
      [ -cxx]     : Specifies the number of columns to be printed
      [--classify]: Classify the words by the first letter

    session  : Session management command prefix: session-list etc.
      <-list>: Shows the list of previously saved sessions
      <-save>: Saves the current session; [-o] to force overwrite
               [name] : Specify session name
               [-o]   : Force overwrite existing session file
      <-del >: Deletes and specified existing session
      <-load>: Loads an specified existing session

    subset   : Subset selection command prefix: subset-show etc.
      <-show>  : Shows the list of the words in a subset specified
                 by the keys in the arguments. Takes -cxx and --classify
                 as optional arguments
      <-select>: Selects the words in the subset of the remaining words
                 specified by the keys in the arguments.

    system:    invoke a system command
    exit:      exit the program

    --------------------------------------------------------

    P.S: All commands are case-insensitive
         [xx] means optional arguments separated by spaces
         <xx> compulsory postfix without spaces
    """


def shortHelp():
    print """ Following commands are Available:
    help:      Prints a detailed help message
    next:      select a new word randomly
    hint:      shows a sentence using the current word
    reveal:    reveals the meanings of current word
    this:      Shows selected word and dictionary name
    mark-hard: Copies the current word into the 'hard' dictionary
    not-hard:  Removes the current word from the 'hard' dictionary
    clear:     Clear the screen
    select:    Select a word by typing it
    relate:    relates specified keywords with the dictionary words
    remaining: Shows the remaining words in the dictionary
    all:       Shows all the words in the dictionary
    session:   Session-management prefix. [Type 'Help' for details]
    subset:    Subset selection prefix. [Type 'Help' for details]
    system:    invoke a system command
    exit:      exit the program
    """



def clearScreen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')




#------------ Main Program ------------
intro = """\
-----------------------------------------
|                                       |
|    Python Script for word practice    |
|    Coded by: Md. Arafat Kabir Sun     |
|                                       |
-----------------------------------------
"""
cmdList =  {'help':printHelp, 'next':nextWord, 'n':nextWord, 'hint':showHint, 'h':showHint,'reveal':showMeaning,'r':showMeaning, 'this':currentWord,
            'mark-hard':markHard, 'not-hard':unmarkHard, 'clear':clearScreen,'remaining':showRemaining, 'all':showAll,
            'select':selectWord,'relate':relateFile,
            'session-list':sessionList, 'session-save':sessionSave, 'session-del':sessionDelete, 'session-load':sessionLoad,
            'subset-show':showSubset, 'subset-select':selectSubset,
            'system':systemCommands, 'exit':exit}
dictname = ''
loc = ''
curword = ''
wordList = []
means = []
sents = []
inp = []

#--initializations--
clearScreen()
print intro
dictList = loadDictNames()        #loads available dictionary names for selection prompt
dictname = selectDict(dictList)   #selects and specify the selected dictionary, load a session

if len(wordList)==0:
    print "Selected dictionary:",dictname
    try:
        wordList = os.listdir(os.getcwd()+'/'+dictname)
    except:
        close("---Selected dictionary doesn't exist---")
else:
    currentWord()  #a session was loaded, show current status
print ''
shortHelp()  #show help at the beginning

#--Command processing loop--
while True:
    inp = raw_input("command> ").strip().split()
    if len(inp)<=0:
        continue
    inp[0] = inp[0].strip().lower()
    if(inp[0]==''):
        continue
    if cmdList.has_key(inp[0]):
        print ""
        cmdList.get(inp[0])()
    else:
        print " Invalid Command\n"
