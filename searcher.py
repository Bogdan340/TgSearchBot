import re, os
def search(text: str, word: str, register: bool, replace: str = None, differentCharacters: int = 0, generalConditions: bool = False):
    print(differentCharacters)
    result = []
    initialWord = word
    word = word if register else word.lower()
    textArrays = {}
    initialOffers = re.split(r'[.\n?;]+', text) 
    text = re.split(r'[.\n?;]+', text) if register else re.split(r'[.\n?;]+', text.lower())
    for i in range(len(text)):
        arr = re.split(r'[, ]+', text[i])
        for j in arr:
            if j == "":
                arr.remove(j)
        try:
            textArrays[str(i)] = {"words": arr, "first": "".join([ij[0] for ij in arr])}
        except:
            continue
    
    if differentCharacters > 0:
        for i in textArrays:
            for j in textArrays[i]["words"]:
                minLen = len(j) if len(j) < len(word) else len(word)

                firstIf = (abs(len(j) - len(word)) == differentCharacters) if generalConditions else (abs(len(j) - len(word) )<= differentCharacters)
                if firstIf and j[0: minLen] == word[0: minLen]:
                    if replace is None:
                        result.append((initialOffers[int(i)])+"\n")
                        continue
                    else:
                        offer = initialOffers[int(i)]
                        result.append(f"Первоначальное предложения: '{offer}'\n")
                        offer = initialOffers[int(i)].strip().replace(initialWord.strip(), replace.strip())
                        result.append(f"Предложения с заменной: '{offer}'\n")
                        continue
    
    for i in textArrays:
        if word[0] in textArrays[str(i)]["first"] and word in textArrays[str(i)]["words"]:
            if replace is None:
                result.append((initialOffers[int(i)])+"\n")
            else:
                offer = initialOffers[int(i)]
                result.append(f"Первоначальное предложения: '{offer}'")
                offer = initialOffers[int(i)].strip().replace(initialWord.strip(), replace.strip())
                result.append(f"Предложения с заменной: '{offer}'\n")
    print(remove_duplicates(result))
    return "\n".join(remove_duplicates(result))

def remove_duplicates(nested_list):
    unique_list = []
    for element in nested_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list

def searchInFiles(filePath: list[str] = None, directoryPath: str = None, word: str = None, register: bool = False, replace: str = None, differentCharacters: int = 0, generalConditions: bool = False) -> None:
    if filePath is None and directoryPath is None:
        return
    filePath = [directoryPath+i for i in os.listdir(directoryPath)] if directoryPath != None else filePath
    for i in filePath:
        with open(i, "r+", encoding="utf8") as f:
            search(f.read(), word=word, register=register, replace=replace, differentCharacters=differentCharacters, generalConditions=generalConditions)
            f.close()