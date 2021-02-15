import json
from PIL import Image
import numpy
import collections as cc
import csv

f = open('Level_1_data\input.json', )
data = json.load(f)
ans = []
numpydata = []
for i in range(1, data['die']['columns'] + 1):
    im = Image.open('Level_1_data\wafer_image_' + str(i) + '.png')
    px = im.load()
    width, height = im.size
    numpydata.append(numpy.array(im))

for y in range(data['care_areas'][0]['top_left']['x'], data['care_areas'][0]['bottom_right']['x']):
    for x in range(data['care_areas'][0]['bottom_right']['y'],data['care_areas'][0]['top_left']['y']):
        d = cc.defaultdict(int)
        for i in range( data['die']['columns'] ):
            d[tuple(numpydata[i][x][y])] += 1
        m = 0
        for z in d:
            if(d[z] > m):
                temp = z
                m = d[z]
        print(d)
        if m == 1:
            for i in range(data['die']['columns']):
                ans.append([i+1,y,len(numpydata)-1-x])
        else:
            for i in range(data['die']['columns']):
                if(tuple(numpydata[i][x][y]) != temp):
                    ans.append([i+1,y,len(numpydata[i])-1-x])
print(ans)
with open("final.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(ans)
f.close()