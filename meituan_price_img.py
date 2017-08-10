# encoding=utf8
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

TESSERACT_PATH = 'd:\\onedrive\\meituan\\tesseract.exe'

def tesseract(x,y,filename):
    fp = open(filename,'rb')
    output='output'
    img = Image.open(fp)
    region = (x,y,x+7,y+13)
    cropImg = img.crop(region)
    cropImg.save(filename)
    fp.close()
    os.system('echo off')
    os.system(TESSERACT_PATH + ' ' + filename + ' ' + output + ' -psm 10 -l num')
    f = open(output+".txt")
    t=f.readlines()[0]
    f.close()
    return t

#print tesseract(60,0,'1.png')
