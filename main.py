import json
from PIL import Image
import numpy
import collections as cc

f = open('D:\kla\Level_1_data\input.json', )
data = json.load(f)

for i in range(1,data['die']['columns']+1):
    im = Image.open('D:\kla\Level_1_data\wafer_image_'+str(i)+'.png')
    px = im.load()
    width,height = im.size
    numpydata = numpy.array(im)
    ans = []
    r = list(range(data['care_areas'][0]['top_left']['x'],data['care_areas'][0]['bottom_right']['x']))
    print(r)
    for x in range(len(numpydata)):
        d = cc.defaultdict(int)
        for y in range(len(numpydata[i])):
            d[numpydata[x][y][0]] += 1
        m = 0
        for z in d:
            if(d[z] > m):
                temp = x
                m = d[z]
        for y in range(len(numpydata[i])):
            if(numpydata[i][y][0] != temp):
                ans.append([i,x,y])



f.close()