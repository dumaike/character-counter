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
numRows = 5

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

outputText = ""
newLineCounter = 0
for word, count in sortedWords:
    newLineCounter += 1
    outputText += str(word) + ": " +  str(count) + "\t"
    if (newLineCounter > numRows):
        newLineCounter = 0
        outputText += "\n"
    
outputText += "\ntotal characters known: " + str(len(sortedWords))

print(outputText)
    
file = open("count_output.txt", "w+", encoding='utf-8')
file.write(outputText)
file.close()