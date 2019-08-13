import xml.etree.ElementTree as ET
import operator

def countCharacter(character, numChars):
    newSoloCharacter = False
    
    if character not in bannedCharacters:        
        if character in wordCount:
            isSingled = wordCount[character][0]
            if not isSingled and numChars == 1:
                newSoloCharacter = True
                isSingled = True
                
            wordCount[character] = (isSingled, wordCount[character][1] + 1)
        else:
            newSoloCharacter = numChars == 1
            wordCount[character] = (newSoloCharacter, 1)
            
    return newSoloCharacter


tree = ET.parse('pleco2.xml')
root = tree.getroot()

wordCount = {}
soloCardCharacters = 0

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
                        if (countCharacter(character, len(headword.text))):
                            soloCardCharacters += 1
                      
sortedWords = sorted(wordCount.items(), key=operator.itemgetter(1))

newLineCounter = 0

outputText = "-------------------------------------------------\n"
outputText += "Total characters known: " + str(len(sortedWords))
outputText += "\nFormat - 'Character : Number of cards it appears on'\n"

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