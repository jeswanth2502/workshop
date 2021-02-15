import json
from PIL import Image
import numpy
import collections as cc
import csv

def Exclusion(data):
    for exclusion in range(len(data['exclusion_zones'])):
        for y in range(data['exclusion_zones'][exclusion]['top_left']['x'], data['exclusion_zones'][exclusion]['bottom_right']['x']):
            for x in range(data['exclusion_zones'][exclusion]['bottom_right']['y'], data['exclusion_zones'][exclusion]['top_left']['y']):
                d_ex[tuple([y,x])] = 1

def inExclusion(i,j):
    if d_ex[tuple([i,j])] == 1:
        return True
    return False

def detect_defect(data):
    row = 0
    while(row < data['die']['rows']*data['die']['columns']):
        numpydata = []
        for i in range(row+1, data['die']['columns']+row+ 1):
            im = Image.open('Level_1_data\wafer_image_' + str(i) + '.png')
            numpydata.append(numpy.array(im))
        for care in range(len(data['care_areas'])):
            for y in range(data['care_areas'][care]['top_left']['x'], data['care_areas'][care]['bottom_right']['x']):
                for x in range(data['care_areas'][care]['bottom_right']['y'],data['care_areas'][care]['top_left']['y']):
                    if(inExclusion(y,x) == False):
                        d = cc.defaultdict(int)
                        for i in range( data['die']['columns'] ):
                            d[tuple(numpydata[i][x][y])] += 1
                        m = 0
                        for z in d:
                            if(d[z] > m):
                                temp = z
                                m = d[z]
                        if m == 1:
                            for i in range(data['die']['columns']):
                                ans.append([i+row+1,y,len(numpydata[i])-1-x])
                        else:
                            for i in range(data['die']['columns']):
                                if(tuple(numpydata[i][x][y]) != temp):
                                    ans.append([i+row+1,y,len(numpydata[i])-1-x])
        row += data['die']['columns']
    f.close()
    return True

ans = []
f = open('Level_1_data\input.json', )
data = json.load(f)
d_ex = cc.defaultdict(int)
Exclusion(data)
detect_defect(data)

with open("final.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(ans)
