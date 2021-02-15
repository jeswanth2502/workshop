import json
from PIL import Image
import numpy
import collections as cc
import csv

f = open('Level_1_data\input.json', )
data = json.load(f)
ans = []
for i in range(1,data['die']['columns']+1):
    im = Image.open('Level_1_data\wafer_image_'+str(i)+'.png')
    px = im.load()
    width,height = im.size
    numpydata = numpy.array(im)
    d = cc.defaultdict(int)
    r = [data['care_areas'][0]['top_left']['x'],data['care_areas'][0]['bottom_right']['x']]
    for x in range(len(numpydata)):
        for y in range(len(numpydata[x])):
            d[tuple(numpydata[x][y])] += 1
    m1 = 0
    m2 = 0
    temp1 = ()
    for z in d:
        if(d[z] > m1):
            temp2 = temp1
            temp1 = z
            m2 = m1
            m1 = d[z]
        elif(d[z] > m2):
            temp2 = z
            m2 = d[z]
    for y in range(data['care_areas'][0]['top_left']['x'],data['care_areas'][0]['bottom_right']['x']):
        for x in range(data['care_areas'][0]['bottom_right']['y'],data['care_areas'][0]['top_left']['y']):
            if(tuple(numpydata[x][y]) != temp1 and tuple(numpydata[x][y]) != temp2):
                ans.append([i,y,len(numpydata)-1-x])

with open("final.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(ans)

f.close()