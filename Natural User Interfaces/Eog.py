'''
Created on 8-nov.-2013

@author: Gertjan & Kevin
'''


import numpy as np
from scipy.signal import filtfilt, butter
import os
import csv
import math

class Eog(object):
    '''
    classdocs
    '''


    def __init__(self, relativePath):
        '''
        Constructor
        '''
        self.setMatrix(self.readData(relativePath))
        self.setAnnotations([])

    def setMatrix(self,matrix):
        self.__matrix = matrix
        
    def getMatrix(self):
        return self.__matrix
    
    def setAnnotations(self,annotations):
        self.__annotations = annotations
        
    def addAnnotation(self,annotation):
        self.__annotations.append(annotation)
        
    def getAnnotations(self):
        return self.__annotations
        
    def normalize(self):
        mean = sum(self.__matrix)/len(self.__matrix)
        nMatrix = self.__matrix
        nMatrix = [(x-mean) for x in nMatrix]
        '''nMatrix = self.__matrix - mean'''
        nMatrix = [(x/np.absolute(nMatrix).max()) for x in nMatrix]
        '''self.__matrix = nMatrix/abs(nMatrix).max()'''
        self.__matrix = nMatrix
        
    def filter(self):
        
        eog_filt1 = np.zeros(len(self.__matrix))
        '''4, 0.016'''
        b1, a1 = butter(1, 0.01, 'lowpass')
        b2, a2 = butter(4, 0.016, 'lowpass')
        eog_filt1 = filtfilt(b2, a2, self.__matrix)
        eog_filt2 = filtfilt(b1, a1, eog_filt1)   
        self.setMatrix(eog_filt1)
    
    def readData(self, relativePath):
        path = (os.getcwd()[:len(os.getcwd())])

        with open("C:\\Users\\Gertjan\\Documents\\GitHub\\NUI_Code\\Data\\test2_A.csv") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                return [float(i) for i in row]
