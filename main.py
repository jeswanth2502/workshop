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

    r = [data['care_areas'][0]['top_left']['x'],data['care_areas'][0]['bottom_right']['x']]
    for x in range(len(numpydata)):
        d = cc.defaultdict(int)
        for y in range(len(numpydata[x])):
            d[str(numpydata[x][y])] += 1
        m = 0
        for z in d:
            if(d[z] > m):
                temp = z
                m = d[z]
        if(x >= r[0] and x <= r[1]):
            for y in range(data['care_areas'][0]['bottom_right']['y'],data['care_areas'][0]['top_left']['y']+1):
                if(str(numpydata[x][y]) != str(temp)):
                    ans.append([i,x,y])
    print(ans)
with open("final.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(ans)

f.close()