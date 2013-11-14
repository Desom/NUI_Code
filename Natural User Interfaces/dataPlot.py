'''
Created on 22-okt.-2013

@author: Gertjan & Kevin
'''

import csv

import io
import serial
import threading
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import Threshold
import Eog
import Sax
from scipy.signal import filtfilt, butter
from time import sleep
from struct import *

global eog1
global eog2
global eog1_filt
global eog2_filt


with open('C:\\Users\\Kevin\\git\\NUI_Code\\Data\\test10_A.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data1 = [float(i) for i in row]
        
with open('C:\\Users\\Kevin\\git\\NUI_Code\\Data\\test10_B.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data2 = [float(i) for i in row]

b, a = butter(2, 0.05, 'low')
for i in range(1):
    data1 = filtfilt(b, a, data1)
    data2 = filtfilt(b, a, data2)
    print(i)

eog1 = Eog.Eog(data1)
eog2 = Eog.Eog(data2)



eog1.normalize()
eog2.normalize()

def plot_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(eog1.getMatrix())
    line2, = ax2.plot(eog2.getMatrix())
    plt.show()

plot_data()