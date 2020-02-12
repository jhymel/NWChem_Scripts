import os
import sys

readFile = sys.argv[1]
inputFile = sys.argv[2]
home = os.getcwd()

count = 0
data = []
data_tmp = []
filePositions = []
with open(readFile, 'r') as f:
    #buff = f.readlines()
    for lineNumber, line in enumerate(f):
        print(line)
        if line.split(' ')[0] == '#modified':
            filePositions.append(lineNumber)
        print (line)
        for item in line.split():
            data_tmp.append(item.replace(',',''))
        data.append(data_tmp)
        data_tmp = []

with open('test.out', 'w+') as g:
    with open(inputFile, 'r') as f:
        for line in f:
            if line.split(' ')[0] != 'geometry':
                print(line)
                g.write(line)
            else:
                g.write(line)
                for geom_line in range(1,int(filePositions[0])+1):
                    g.write(str(data[int(filePositions[0])+int(geom_line)+1]).replace(',','').replace('[','').replace(']','').replace('"','').replace("'",'') + '\n')
print (data)
print (filePositions)
#print (buff)
