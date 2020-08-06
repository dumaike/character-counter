import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import bisect
import datetime

def countNewWord(firstReviewedTime, numCharacters):
    if (numCharacters > 4):
        numCharacters = 4;
    bisect.insort(timestamps[numCharacters - 1], int(firstReviewedTime))

def fillPlot(wordCount):
    wordsOfCount = timestamps[wordCount]
    xInterval = 0
    graphPlot = list(range(numIntervals))
    for i in wordsOfCount:
        if ((xInterval < (numIntervals - 1)) and i <= xValues[xInterval + 1] and i >= xValues[xInterval]):
            xInterval+=1
            if (cumulative):
                graphPlot[xInterval] = graphPlot[xInterval - 1]
        graphPlot[xInterval] += 1
        
    return graphPlot

def flattenArray(arrayToFlatten):
    startingValue = arrayToFlatten[0]
    for i in range(len(arrayToFlatten)):
        arrayToFlatten[i] = arrayToFlatten[i] - startingValue
    
        
tree = ET.parse('pleco4.xml')
root = tree.getroot()

timestamps = [[],[],[],[]]

totalWords = 0
firstReview = -1;
lastReview = 0;

#Settings
numIntervals = 20
removeFirstIntervals = 1
cumulative = True
flattenToStartingY = True

for cards in root.findall('cards'):
    for card in cards.findall('card'):
        firstReviewedTime = 0;
        numCharacters = 0;
        for scoreInfo in card.findall('scoreinfo'):
            srsType = scoreInfo.get('scorefile')
            if srsType == "Spaced Repetition":
                firstReviewedTime = int(scoreInfo.get('firstreviewedtime'))
        for entry in card.findall('entry'):
            for headword in entry.findall('headword'):
                charset = headword.get('charset')
                if (charset == "tc"):
                    numCharacters = len(headword.text)
        if (firstReviewedTime != 0):
            if (firstReviewedTime < firstReview or firstReview == -1):
                firstReview = firstReviewedTime
            if (firstReviewedTime > lastReview):
                lastReview = firstReviewedTime
            countNewWord(firstReviewedTime, numCharacters)
            totalWords += 1

print("First Review: " +  datetime.datetime.fromtimestamp(firstReview).strftime('%c'))
print("Last Review: " + datetime.datetime.fromtimestamp(lastReview).strftime('%c'))

xValues = list(range(numIntervals))
for i in xValues:
    xValues[i] = ((i/numIntervals)*(lastReview - firstReview)) + firstReview

xLabels = list(range(numIntervals))
for i in xLabels:
    xLabels[i] = datetime.datetime.fromtimestamp(xValues[i]).strftime('%c')

y1 = fillPlot(0)
y2 = fillPlot(1)
y3 = fillPlot(2)
y4 = fillPlot(3)

for i in range(removeFirstIntervals):
    xLabels.pop(0)
    xValues.pop(0)
    y1.pop(0)
    y2.pop(0)
    y3.pop(0)
    y4.pop(0)

if flattenToStartingY:
    flattenArray(y1)
    flattenArray(y2)
    flattenArray(y3)
    flattenArray(y4)
    
print("Total Words: " + str(totalWords))

y = np.vstack([y1, y2, y3, y4])

labels = ["1 Character ", "2 Charactes", "3 Characters", "4+ Characters"]

fig, ax = plt.subplots()
ax.stackplot(xValues, y1, y2, y3, y4, labels=labels)
plt.xticks(xValues, xLabels)
ax.legend(loc='upper left')
plt.xticks(rotation=90)
plt.show()