from flask import Flask, request, redirect

wordDict = {
    "n": "Noun",
    "v": "Verb",
    "adj": "Adjective",
    "adv": "Adverb",
    "interj": "Interjection",
    "prep": "Preposition",
    "conj": "Conjunction",
    "pron": "Pronoun"
}

allWords = []
allDefs = []
allSorts = []

with open("defDict.txt", "rt") as dictFile:
    for line in dictFile:
        line = line[: -1].split("\t")

        cWord = line[0].lower()

        splitDef = line[1].replace('"', "").split("[")
        cDef = splitDef[0].strip()
        cInfo = splitDef[1][: -1]

        for keyName in wordDict:
            if not cInfo.find(keyName):
                cWordType = wordDict[keyName]
                if len(cInfo) > len(keyName):
                    cDef += "\n[" + cInfo[len(keyName)+1 :] + "]"
                break

        allDefs.append(cWordType + ":\n" + cDef)
        allWords.append(cWord)
        allSorts.append("".join(sorted(cWord)))

baseStr = ""
baseLength = 0
wildCards = 0


def elemHTML(tagName, innerHTML):
    return "<"+tagName+">" +innerHTML+ "</"+tagName.split()[0]+">"

def arrForUI(baseSrc, normArr, passPt1, passPt2, failMsg):
    if len(normArr):
        if len(normArr) > 1:
            normArr[-1] = "and "+normArr[-1]

        return baseSrc + passPt1 + ", ".join(normArr) + passPt2
    else:
        return failMsg + baseSrc+"."


def checkWordWC (dictWord):
    if len(dictWord) > baseLength:
        return False
    wildCount = wildCards
    cBase = baseStr
    for char in dictWord:
        nextFind = cBase.find(char) + 1
        if not nextFind:
            if wildCount: wildCount -= 1
            else: return False
        cBase = cBase[nextFind :]
    return True


def checkWordNWC (dictWord):
    if len(dictWord) > baseLength:
        return False
    cBase = baseStr
    for char in dictWord:
        nextFind = cBase.find(char) + 1
        if not nextFind: return False
        cBase = cBase[nextFind :]
    return True

formatLink = lambda wordObj : ('<a rel="noopener noreferrer" href="'+wordObj[0]+
'" title="' +wordObj[2]+ '">' +wordObj[0]+ "</a>")


app = Flask(__name__)
@app.route('/results', methods=["GET", "POST"])
def showWords():
    if request.method == "POST":
        sentData = str(request.get_data()).split("'")[1]
        inputLetters = sentData[:-1].replace("-", "_")
        if len(inputLetters) < 2:
            return "Please enter at least two letters first. Thanks!"

        dictZip = zip(allWords, allSorts, allDefs)
        global baseStr
        global baseLength
        global wildCards
        words = []
        directIncludeWords = []

        baseStr = "".join(sorted(inputLetters))
        baseLength = len(baseStr)
        wildCards = baseStr.count("_")
        isWild = bool(wildCards)

        if isWild:
            for dictWordObj in dictZip:
                if checkWordWC(dictWordObj[1]):
                    words.append(dictWordObj)

        else:
            for dictWordObj in dictZip:
                if checkWordNWC(dictWordObj[1]):
                    if dictWordObj[0] in inputLetters:
                        directIncludeWords.append(elemHTML("strong", formatLink(dictWordObj)))
                    words.append(dictWordObj)

        if int(sentData[-1]):
            formattedWords = ""
            currentWords = []
            for requestLength in range(2, baseLength+int(isWild)):
                for foundObj in words:
                    if len(foundObj[0]) == requestLength:
                        currentWords.append(formatLink(foundObj))

                if currentWords:
                    formattedWords = elemHTML('div class="column"',
                    elemHTML('div class="lengthHead"',
                    str(requestLength) + " letter words<br>(" +
                    str(len(currentWords)) + " found):") +
                    "<br>".join(currentWords)) + formattedWords
                    currentWords.clear()

        else:
            foundWordsArr = []
            for foundWord in words:
                foundWordsArr.append(formatLink(foundWord))
            formattedWords = "<br>".join(foundWordsArr)

        uiLetters = baseStr.upper().replace("_", "(WC)")
        newDoc = elemHTML("div", "Found "+str(len(words))+" words from "+uiLetters+"!")

        if not isWild:
            swapsArr = []
            for foundObj in words:
                if len(foundObj[0]) == baseLength:
                        swapsArr.append(elemHTML("strong", formatLink(foundObj)))

            swapsStr = arrForUI(uiLetters, swapsArr,
            " can be directly swapped to form ",
            "! (" + str(len(swapsArr)) + " found)",
            "No words can be formed by directly swapping ")

            cutsStr = arrForUI(inputLetters, directIncludeWords,
            " can be directly cut to form ", "!",
            "No words can be formed by directly cutting ")

            newDoc += swapsStr+"<br>"+cutsStr

        newDoc += elemHTML("div", formattedWords)

        return newDoc
    else: return redirect("/")
