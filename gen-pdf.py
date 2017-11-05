# Generates the PlainTeX formate file
# Invokes pdfTeX to compile into output.pdf

import os
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



#------------ Main Program ------------
format = """
\\beginsection
%s

%s\\vskip 3 mm
\\noindent
"""
output = 'output.tex'
render = ''

folder = raw_input('Enter Folder name: ').strip()
output = raw_input('Enter output file name: ').strip()
if os.path.isdir(folder)==False:
    raw_input(" The Folder doesn't exit!\n Closing program...\n Press Enter to continue...");
    exit();

files = glob(folder+'/*.txt')
for f in files:
    print 'working on',f
    txt = open(f).read()
    data = clean(txt)
    curword = extract(data,'w')
    means = extract(data,'m')
    sents = []
    try:
        sents = extract(data,'s').split('.')
    except:
        pass
        #nothing

    temp = format % (curword, means)
    for s in sents:
        s = s.replace('"',"`")
        s = s.replace('$',"dollar ")
        temp += s+'\\hfil\\break\n'
    render += temp+'\n'
render += '\\bye'

f = open(output+'.tex','w')
f.write(render)
f.close()
inp = raw_input("Should I run pdfTex? (Y/N): ").strip().lower()
if inp.startswith('y'):
    os.system('pdftex '+output+'.tex')
    print '---- PDF file generated ----'
close('')


