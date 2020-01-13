##############################################################################
## EA data processor (Python 2.7)
## Function: EA Data Processor: Renames columns and does phase correction
## Author: Seah Zong Long
## Version: 1.0.0
## Last modified: 13/01/2020

## Changelog: 
## 0.0.0 Created
## 0.0.1 pandas-iefy
## 0.1 SSR fit, into df
## 0.1.1 Make into plot
## 1.0.0 Export processed plots

## Instructions:
## Similar to pytest. Open and select file dir that contains EA files
##############################################################################

from pyExcelerator import *
import xlrd
import os,sys
import numpy as np
import scipy.optimize 
import matplotlib.pyplot as plt  
import Tkinter
import tkFileDialog
import pandas as pd

def func(x,a,b):
    return np.sum((-a*np.sin(x)+b*np.cos(x))**2)


#root = Tkinter.Tk()
#root.withdraw() #use to hide tkinter window
#root.wm_attributes('-topmost', 1) # Forces askdirectory on top

#currdir = os.getcwd()
#tempdir = tkFileDialog.askdirectory(parent=root, initialdir='C:\\Users\\E0004621\\Desktop\\ONDL Computer sync\\Papers\\Data\\4. Energy level alignment\\XPS', title='Please select the data folder') #select directory for data
tempdir = 'C:\\Users\\E0004621\\Desktop\\ONDL Computer sync\\Papers\\Data\\4. Energy level alignment\\EA\\Trial'
os.chdir(tempdir)

filelist = os.listdir(os.getcwd())  # working dir


if os.path.exists('processed')!=True:
    os.mkdir('processed')

wlist=[] #working list
for filename in (filelist):
    if 'Vdc' in filename:
        wlist.append(filename)
print wlist        
first = 0

for filename in wlist:

    f=open('%s' %filename)      
    lines = f.readlines()       
    split_lines,a,b = [],[],[]

### Small subroutine to find the voltage used from the filename ###    
    voltage_name = ''
    
    if '-' in filename:
        voltage_name = filename[filename.index('-'):filename.index('V')]
    else:
        if '.' in filename:
            voltage_name = filename[filename.index('.')-1:filename.index('V')]
        else:
            voltage_name = filename[filename.index('V')-1:filename.index('V')]
    
#    print voltage_name    

    for line in lines:
        split_line = [float(i) for i in line.split()]
        split_line[9] = split_line[9]/split_line[2]
        a.append(split_line[8])
        b.append(split_line[9])
        split_lines.append(split_line)

    a = np.array(a,dtype=float)
    b = np.array(b,dtype=float)
    res=scipy.optimize.minimize_scalar(func,args=(a,b))
#    print res.x
    for split_line in split_lines:
        split_line[10]=split_line[8]*np.cos(res.x)+split_line[9]*np.sin(res.x)
        split_line[11]=split_line[8]*-np.sin(res.x)+split_line[9]*np.cos(res.x)

    df = pd.DataFrame.from_records(split_lines,columns=['PE','Vdc','Vpd','Vpd_SD','Ch1','Ch1_SD','Ch2','Ch2_SD','Ch1/Vpd','Ch2/Vpd','%s' %voltage_name,'Ch2p','m'])
#    fig, axes = plt.subplots(sharex=True)
    least_sq_plot = df.plot(x='PE',y=['%s' %voltage_name,'Ch2p']).get_figure()
    if first == 0:
        big_plot_array=(df.PE.to_frame()).join(df['%s' %voltage_name])
        first = 1
        
    else:
        big_plot_array=big_plot_array.join(df['%s' %voltage_name])
        
    least_sq_plot.savefig('processed/%s _p.png' %voltage_name)
    plt.close()
#    plt.close()
    f.close()
big_plot = big_plot_array.plot(x='PE',legend).get_figure()
big_plot.savefig('processed/bigplot.png')
plt.close()