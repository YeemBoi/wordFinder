const okKeys = [8, 16, 37, 39, 61, 95, 189];
const wordValues = ["eaionrtlsu", "dg", "bcmp", "fhvwy", "k", "jx", "qz"];
const loadNote = "Loading...";

var dictionary = [];

var base = document.createElement("base");
base.href = "https://www.collinsdictionary.com/dictionary/english/";
base.setAttribute("TARGET", "_blank");

window.addEventListener("DOMContentLoaded", (event) =>
{
    var wordDiv = document.getElementById("resultsDiv");
    var userInput = document.getElementById("letters");
    var goButton = document.getElementById("goButton");
    var sortBox = document.getElementById("lengthSort");

    goButton.onclick = function()
    {
        if (wordDiv.innerHTML == loadNote)
            return;
        if (wordDiv.innerHTML)
            document.head.removeChild(base);

        this.style.backgroundColor = "#009900";
        var pyGet = new XMLHttpRequest();
        pyGet.open("POST", "/results", true);
        pyGet.setRequestHeader("Content-Type", "text/plain;charset=ASCII");
        pyGet.onload = function (e)
        {
            goButton.style.backgroundColor = "#00ff00";
            if (this.readyState === 4)
            {
                if (this.status === 200)
                {
                    document.head.appendChild(base);
                    wordDiv.innerHTML = this.responseText;
                }
            }
            else alert(this.statusText);
        }
        pyGet.onerror = function(e){alert(this.statusText);};
        pyGet.send(userInput.value.toLowerCase()+Number(sortBox.checked));
        wordDiv.innerHTML = loadNote;
    };

    userInput.addEventListener("keydown", function(ev)
    {
        var pKey = ev.keyCode;
        if (!okKeys.includes(pKey) && !(pKey>64 && pKey<91))
            ev.preventDefault();
        if (pKey == 13)
            goButton.click();
    });

    userInput.oninput = function()
    {this.value = this.value.toUpperCase();};

    var dictReq = new XMLHttpRequest();
    dictReq.open("GET", "/dictionary.txt", true);
    dictReq.onload = function (e)
    {
        if (dictReq.readyState === 4)
        {
            if (dictReq.status === 200)
            {
                dictionary = dictReq.responseText.split(" ");

                var resultsElem = document.getElementById("checkerResults");
                var userInputElem = document.getElementById("word");
                var word;
                var outputStr;
                var score;
                userInputElem.oninput = function()
                {
                    word = userInputElem.value.toLowerCase();
                    outputStr = word + " is ";
                    if (word.length < 2)
                    {
                        resultsElem.innerHTML = "";
                        return;
                    }
                    if (dictionary.includes(word))
                    {
                        score = 0;
                        for (cI in word)
                        {
                            for (vI in wordValues)
                            {
                                if (wordValues[vI].includes(word[cI]))
                                {
                                    score += Number(vI)+1;
                                    break;
                                }
                            }
                        }
                        outputStr += "worth "+score+" points.";
                    }
                    else outputStr += "not a valid word.";
                    resultsElem.innerHTML = outputStr;
                };
            }
            else
                alert(dictReq.statusText);
        }
    };
    dictReq.onerror = function(e){alert(dictReq.statusText);};
    dictReq.send(null);
});
