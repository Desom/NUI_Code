
import eyetracking2
import eyetracking3
import TimeSequence
import ThresholdSolution
import PatternSolution
import PatternSolution2
import Visualize
import Sequence2
import DataWindow
import numpy as np
from time import sleep
import queue
import threading
import Batcher
import DataSaver
import matplotlib.pyplot as plt

inputQueue = queue.Queue()
queueSemaphore = threading.Semaphore(10000)
queueAccessLock = threading.Lock()

THRESHOLD_CALIBRATION_LENGTH = 500
ALPHABET_SIZE = 8
VALUES_PER_LETTER = 15

directionThresholdPercentages = {"Left" : 0.45, "Right" : 0.45}
minimalThresholdHits = 3

def runT():
    #thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock))
    #thread.start()

    #calibrationPath = 'Data2\\test24_B.csv'
    #calibrationIndex = 250
    #recognitionPath = 'Data2\\test24_B.csv'
#     calibrationPath, vanC, totC= calibrationComp
#     recognitionPath, vanR, totR = recognitionComp
#     
#     batcher = Batcher.Batcher(ALPHABET_SIZE, VALUES_PER_LETTER)
#     batcher.setCalibrationData(vanC, totC, calibrationPath)
#     batcher.setRecognitionData(vanR, totR, recognitionPath)

    thresholdSol = thresholdsCalibration()
    print(thresholdSol)
    thresholdsRecognition(thresholdSol)


# TODO semaphore in plaats van lock
def thresholdsCalibration(batcher = None):
    if batcher == None:
        data = getDataRealTime()
    else:
        data = getDataBatch(batcher)
    timeSeq = TimeSequence.TimeSequence(data)
    timeSeq.filter()
    timeSeq.makeSaxWord(ALPHABET_SIZE, VALUES_PER_LETTER)

    directionThresholds = {}

    directionThresholds["Left"] = timeSeq.getMinimalValue() * directionThresholdPercentages["Left"]
    directionThresholds["Right"] = timeSeq.getMaximalValue() * directionThresholdPercentages["Right"]
    
    print("Left threshold: " + str(directionThresholds["Left"]))
    print("Right threshold: " + str(directionThresholds["Right"]))
    
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    thresholdSol.processTimeSequenceCalibration(timeSeq)

    Visualize.plot_data_saxString(timeSeq,ALPHABET_SIZE,VALUES_PER_LETTER)

    answer = input("Ben je tevreden met de resultaten? (y/n)")
    
    if answer == "y":
        return thresholdSol
    else:
        return thresholdsCalibration()

def getDataRealTime():
    return eyetracking3.run(THRESHOLD_CALIBRATION_LENGTH)

def getDataBatch(batcher):
    return batcher.getCalibrationVector()

def thresholdsRecognition(thresholdSol, batcher = None):
    dataWindow = DataWindow.DataWindow()
    if batcher == None:
        thread = threading.Thread(target=eyetracking3.run2, args=(inputQueue,queueSemaphore,dataWindow))
        thread.start()
    else:
        thread = threading.Thread(target=batcher.fillQueue, args=(inputQueue, dataWindow))
        thread.start()
    
    for i in range(50):
        letterPart = []
        for t in range(10):
            letterPart.append(inputQueue.get(True))
        dataWindow.addData(letterPart)
    print("End of data window fill.")
    
    letterPart = []
    for t in range(10):
        letterPart.append(inputQueue.get(True))
    while(letterPart != None):
        
        dataWindow.addData(letterPart)
        lastLetter = dataWindow.getLastValue()
        #print(lastLetter)
        if(thresholdSol.processTimeSequenceRecognition(lastLetter)):
            1==1
            dataWindow.flatten()
        letterPart = []
        for t in range(10):
            letterPart.append(inputQueue.get(True))



