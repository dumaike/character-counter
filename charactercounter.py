import xml.etree.ElementTree as ET
import operator

def countCharacter(character):
    if character in wordcount:
        wordcount[character] = wordcount[character] + 1
    else:
        wordcount[character] = 1

tree = ET.parse('pleco2.xml')
root = tree.getroot()

wordcount = {}

for cards in root.findall('cards'):
    for card in cards.findall('card'):
        for entry in card.findall('entry'):
            for headword in entry.findall('headword'):
                charset = headword.get('charset')
                if (charset == "tc"):
                    for character in headword.text:
                        countCharacter(character)
                      
sorted_words = sorted(wordcount.items(), key=operator.itemgetter(1))

for word, count in sorted_words:
    print (word, count)
    
print ("total characters known: ", len(sorted_words))