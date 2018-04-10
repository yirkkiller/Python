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

def eliminateBadgesNotIntersting(dictSurvivor, dictBadges):
    listOfClasses = []
    for elt in dictSurvivor.keys():
        if not dictSurvivor[elt]["Class"] in listOfClasses:
            listOfClasses.append(dictSurvivor[elt]["Class"])
    
    priorityByClass = {}
    for badge in dictBadges.keys():
        for class_survivor in listOfClasses:
            type_effect = dictBadges[badge]["Effect"]
            priority_badge = int(dictPriorities[class_survivor][type_effect])
            if not priority_badge == 0:
                if not class_survivor in priorityByClass.keys():
                    priorityByClass[class_survivor] = [badge]
                else:
                    if badge not in priorityByClass[class_survivor]:
                        priorityByClass[class_survivor].append(badge)

    return priorityByClass, listOfClasses

def createCombosPerSurvivor(priorityByClass, listOfClasses, dictBadges, dictSurvivor):
    badges_survivor1 = []
    badges_survivor2 = []
    badges_survivor3 = []
    
    survivor1 = dictSurvivor.keys()[0]
    class_survivor1 = dictSurvivor[survivor1]["Class"]
    survivor2 = dictSurvivor.keys()[1]
    class_survivor2 = dictSurvivor[survivor2]["Class"]
    survivor3 = dictSurvivor.keys()[2]
    class_survivor3 = dictSurvivor[survivor3]["Class"]
    badges_survivor1 = priorityByClass[class_survivor1]
    badges_survivor2 = priorityByClass[class_survivor2]
    badges_survivor3 = priorityByClass[class_survivor3]

    return badges_survivor1, badges_survivor2, badges_survivor3, survivor1, survivor2, survivor3


def getPossibleCombos(survivor, badges_survivor, dictBadges, dictSurvivor):
    liste_west = []
    liste_south_west = []
    liste_north_west = []
    liste_east = []
    liste_north_east = []
    liste_south_east = []

    for elt in badges_survivor:
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
    listCombinaisons_survivor = list(itertools.product(liste_west, liste_south_west, liste_north_west, liste_east, liste_north_east, liste_south_east))
    
    for elt in listCombinaisons_survivor:
        ### Test
            
        if '5' in elt:
            if '11' in elt:
                if '13' in elt:
                    if '15' in elt:
                        if '17' in elt:
                            if '24' in elt:
                                print elt
        
        ### End Test
        
        effects = []
        for idBadge in elt:
            effects.append(dictBadges[idBadge]["Effect"])
        cpt = Counter(effects)
        for type_effect in cpt.keys():
            sorted_test = sorted(elt)
            if cpt[type_effect] > 3:
                listCombinaisons_survivor.remove(elt)
                
    prioritySortedCombos = []
    for elt in listCombinaisons_survivor:
        rarety = []
        for idBadge in elt:
            rarety.append(dictBadges[idBadge]["Rarety"])
        cpt = Counter(rarety)
        priority = 0
        for rarety in cpt.keys():
            priority += int(cpt[rarety])*int(rarety)
        prioritySortedCombos.append((elt,priority))
    
    priorityCombosByClass = []   
    class_survivor = dictSurvivor[survivor]["Class"]

    for badgeSetWithPriority in prioritySortedCombos:
        badgeSet = badgeSetWithPriority[0]
        priority = 0
        for idBadge in badgeSet:
            type_effect = dictBadges[idBadge]["Effect"]
            priority_badge = int(dictPriorities[class_survivor][type_effect])
            priority += priority_badge
        priority = priority + badgeSetWithPriority[1]
        priorityCombosByClass.append((priority, badgeSet))
    
    priorityCombosPerBonus = []
    for badgeSet in priorityCombosByClass:
        letter = []
        for idBadge in badgeSet[1]:
            letter.append(dictBadges[idBadge]["Letter"])
        cpt = Counter(letter)
        for letter in cpt.keys():
            if cpt[letter] > 3:
                priority = 10 + badgeSet[0]
            else:
                priority = badgeSet[0]
        priorityCombosPerBonus.append((priority,badgeSet[1]))
    
    return priorityCombosPerBonus

def eliminateLowAverageSets(badgeSet, numberOfBadgesSets):
    newbadgeSet = badgeSet
    while len(newbadgeSet) > numberOfBadgesSets:
        priorities_survivor = 0
        temp_badgeSet = []
        for elt in newbadgeSet:
            priorities_survivor+= elt[0]
        moyenne_survivor = priorities_survivor/len(newbadgeSet)
                    
        for elt in newbadgeSet:
            if elt[0] > moyenne_survivor:
                temp_badgeSet.append(elt)
        newbadgeSet = temp_badgeSet
            
    return newbadgeSet
    

