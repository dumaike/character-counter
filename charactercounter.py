import xml.etree.ElementTree as ET
import operator

def countCharacter(character, numChars, firstReviewedTime):
    newSoloCharacter = False
    
    if character not in bannedCharacters:        
        if character in wordCount:
            isSingled = wordCount[character][0]
            if not isSingled and numChars == 1:
                newSoloCharacter = True
                isSingled = True
                
            cachedReviewedTime = wordCount[character][2]
            if (firstReviewedTime < cachedReviewedTime):
                cachedReviewedTime = firstReviewedTime
                
            wordCount[character] = [isSingled, wordCount[character][1] + 1, cachedReviewedTime]
        else:
            newSoloCharacter = numChars == 1
            wordCount[character] = [newSoloCharacter, 1, firstReviewedTime]
            
    return newSoloCharacter

tree = ET.parse('pleco5.xml')
root = tree.getroot()

wordCount = {}
soloCardCharacters = 0
totalCards = 0
oldestReviewedCard = 0

# Settings
numRows = 6

bannedCharacters = ["，", " ", ","]
#bannedCharacters = ["，", "Ｖ", "S", "ｖ", "ｓ", "+", " ", "。", ","]

for cards in root.findall('cards'):
    for card in cards.findall('card'):
        isGrammar = False
        numReviews = 0
        firstReviewedTime = 0
        for catassign in card.findall('catassign'):
            if (catassign.get('category') == "Grammar"):
                isGrammar = True
        for scoreinfo in card.findall('scoreinfo'):
            numReviews = scoreinfo.get('correct')
            numReviews = numReviews + scoreinfo.get('incorrect')
            if (scoreinfo.get('firstreviewedtime') != None):
                firstReviewedTime = int(scoreinfo.get('firstreviewedtime'))
        if (oldestReviewedCard == 0 or firstReviewedTime > oldestReviewedCard):
            oldestReviewedCard = firstReviewedTime
        if isGrammar == False and numReviews != 0:
            for entry in card.findall('entry'):
                totalCards += 1
                for headword in entry.findall('headword'):
                    charset = headword.get('charset')
                    if (charset == "tc"):
                        for character in headword.text:
                            if (countCharacter(character, len(headword.text), firstReviewedTime)):
                                soloCardCharacters += 1
                      
print(wordCount.items())
sortedWords = sorted(wordCount.items(), key=lambda x: (x[1][0], x[1][1], x[1][2]))

newLineCounter = 0

outputText = "-------------------------------------------------\n"
outputText += "Total cards in database: " + str(totalCards) + "\n"
outputText += "Total characters in database: " + str(len(sortedWords)) + "\n"
outputText += "Format - 'Character : Number of cards it appears on'\n"

outputText += "-------------------------------------------------\n"
outputText += "Characters that only appear in other words: \n"
nonSoloCharacters = len(sortedWords) - soloCardCharacters
outputText += str(nonSoloCharacters) + " (" + str(round(nonSoloCharacters*100/(len(sortedWords)), 2)) + "%)\n"
outputText += "-------------------------------------------------\n"
firstSection = True
for word, count in sortedWords:
    if firstSection and count[0]:
        firstSection = False
        if outputText[len(outputText) - 1] != "\n":
            outputText += "\n"
        outputText += "-------------------------------------------------\n"
        outputText += "Characters that have their own card: \n"
        outputText += str(soloCardCharacters) + " (" + str(round(soloCardCharacters*100/(len(sortedWords)), 2)) + "%)\n"
        outputText += "-------------------------------------------------\n"
        
    newLineCounter += 1
    outputText += str(word) + ": " +  str(count[1]) + "\t"
    if (newLineCounter >= numRows):
        newLineCounter = 0
        outputText += "\n"

print(outputText)
    
file = open("count_output.txt", "w+", encoding='utf-8')
file.write(outputText)
file.close()