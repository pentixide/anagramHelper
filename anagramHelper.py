from csv import reader
from random import shuffle,randint
from time import sleep

alphabet = "abcdefghijklmnopqrstuvwxyz"
fileName = 'anagramNames.csv'
symbolList = ['1234567890!@#$%^&*()_=+{}[]/\|;",.<>?'," '-"] 
symbolListJoined = "".join(symbolList) #I can't say I like this variable

# has to be a valid anagram for one of the 102 NPCs, or don't
testingWordBypass = "" 

lineLimit = 80          # targets this max width
lineMin = 60            # will at least be this wide
spaceMultiplyer = 4     # limits added spaces to 4x original amount
shortLineMultiplyer = 2 # line length * shLiMu < longest line, limits added " "
minHints = 20           # for hint # randint generation  
maxHints = 30           # same same
outputDivider = " "     # replaces the commas for what

    # it's main, what do you want
def main(stupidCount, anagram = ""):
    lengthDict,nameDict = parseCSV()
    anagram,stupidCount = anagramInput(stupidCount,anagram)
    
    hintList = hintGenerate(stupidCount,anagram,lengthDict, nameDict)
    cleanedHintList = cleanHintOutput(hintList)
    print("\n"+cleanedHintList,"\n\n")

    main(stupidCount)
    #endGame(stupidCount)


    # csv of names from osrs wiki page, 102 total
    # returns two dicts {'Evil Dave':'evildave'} or {'Evil Dave':'8'}
def parseCSV(fileName = fileName):
    with open(fileName) as f:
        readText = reader(f)
        data = "".join(list(readText)[0])

    collapsedString, lengthDict = data, dict()
    displayString, nameDict = data, dict()

    for symbol in symbolList[0]:
        displayString = displayString.replace(symbol,"")
    displayList = displayString.split(':')

    for symbol in symbolListJoined:
        collapsedString = collapsedString.replace(symbol,"")
    collapsedList = collapsedString.lower().split(':')

    for index in range(len(displayList)):
        lengthDict[displayList[index]] = len(collapsedList[index])
        nameDict[displayList[index]] = collapsedList[index]

    return lengthDict,nameDict



    # gathers input and sends to hint
def anagramInput(stupidCount,anagram):
    if(len(anagram) == 0):
        anagram = input("Enter anagram here: ").lower()        
    
    if(anagram == 'exit' or anagram == 'quit'):
        print("\nClosing window now.")
        sleep(1)
        exit()
    else:
        anagram = anagram.lower()
        for character in anagram:
            if(character not in alphabet):
                anagram = anagram.replace(character,"")
        if(len(anagram) > 3):
            return anagram,stupidCount
        else:
            print(anagram)
            stupidSwitch(stupidCount,True)


    # generates at least "minimumHints" in the list
def hintGenerate(stupidCount, anagram, lengthDict, nameDict):
    wordLength,word = len(anagram),anagram

    hintList = []
    maxMargin = 1
    minMargin = 0
    minimumHints = randint(minHints,maxHints)

    while(len(hintList) < minimumHints):
        minL = wordLength - minMargin
        maxL = wordLength + maxMargin

        shuffleDict = list(lengthDict.items())
        shuffle(shuffleDict)
        lengthDict = dict(shuffleDict)

        for key in lengthDict:
            if(lengthDict[key] == wordLength or
               maxL > lengthDict[key] and
               lengthDict[key] > minL):
                hintList.append(key)
        if(len(hintList) < minimumHints):
            if(maxMargin <= minMargin):
                maxMargin = maxMargin + 1
            else:
                minMargin = minMargin + 1
            hintList = []
        else:
            for hint in hintList:
                hintSorted = list(nameDict[hint])
                wordSorted = list(word)
                hintSorted.sort()
                wordSorted.sort()

                if(hintSorted == wordSorted):
                    return hintList

                elif(hint == hintList[-1]):
                    stupidSwitch(stupidCount)


    # creates a new line after LINELIMIT is reached, also attempts to justify text based on
    # the longest line before any modifications.
    # there's probably a better way to do this but, it works so...
def cleanHintOutput(hintList):
    outputList = []
    tempString=""

    for hint in hintList:
        hintBool = hint == hintList[-1]
        tempLen = len(tempString)
        if(tempLen == 0):
            tempString = hint + ","
        elif(tempLen+len(hint)+2 > lineLimit):
            if(tempString[-1] == ","):
                tempString = tempString[:-1]
            outputList.append(tempString)
            tempString = hint + ","
        elif(hintBool):
            tempString = tempString + " " + hint
            outputList.append(tempString)
        else:
            tempString = tempString + " " + hint + ","
            
    spaceAdjustedList = []
    longestLine = 0

    for line in outputList:
        if(len(line) > longestLine):
            longestLine = len(line)
    spaceMultiplyerL = spaceMultiplyer

    for line in outputList:
        if(len(line) * shortLineMultiplyer < longestLine):
            spaceMultiplyerL = 1.5
        lineSpaces = line.count(" ")
        while(len(line) < longestLine and
              line.count(" ") < int(lineSpaces * spaceMultiplyerL)):
            count = 0
            for character in line:
                if(character == "," and len(line) < longestLine):
                    count = count + 1
                    line = line[:count] + " " + line[count:]
                count = count + 1
        spaceAdjustedList.append(line)
        
    return "\n".join(spaceAdjustedList).replace(",",outputDivider)


    # resets the program, took it out for better flow
def endGame(stupidCount):
    endInput = input("\n\tDo you want to enter another anagram? (Y/N): ")
    if(endInput.replace(" ","").lower() not in ["n","no"]):
        print("\n")
        main(stupidCount)
    else:
        exit()


    # it's stupid, ignore this function
def stupidSwitch(stupidCount,shortWord = False, wow = False):
    if(stupidCount < 12):
        stupidCount = stupidCount + 1
    else:
        stupidCount = 1

    if(shortWord and stupidCount < 2):
        outputMessage = "  Too short."
    else:
        if(stupidCount < 4):
            outputMessage = "  Somethings fishy here, try again."
        elif(stupidCount < 5):
            outputMessage = "  Okay I beleive in you, you can do it."
        elif(stupidCount < 6):
            outputMessage = "  Maybe the program is just glitched or something, no dice on this garbage."
        elif(stupidCount < 7):
            outputMessage = "  Okay, no. It is definitely you."
        elif(stupidCount < 8):
            outputMessage = "  <3 Goodluck on all your adventures! <3"
        else:
            if(randint(0,100) != 69):
                outputMessage = "  Alright, Alright, Alright!"
            else:
                wow = True
                outputMessage = "  Wow!"

    print("\n",outputMessage,"\n\n")
    if(wow):
        sleep(1)

    main(stupidCount)


    # no comment
if __name__ == "__main__":
    try:
        main(0,testingWordBypass)
    except RecursionError as e:
        main(8)
