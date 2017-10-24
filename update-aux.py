import os
from filecmp import cmp
from shutil import copyfile
from glob import glob


#---- Main Program ----
source_folders = ['random/','barron800/','barron333/']
dest_folders = ['hard/','barronAll/']

#load source dictionaries
sources = {}
for s in source_folders:
    files = glob(s+'*.txt')
    length = len(s)
    for i in range(len(files)):
        files[i] = files[i][length:]
    sources[s] = files


#update dependent dictionaries one-by-one
#d = dest_folders[0]
for d in dest_folders:
    print '\n---- Working on \''+d+'\' ----'
    cnt = 0
    files = glob(d+'*.txt')
    length = len(d)
    for i in range(len(files)):
        files[i] = files[i][length:]
        f = files[i]
        #print files[i]
        for k in source_folders:
            if f in sources[k]:
                if cmp(k+f, d+f)==False:
                    cnt += 1
                    print 'Updating:  ',k+f,' -> ',d+f
                    copyfile(k+f, d+f)
    if cnt>0:
        print '\nTotal updated: ',cnt,'entries\n'
    else:
        print '  All entries up-to-date\n'