###########################################################################################
###########################################################################################
###########################################################################################
PATTERN_CALIBRATION_LENGTH = 40
P_ALPHABET_SIZE = 8
P_VALUES_PER_LETTER = 10
P_MAX_MATCHING_DISTANCE = 3


def runP(calibrationComp, recognitionComp):
    calibrationPath, vanC, totC= calibrationComp
    recognitionPath, vanR, totR = recognitionComp
    
    calibrationVector = Visualize.readData(calibrationPath, 23)

    dataDict = {"Left" : [],"Right" : []}
    
    if calibrationPath == 'Data2\\test8_B.csv':
        dataDict["Left"].append(calibrationVector[120:1000])
        dataDict["Left"].append(calibrationVector[1500:2200])
        dataDict["Left"].append(calibrationVector[2800:3450])
        dataDict["Right"].append(calibrationVector[900:1600])
        dataDict["Right"].append(calibrationVector[2200:2800])
        
    if calibrationPath == 'Data2\\test9_B.csv':
        dataDict["Left"].append(calibrationVector[200:800])
        dataDict["Left"].append(calibrationVector[1400:2000])
        dataDict["Left"].append(calibrationVector[2600:3250])
        dataDict["Right"].append(calibrationVector[800:1400])
        dataDict["Right"].append(calibrationVector[2000:2600])
        dataDict["Right"].append(calibrationVector[3300:3745])
        
        
#         dataDict["Left"].append(calibrationVector[150:750])
#         dataDict["Left"].append(calibrationVector[1350:1950])
#         dataDict["Left"].append(calibrationVector[2450:3050])
#         dataDict["Right"].append(calibrationVector[750:1350])
#         dataDict["Right"].append(calibrationVector[1900:2500])
#         dataDict["Right"].append(calibrationVector[3000:3600])

    patternSol = patternCalibration(dataDict)
    
    batcher = Batcher.Batcher(ALPHABET_SIZE, VALUES_PER_LETTER)
    
    batcher.setRecognitionData(vanR, totR, recognitionPath)
    
    patternRecognition(patternSol, batcher)

def patternCalibration(dataDict = None):
    if dataDict == None:
        dataDict = {"Left" : [],"Right" : []}
        for i in range(3):
            for direction in dataDict:
                print(direction)
                sleep(0.5)
                dataDict[direction].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    else:
        #patternSol = PatternSolution.PatternSolution(dataDict,P_ALPHABET_SIZE,P_VALUES_PER_LETTER, P_MAX_MATCHING_DISTANCE)
        patternSol = PatternSolution2.PatternSolution2(dataDict,10,P_ALPHABET_SIZE,P_VALUES_PER_LETTER,7,5,5000)
        patternSol.processTimeSequenceCalibration()
        return patternSol
   
def patternRecognition(patternSol, batcher = None):

    dataWindow = DataWindow.DataWindow()

    if batcher == None:
       thread = threading.  Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock,dataWindow))
       thread.start()
    else:
       thread = threading.Thread(target=batcher.fillQueue, args=(inputQueue, dataWindow))
       thread.start()

    for i in range(100):
        letterPart = inputQueue.get(True)
        #letterPart = [10000] * 10
#         for i in range(len(letterPart)):
#             letterPart[i] = letterPart[i]/2.5
        dataWindow.addData(letterPart)
    print("End of data window fill.")

    letterPart = inputQueue.get(True)
    while(letterPart != None):
#         for i in range(len(letterPart)):
#             letterPart[i] = letterPart[i]/2.5
        dataWindow.addData(letterPart)
        newSequence = Sequence2.Sequence2(dataWindow.getLastSequence(100))
        direction = patternSol.processTimeSequenceRecognition(newSequence)
        if (direction != None):
            print("You look in direction : " + direction)
        #dataWindow.flattenFirst()
        
        letterPart = inputQueue.get(True)

def plot(vector):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(vector)
    plt.show()

if __name__ == '__main__':
    thread = threading.  Thread(target=DataSaver.run)
    thread.start()
    runT()