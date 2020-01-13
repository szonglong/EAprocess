##############################################################################
## EA data processor (Python 2.7)
## Function: EA Data Processor: Renames columns and does phase correction
## Author: Seah Zong Long
## Version: 0.0.0
## Last modified: 13/01/2020

## Changelog: 0.0.0 Created

## Instructions:
## Similar to pytest. Open and select file dir that contains EA files
##############################################################################

from pyExcelerator import *
import xlrd
import os,sys
from numpy import *
import numpy as np
import matplotlib.pyplot as plt  
import Tkinter
import tkFileDialog


root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window
root.wm_attributes('-topmost', 1) # Forces askdirectory on top

#currdir = os.getcwd()
#tempdir = tkFileDialog.askdirectory(parent=root, initialdir='C:\\Users\\E0004621\\Desktop\\ONDL Computer sync\\Papers\\Data\\4. Energy level alignment\\XPS', title='Please select the data folder') #select directory for data
tempdir = 'C:\\Users\\E0004621\\Desktop\\ONDL Computer sync\\Papers\\Data\\4. Energy level alignment\\EA\\Trial'
os.chdir(tempdir)

filelist = os.listdir(os.getcwd())  # working dir


if os.path.exists('processed')!=True:
    os.mkdir('processed')

wlist=[]
for filename in (filelist):
    if 'Vdc' in filename:
        wlist.append(filename)

for file in wlist:

    if os.path.exists('processed/%s' %file)!=True:
        os.mkdir('processed/%s' %file)

    w = Workbook()  ## creates workbook

    count = 0
    position = [0 for x in range (0,20)]
    
    f=open('%s' %file)      ## opens text file as f
#    print 'Processing %s' %file
    lines = f.readlines()       ## reads all lines
