import xml.etree.ElementTree as ET
import operator

def countCharacter(character, numChars):
    if character in bannedCharacters:
        return
    
    if character in wordCount:
        isSingled = wordCount[character][0]
        if (not isSingled and numChars == 1):
            isSingled = True
            
        wordCount[character] = (isSingled, wordCount[character][1] + 1)
    else:
        wordCount[character] = (numChars == 1, 1)

tree = ET.parse('pleco2.xml')
root = tree.getroot()

wordCount = {}

# Settings
numRows = 6

bannedCharacters = ["，", "Ｖ", "S", "ｖ", "ｓ", "+", " ", "。", ","]

for cards in root.findall('cards'):
    for card in cards.findall('card'):
        for entry in card.findall('entry'):
            for headword in entry.findall('headword'):
                charset = headword.get('charset')
                if (charset == "tc"):
                    for character in headword.text:
                        countCharacter(character, len(headword.text))
                      
sortedWords = sorted(wordCount.items(), key=operator.itemgetter(1))

newLineCounter = 0
outputText = "-------------------------------------------------\n"
outputText += "Characters that only appear in other words\n"
outputText += "-------------------------------------------------\n"
firstSection = True
for word, count in sortedWords:
    if firstSection and count[0]:
        firstSection = False
        if outputText[len(outputText) - 1] != "\n":
            outputText += "\n"
        outputText += "-------------------------------------------------\n"
        outputText += "Characters that appear in their own card\n"
        outputText += "-------------------------------------------------\n"
        
    newLineCounter += 1
    outputText += str(word) + ": " +  str(count[1]) + "\t"
    if (newLineCounter >= numRows):
        newLineCounter = 0
        outputText += "\n"
        

    
outputText += "\ntotal characters known: " + str(len(sortedWords))

print(outputText)
    
file = open("count_output.txt", "w+", encoding='utf-8')
file.write(outputText)
file.close()