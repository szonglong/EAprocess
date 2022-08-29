##############################################################################
## EA data processor (Python 2.7)
## Function: EA Data Processor: Renames columns and does phase correction
## Author: Seah Zong Long
## Version: 1.3
## Last modified: 22/08/2022

## Changelog: 
## 0.0.0 Created
## 0.0.1 pandas-iefy
## 0.1 SSR fit, into df
## 0.1.1 Make into plot
## 1.0.0 Export processed plots
## 1.1.1 Export with plots and excel
## 1.2 Export excel with big_plot_array
## 1.3 Adapt to newer version of EA program (Current ver 1.0.r)

## Instructions:
## Similar to pytest. Open and select file dir that contains EA files
##############################################################################

#from pyExcelerator import *
#import xlrd
import os
import numpy as np
import scipy.optimize 
import matplotlib.pyplot as plt  
import Tkinter
import tkFileDialog
import pandas as pd

def func(x,a,b):  # function to minimise (i.e "Ch2_processed")
    return np.sum((-a*np.sin(x)+b*np.cos(x))**2)

opt_range = [2.8,3.1] # range to optimise. Format: [lower_lim, upper_lim]. (Default: [])

### get file list ###
root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window
root.wm_attributes('-topmost', 1) # Forces askdirectory on top

currdir = os.getcwd()
tempdir = tkFileDialog.askdirectory(parent=root, initialdir='C:\\Users\\e0004621\\Desktop\\ONDL desktop sync\\Papers\\Data\\7. Stability\\EA', title='Please select the data folder') #select directory for data
#tempdir = 'C:\\Users\\e0004621\\Desktop\\ONDL desktop sync\\Papers\\Data\\7. Stability\\EA\\20220822\\300k'
os.chdir(tempdir)

filelist = os.listdir(os.getcwd())  # working dir

if os.path.exists('processed')!=True:
    os.mkdir('processed')

wlist=[] #working list
for filename in (filelist):
    if 'Vdc' in filename and 'txt' in filename:
        wlist.append(filename)
        
print wlist                


### init variables ###
first = 0 # file counter
writer = pd.ExcelWriter('processed/processed.xlsx', engine='xlsxwriter')
SSR_list = []


### begin processing ###
for filename in wlist:
    f=open('%s' %filename)      
    lines = [l for l in (line.strip() for line in f) if l][1:] #discards headers & empty lines
    split_lines,a,b,PE = [],[],[],[]

### Small subroutine to find the voltage used from the filename ###    
    voltage_name = ''
    
    if '-' in filename:
        voltage_name = filename[filename.index('-'):filename.index('V')]
    else:
        if '.' in filename:
            voltage_name = filename[filename.index('.')-1:filename.index('V')]
        else:
            voltage_name = filename[filename.index('V')-1:filename.index('V')]

    for line in lines: #process readlines. 
        split_line = [float(i) for i in line.split()]
        a.append(split_line[7])
        b.append(split_line[8])
        PE.append(split_line[0])
        split_lines.append(split_line)

    try:
        if opt_range != []:
            lower_index = PE.index(opt_range[0])
            upper_index = PE.index(opt_range[1])
            
            a = a[upper_index:lower_index] #for descending list of PE
            b = b[upper_index:lower_index]
            
    except ValueError:
        print("%s: opt_range not in photon energy list. Set to optimise over whole range; accept or try again" %voltage_name)
        
    a = np.array(a,dtype=float)
    b = np.array(b,dtype=float) #because I am lazy to work in arrays before this

    res=scipy.optimize.minimize_scalar(func,args=(a,b)) # optimisation step -> Phase == res.x
    SSR_list.append((voltage_name,res.x)) # create voltage-phase correction table

    for split_line in split_lines: #making processed channels
#        split_line.append(split_line[7]*np.cos(res.x)+split_line[8]*np.sin(res.x)) #works with labview prog ver 1.0.0
        split_line[9] = split_line[7]*np.cos(res.x)+split_line[8]*np.sin(res.x) #works with labview prog ver. 1.0.r
        split_line.append(split_line[7]*-np.sin(res.x)+split_line[8]*np.cos(res.x))

    df = pd.DataFrame.from_records(split_lines,columns=['PE','Ch1','Ch1_SD','Ch2','Ch2_SD','Vpd','Vpd_SD','Ch1/Vpd','Ch2/Vpd','%s' %voltage_name,'Ch2p'])
    least_sq_plot = df.plot(x='PE',y=['%s' %voltage_name,'Ch2p']).get_figure() # Phase plot

    if first == 0: #Combining to get big EA plot
        big_plot_array=(df.PE.to_frame()).join(df['%s' %voltage_name])
        first = 1
    else:
        big_plot_array=big_plot_array.join(df['%s' %voltage_name],rsuffix='_re')
        
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    least_sq_plot.savefig('processed/%s _p.png' %voltage_name)
    plt.close()
    df.to_excel(writer, sheet_name = '%s' %voltage_name)
    f.close()

big_plot = big_plot_array.plot(x='PE').get_figure()
big_plot.savefig('processed/bigplot.png')

df2 = pd.DataFrame(SSR_list, columns = ['Voltage','Phase'])
df2.to_excel(writer, sheet_name = 'SSR')
big_plot_array.to_excel(writer, sheet_name = 'bigplot')

plt.close()
writer.save()
