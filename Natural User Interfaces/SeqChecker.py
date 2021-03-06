'''
Created on 16-dec.-2013

@author: Kevin & Gertjan
'''
import random

class SeqChecker(object):
    '''
    classdocs
    '''


    def __init__(self, labeling, wordLength, alphabetSize, valuesPerLetter, collisionThreshold, r, heightDifference, distribution = None, letterWaarden = None):
        '''
        Constructor
        '''
        self.wait = -1
        self.labeling = labeling
        self.states = {}
        for label in labeling:
            self.states[label] = 0
        self.wordLength = wordLength
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.heightDifference = heightDifference
        self.distribution = distribution
        print(distribution);
        self.letterWaarden = letterWaarden
        self.countDown = -1
        self.masks = [[1,3,5,7,9],
                        [0,2,4,6,8],
                        [0,1,2,3,4],
                        [5,6,7,8,9],
                        [0,1,4,5,8],
                        [2,3,6,7,9],
                        [0,2,3,6,7],
                        [1,4,5,8,9],
                        [0,1,5,8,9],
                        [2,3,4,6,7]]
#         self.masks = self.getMasks()
        print("SeqChecker masks : " + str(self.masks))
        self.maskedLabeling = {}
        
        for label in labeling:
            self.maskedLabeling[label] = []
            saxArray = self.getSaxArray(self.labeling[label])
            #print(self.labeling[label][0].getAllPoints())
            print(saxArray)
            for masker in self.masks:
                self.maskedLabeling[label].append(self.mask(saxArray,masker))

        

                
    def checkSequence(self, sequence):
        #if sequence.getStart() < self.wait:
        #    return None
        #TODO

        if self.countDown > 0:
            self.countDown = self.countDown - 1
            return None
        if self.countDown == 0:
            print("wait is done")
            self.countDown = -1
            
            
        if sequence.getRealHeight() < self.heightDifference:
            return None
        possibleLabels = self.saxCheck(sequence)
        if len(possibleLabels) > 0:
            print("rangeCheck : " + sequence.getOldWord(self.wordLength, self.alphabetSize))
        matchLabels = self.rangeCheck(possibleLabels, sequence)
#         matchLabels = possibleLabels
        #if len(matchLabels) > 0:
        for label in matchLabels:
            if self.incrementState(label):
                self.resetStates()
                self.countDown = 10
                #self.wait = sequence.getStart() + sequence.getLength()
#                 print(str(sequence.getAllPoints()))
                #print(sequence.getWord(self.alphabetSize, self.valuesPerLetter, self.distribution, self.letterWaarden).getWord())
#                 print(sequence.getOldWord(self.wordLength, self.alphabetSize))
                return label
        return None
            
    def incrementState(self, label):
        print(label + " : " + str(self.states[label]))
        self.states[label] += 1
        if self.states[label] >= len(self.labeling[label]):
            return True
        else:
            return False
    
    def resetStates(self):
        for label in self.labeling:
            self.states[label] = 0
        
    def saxCheck(self, sequence):
#         word = [sequence.getWord(self.alphabetSize, self.valuesPerLetter, self.distribution, self.letterWaarden).getWord()]
        word = [sequence.getOldWord(self.wordLength, self.alphabetSize)]
        counters = {}
        for label in self.labeling:
            counters[label] = 0
        for i in range(len(self.masks)):
            maskedWord = self.mask(word, self.masks[i])[0]
            for label in self.labeling:
                if maskedWord == self.maskedLabeling[label][i][self.states[label]]:
                    counters[label] += 1
        
        possibleLabels = []
        for label in self.labeling:    
            if ( self.collisionThreshold <= counters[label]
                and sequence.getRealHeight() ) :                
                possibleLabels.append(label)
        return possibleLabels
    
    def rangeCheck(self, possibleLabels, sequence):
        
        matchLabels = []
        for label in possibleLabels:
            if sequence.getRealHeight() >= self.heightDifference and self.r >= self.labeling[label][self.states[label]].getNormalized().compare(sequence.getNormalized()):
                matchLabels.append(label)
        return matchLabels
    
    '''Returns the SAX-array of this timesequence.'''
    def getSaxArray(self, group):
        saxArray = []
        for seq in group:
            saxArray.append(seq.getWord(self.wordLength, self.alphabetSize))
#             saxArray.append(seq.makeSequence2().getWord(self.alphabetSize, self.valuesPerLetter, self.distribution, self.letterWaarden).getWord())
        return saxArray
    
    '''Returns a random generated list of masks (who satisfy our conditions)'''
    def getMasks(self):
        masks = []
        maskLengte = self.wordLength * 1 / 2
        while len(masks) < self.wordLength:
            mask = []
            while len(mask) < maskLengte:
                punt = random.randrange(self.wordLength)
                if not(punt in mask):
                    mask.append(punt)
            for m in masks:
                if len(m) != len(mask):
                    continue
                for element in m:
                    if not(element in mask):
                        break
                else:
                    break
            else:
                masks.append(mask)
        return masks
    
    '''Returns a masked version of the given SAX-array by the given masks'''
    def mask(self, saxArray, mask):
        maskedSaxArray = []
        for word in saxArray:
            maskWord = ""
            for i in range(self.wordLength):
                if not(i in mask):
                    maskWord += word[i]
            maskedSaxArray.append(maskWord)
        return maskedSaxArray