def createSetsOfBadgesFor3Survivors(name_survivor1, name_survivor2, name_survivor3, listPossibleCombos_survivor1, listPossibleCombos_survivor2, listPossibleCombos_survivor3):
    list_CombosSurvivors = []
        
    for elt_survivor3 in sorted(listPossibleCombos_survivor3, reverse=True):
        if list_CombosSurvivors != [] :
            break
        set_badge_survivor3 = set(elt_survivor3[1])
        for elt_survivor2 in sorted(listPossibleCombos_survivor2, reverse=True):
            if list_CombosSurvivors != [] :
                break
            set_badge_survivor2 = set(elt_survivor2[1])
            for elt_survivor1 in sorted(listPossibleCombos_survivor1, reverse=True):
                set_badge_survivor1 = set(elt_survivor3[1])
                liste_badges = elt_survivor1[1]+elt_survivor2[1]+elt_survivor3[1]
                set_badges = set(liste_badges)
                if len(liste_badges) == len(set_badges):
                    priority_survivor1 = int(elt_survivor1[0])
                    priority_survivor2 = int(elt_survivor2[0])
                    priority_survivor3 = int(elt_survivor3[0])
                    priority = priority_survivor1+priority_survivor2+priority_survivor3
                    list_CombosSurvivors.append((priority, ((name_survivor1, elt_survivor1[1]), (name_survivor2, elt_survivor2[1]), (name_survivor3, elt_survivor3[1]))))
                    if list_CombosSurvivors != [] :
                        break
    return  list_CombosSurvivors

def prepareCSV(listSetsOfBadges, dictBadges):
    setsOfBadges_survivor1 = listSetsOfBadges[0][1][0][1]
    setsOfBadges_survivor2 = listSetsOfBadges[0][1][1][1]
    setsOfBadges_survivor3 = listSetsOfBadges[0][1][2][1]
    name_survivor1 = listSetsOfBadges[0][1][0][0]
    name_survivor2 = listSetsOfBadges[0][1][1][0]
    name_survivor3 = listSetsOfBadges[0][1][2][0]
    
    csvString = ""
    firstLine = "Survivor;BadgeID;Letter;Rarety;Effect;Orientation;Value;%/Value;Bonus;%/Value Bonus;Activation Bonus\n"
    csvString += firstLine
    
    for badge in setsOfBadges_survivor1:
         csvString += createLineBadge(badge, dictBadges, name_survivor1)
    for badge in setsOfBadges_survivor2:
         csvString += createLineBadge(badge, dictBadges, name_survivor2)
    for badge in setsOfBadges_survivor3:
         csvString += createLineBadge(badge, dictBadges, name_survivor3)
    
    return csvString
    
def createLineBadge(badge, dictBadges, nameSurvivor):
    letter = dictBadges[badge]["Letter"]
    rarety = dictBadges[badge]["Rarety"]
    effect = dictBadges[badge]["Effect"]
    orientation = dictBadges[badge]["Orientation"]
    value = dictBadges[badge]["Value"]
    type_value = dictBadges[badge]["%/Value"]
    bonus = dictBadges[badge]["Bonus"]
    type_value_bonus = dictBadges[badge]["%/Value Bonus"]
    activation_bonus = dictBadges[badge]["Activation Bonus"]
    
    lineString = nameSurvivor+";"
    lineString += badge+";"
    lineString += letter+";"
    lineString += rarety+";"
    lineString += effect+";"
    lineString += orientation+";"
    lineString += value+";"
    lineString += type_value+";"
    lineString += bonus+";"
    lineString += type_value_bonus+";"
    lineString += activation_bonus+"\n"
    
    return lineString

def createCSV(csv_string):
    csv_path = str(PATH)+'output.csv'
    file_csv = open(csv_path,'w')
    file_csv.write(csv_string)
    file_csv.close()


if __name__ == "__main__":
    listOfBadges = readCSVFile("badges")
    survivor1 = readCSVFile("survivor1")
    survivor2 = readCSVFile("survivor2")
    survivor3 = readCSVFile("survivor3")
    mappingBadges = listOfBadges[0].split(";")
    listOfBadges.remove(listOfBadges[0])
    dictBadges = setOnDictBadges(mappingBadges, listOfBadges)
    dictSurvivor = setOnDictSurvivors(survivor1, survivor2, survivor3)
    badgesPerClass, listOfClasses = eliminateBadgesNotIntersting(dictSurvivor, dictBadges)
    badges_survivor1, badges_survivor2, badges_survivor3, survivor1, survivor2, survivor3 = createCombosPerSurvivor(badgesPerClass, listOfClasses, dictBadges, dictSurvivor)
    listPossibleCombos_survivor1 = getPossibleCombos(survivor1, badges_survivor1, dictBadges, dictSurvivor)
    listPossibleCombos_survivor2 = getPossibleCombos(survivor2, badges_survivor2, dictBadges, dictSurvivor)
    listPossibleCombos_survivor3 = getPossibleCombos(survivor3, badges_survivor3, dictBadges, dictSurvivor)
    numberOfBadgesSets = 560
    listSetsOfBadges = None
    while listSetsOfBadges == None:
        listCombos_survivor1 = eliminateLowAverageSets(listPossibleCombos_survivor1, numberOfBadgesSets)
        listCombos_survivor2 = eliminateLowAverageSets(listPossibleCombos_survivor2, numberOfBadgesSets)
        listCombos_survivor3 = eliminateLowAverageSets(listPossibleCombos_survivor3, numberOfBadgesSets)
        listSetsOfBadges = createSetsOfBadgesFor3Survivors(survivor1, survivor2, survivor3, listCombos_survivor1, listCombos_survivor2, listCombos_survivor3)
        numberOfBadgesSets += 10
    csv_string = prepareCSV(listSetsOfBadges, dictBadges)
    createCSV(csv_string)