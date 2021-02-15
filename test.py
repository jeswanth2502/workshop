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
            im = Image.open('Level_2_data\wafer_image_' + str(i) + '.png')
            numpydata.append(numpy.array(im))
        for care in range(len(data['care_areas'])):
            for y in range(data['care_areas'][care]['top_left']['x'], data['care_areas'][care]['bottom_right']['x']):
                for x in range(data['care_areas'][care]['bottom_right']['y'],data['care_areas'][care]['top_left']['y']):
                    if(inExclusion(y,x) == False):
                        for i in range( data['die']['columns'] ):
                            d = cc.defaultdict(int)
                            d[tuple(numpydata[i][x][y])] += 1
                            if(i-1 >= 0):
                                d[tuple(numpydata[i-1][x][y])] += 1
                            if(i+1 < data['die']['columns']):
                                d[tuple(numpydata[i+1][x][y])] += 1
                            m = 0
                            for z in d:
                                if(d[z] > m):
                                    temp = z
                                    m = d[z]
                            if m == 1:
                                if(i-1 >= 0):
                                    if(d_ans[tuple([i-1 + row + 1, y, len(numpydata[i])-1-x])] == 0):
                                        ans.append([i-1 + row + 1, y, len(numpydata[i])-1-x])
                                        d_ans[tuple([i - 1 + row + 1, y, len(numpydata[i]) - 1 - x])] = 1
                                if(d_ans[tuple([i + row + 1, y, len(numpydata[i])-1-x])] == 0):
                                    ans.append([i + row + 1, y, len(numpydata[i]) - 1 - x])
                                    d_ans[tuple([i + row + 1, y, len(numpydata[i]) - 1 - x])] = 1
                                if(i+1 < data['die']['columns']):
                                    if(d_ans[tuple([i + 1 + row + 1, y, len(numpydata[i]) - 1 - x])] == 0):
                                        ans.append([i+1 + row + 1, y, len(numpydata[i]) - 1 - x])
                                        d_ans[tuple([i + 1 + row + 1, y, len(numpydata[i]) - 1 - x])] = 1
                            else:
                                if(tuple(numpydata[i][x][y]) != temp):
                                    if (d_ans[tuple([i + row + 1, y, len(numpydata[i]) - 1 - x])] == 0):
                                        ans.append([i + row + 1, y, len(numpydata[i]) - 1 - x])
                                        d_ans[tuple([i + row + 1, y, len(numpydata[i]) - 1 - x])] = 1

                                if (i-1 >= 0 and tuple(numpydata[i-1][x][y]) != temp):
                                    if (d_ans[tuple([i - 1 + row + 1, y, len(numpydata[i]) - 1 - x])] == 0):
                                        ans.append([i - 1 + row + 1, y, len(numpydata[i]) - 1 - x])
                                        d_ans[tuple([i - 1 + row + 1, y, len(numpydata[i]) - 1 - x])] = 1

                                if (i+1 < data['die']['columns'] and tuple(numpydata[i+1][x][y]) != temp):
                                    if (d_ans[tuple([i + 1 + row + 1, y, len(numpydata[i]) - 1 - x])] == 0):
                                        ans.append([i + 1 + row + 1, y, len(numpydata[i]) - 1 - x])
                                        d_ans[tuple([i + 1 + row + 1, y, len(numpydata[i]) - 1 - x])] = 1

        row += data['die']['columns']
    f.close()
    return True

ans = []
f = open('Level_2_data\input.json', )
data = json.load(f)
d_ex = cc.defaultdict(int)
d_ans = cc.defaultdict(int)
Exclusion(data)
detect_defect(data)

with open("final.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(ans)
