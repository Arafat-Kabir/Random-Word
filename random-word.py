import os

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


def selecDict(dictNames):
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


helpStr = """Following commands are Available:
    help: prints this help message
    next: show a new random word
    hint: shows a sentences using the current word
    show: reveals the meaning
    exit: exit the program
"""


#------ Main Program ------
os.system('cls')
dictList = loadDictNames()
dictname = selecDict(dictList)
print "Selected dictionary:",dictname

wordList = os.listdir(os.getcwd()+'\\'+dictname)


# txt = open('./barron333/zealot.txt').read()
# data = clean(txt)
# word = extract(data,'w')
# means = extract(data,'m').split(';')
# sents = extract(data,'s').split('.')


# # print the elements
# for l in data:
#     print l

# print 'word:',word
# print 'meanings:',means
# print 'sentences:',sents

