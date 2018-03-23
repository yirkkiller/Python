import itertools
from collections import Counter

PATH = "D:\\Badges\\"

dictPriorities = {
        "Hunter" : {
                "Critical Damage" : 2,
                "Damage" : 3,
                "Health" : 1,
                "Critical Chance" : 0,
                "Damage Reduction" : 0
            },
        "Assault" : {
                "Critical Damage" : 0,
                "Damage" : 0,
                "Health" : 3,
                "Critical Chance" : 1,
                "Damage Reduction" : 2
            },
        "Shooter" : {
                "Critical Damage" : 2,
                "Damage" : 3,
                "Health" : 0,
                "Critical Chance" : 1,
                "Damage Reduction" : 0
            },
        "Warrior" : {
                "Critical Damage" : 0,
                "Damage" : 2,
                "Health" : 3,
                "Critical Chance" : 0,
                "Damage Reduction" : 1
            },
        "Bruiser" : {
                "Critical Damage" : 0,
                "Damage" : 1,
                "Health" : 3,
                "Critical Chance" : 0,
                "Damage Reduction" : 2
            },
        "Scout" : {
                "Critical Damage" : 2,
                "Damage" : 3,
                "Health" : 0,
                "Critical Chance" : 1,
                "Damage Reduction" : 0
            }
        
    }

def readCSVFile(filename):
    csv_path = str(PATH)+str(filename)+'.csv'
    file_csv = open(csv_path,'r')
    result = file_csv.read().split("\n")
    file_csv.close()
    return result

def setOnDictBadges(mappingBadges, listOfBadges):
    dictBadges = {}
    for elt in listOfBadges:
        splittedBadge = elt.split(";")
        if splittedBadge[0] != "":
            dictBadges[splittedBadge[0]] = {
                mappingBadges[1] : splittedBadge[1],
                mappingBadges[2] : splittedBadge[2],
                mappingBadges[3] : splittedBadge[3],
                mappingBadges[4] : splittedBadge[4],
                mappingBadges[5] : splittedBadge[5],
                mappingBadges[6] : splittedBadge[6],
                mappingBadges[7] : splittedBadge[7],
                mappingBadges[8] : splittedBadge[8],
                mappingBadges[9] : splittedBadge[9],
                }
    return dictBadges

def setOnDictSurvivors(survivor1, survivor2, survivor3):
    dictSurvivor = {}
    for survivor in [survivor1, survivor2, survivor3]:
        survivor.remove("Field;Value")
        name_survivor = survivor[0].split(";")[1]
        for elt in survivor:
            splittedSurvivor = elt.split(";")
            try:
                dictSurvivor[name_survivor][splittedSurvivor[0]] = splittedSurvivor[1]
            except:
                if not elt == "":
                    dictSurvivor[name_survivor] = { splittedSurvivor[0] : splittedSurvivor[1] }
        dictSurvivor[name_survivor].pop("Name")
    return dictSurvivor

