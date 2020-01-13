##############################################################################
## EA data processor (Python 2.7)
## Function: EA Data Processor: Renames columns and does phase correction
## Author: Seah Zong Long
## Version: 0.0.1
## Last modified: 13/01/2020

## Changelog: 
## 0.0.0 Created
## 0.0.1 pandas-iefy
## 0.1 SSR fit, into df

## Instructions:
## Similar to pytest. Open and select file dir that contains EA files
##############################################################################

from pyExcelerator import *
import xlrd
import os,sys
from numpy import *
import numpy as np
import scipy.optimize 
import matplotlib.pyplot as plt  
import Tkinter
import tkFileDialog
import pandas as pd

def func(x,a,b):
    return np.sum((-a*np.sin(x)+b*np.cos(x))**2)


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
        
#   
for filename in wlist:

    f=open('%s' %filename)      ## opens text file as f
    lines = f.readlines()       ## reads all lines
    split_lines,a,b = [],[],[]

    for line in lines:
        split_line = [float(i) for i in line.split()]
        split_line[9] = split_line[9]/split_line[2]
        a.append(split_line[8])
        b.append(split_line[9])
#        res=scipy.optimize.minimize_scalar(func,args=(split_line[8],split_line[9]))
#        split_line[10]=split_line[8]*np.cos(res.x)+split_line[9]*np.sin(res.x)
#        split_line[11]=-split_line[8]*np.cos(res.x)+split_line[9]*np.cos(res.x)
        split_lines.append(split_line)

    a = np.array(a,dtype=float)
    b = np.array(b,dtype=float)
    res=scipy.optimize.minimize_scalar(func,args=(a,b))
#    print res.x
    for split_line in split_lines:
        split_line[10]=split_line[8]*np.cos(res.x)+split_line[9]*np.sin(res.x)
        split_line[11]=split_line[8]*-np.sin(res.x)+split_line[9]*np.cos(res.x)

    df = pd.DataFrame.from_records(split_lines,columns=['Photon Energy (eV)','Vdc','Vpd','Vpd_SD','Ch1','Ch1_SD','Ch2','Ch2_SD','Ch1/Vpd','Ch2/Vpd','%s' %filename,'Ch2p','m'])
    
    