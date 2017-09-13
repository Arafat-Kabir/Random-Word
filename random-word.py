import os

def clean(text):
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
    for d in data:
        if d.startswith(key):
            return d.replace(key+':','').strip()   #remove the parser tag then remove the spaces


txt = open('./barron333/zealot.txt').read()
data = clean(txt)
word = extract(data,'w')
means = extract(data,'m').split(',')
sents = extract(data,'s').split('.')


# print the elements
for l in data:
    print l

print 'word:',word
print 'meanings:',means
print 'sentences:',sents