def getPossibleCombos(dictBadges, dictSurvivor):
    liste_west = []
    liste_south_west = []
    liste_north_west = []
    liste_east = []
    liste_north_east = []
    liste_south_east = []
    for elt in dictBadges.keys():
        if dictBadges[elt]["Orientation"] == "W":
            liste_west.append(elt)
        elif dictBadges[elt]["Orientation"] == "NW":
            liste_north_west.append(elt)
        elif dictBadges[elt]["Orientation"] == "SW":
            liste_south_west.append(elt)
        elif dictBadges[elt]["Orientation"] == "E":
            liste_east.append(elt)
        elif dictBadges[elt]["Orientation"] == "NE":
            liste_north_east.append(elt)
        elif dictBadges[elt]["Orientation"] == "SE":
            liste_south_east.append(elt)
    listCombinaisonsID = list(itertools.product(liste_west, liste_south_west, liste_north_west, liste_east, liste_north_east, liste_south_east))
    for elt in listCombinaisonsID:
        effects = []
        for idBadge in elt:
            effects.append(dictBadges[idBadge]["Effect"])
        cpt = Counter(effects)
        for type_effect in cpt.keys():
            if cpt[type_effect] > 3:
                listCombinaisonsID.remove(elt)
                
    prioritySortedCombos = []
    for elt in listCombinaisonsID:
        rarety = []
        for idBadge in elt:
            rarety.append(dictBadges[idBadge]["Rarety"])
        cpt = Counter(rarety)
        priority = 0
        for rarety in cpt.keys():
            priority += int(cpt[rarety])*int(rarety)
        prioritySortedCombos.append((elt,priority))
    
    listOfClasses = []
    for elt in dictSurvivor.keys():
        listOfClasses.append(dictSurvivor[elt]["Class"])
    
    priorityCombosByClass = []    
    for badgeSetWithPriority in prioritySortedCombos:
        badgeSet = badgeSetWithPriority[0]
        for class_survivor in listOfClasses:
            priority = 0
            for idBadge in badgeSet:
                type_effect = dictBadges[idBadge]["Effect"]
                priority += int(dictPriorities[class_survivor][type_effect])
            priority = priority + badgeSetWithPriority[1]
            priorityCombosByClass.append((priority, class_survivor, badgeSet))
    
    priorityCombosPerBonus = []
    for badgeSet in priorityCombosByClass:
        letter = []
        for idBadge in badgeSet[2]:
            letter.append(dictBadges[idBadge]["Letter"])
        cpt = Counter(letter)
        for letter in cpt.keys():
            if cpt[letter] > 3:
                priority = 10 + badgeSet[0]
            else:
                priority = badgeSet[0]
        priorityCombosPerBonus.append((priority,badgeSet[1],badgeSet[2]))
    
    finalCombos = []
    for badgeSet in priorityCombosPerBonus:
        priority = badgeSet[0]
        for idBadge in badgeSet[2]:
            bonus = dictBadges[idBadge]["Activation Bonus"]
            survivors_concerned = []
            for survivor in dictSurvivor.keys() :
                if dictSurvivor[survivor]["Class"] == badgeSet[1]:
                    survivors_concerned.append(survivor)
            for survivor in survivors_concerned:
                bonus_list = []
                for teammate in dictSurvivor.keys():
                    if not teammate == survivor:
                        bonus_list.append(teammate)
                        bonus_list.append(dictSurvivor[teammate]["Class"])
                for param in dictSurvivor[survivor]:
                    if param.startswith("Trait"):
                        bonus_list.append(dictSurvivor[survivor][param])
                if bonus in bonus_list:
                    priority += 1
                list_to_check = (survivor, priority-1, badgeSet[2])
                if list_to_check in finalCombos:
                    finalCombos.remove(list_to_check)
                finalCombos.append((priority, survivor, badgeSet[2]))
    finalCombos = list(set(finalCombos))
    finalCombos.sort(reverse=True)
    return finalCombos

def createSetsOfBadgesFor3Survivors(listPossibleCombos):
    dictBadgesSetPerSurvivor = {}
    list_survivors = []
    for survivor in dictSurvivor.keys():
        list_survivors.append(survivor)
        dictBadgesSetPerSurvivor[survivor] = []
    for badgeSet in listPossibleCombos:
        priority = badgeSet[0]
        survivor = badgeSet[1]
        setOfBadges = badgeSet[2]
        dictBadgesSetPerSurvivor[survivor].append(setOfBadges)

    
    
    
                
if __name__ == "__main__":
    listOfBadges = readCSVFile("badges")
    survivor1 = readCSVFile("survivor1")
    survivor2 = readCSVFile("survivor2")
    survivor3 = readCSVFile("survivor3")
    mappingBadges = listOfBadges[0].split(";")
    listOfBadges.remove(listOfBadges[0])
    dictBadges = setOnDictBadges(mappingBadges, listOfBadges)
    dictSurvivor = setOnDictSurvivors(survivor1, survivor2, survivor3)
    listPossibleCombos = getPossibleCombos(dictBadges, dictSurvivor)
    listSetsOfBadges = createSetsOfBadgesFor3Survivors(listPossibleCombos)