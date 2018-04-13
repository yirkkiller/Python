import itertools
from collections import Counter

PATH = "D:\\Badges\\"

# Priority of badge effects per class of survivor
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

# Read CSV class
def readCSVFile(filename):
    csv_path = str(PATH)+str(filename)+'.csv'
    file_csv = open(csv_path,'r')
    result = file_csv.read().split("\n")
    file_csv.close()
    return result

# Set the list of badges onto a dictionary
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

# Set the list of survivors and their traits onto a dictionary
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

# Eliminate badges with priority = 0 (related to GLOBAL dictionary dictPriorities)
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

# Affect a list of possible badges per survivor related to his class
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
    # In a 6 badges combination, each badge should have a unique orientation.
    liste_west = []
    liste_south_west = []
    liste_north_west = []
    liste_east = []
    liste_north_east = []
    liste_south_east = []
    
    # Set the badges into a list created by its orientation
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
    
    # Get the list of all possible combinations with right orientation (one of each orientation)
    listCombinaisons_survivor = list(itertools.product(liste_west, liste_south_west, liste_north_west, liste_east, liste_north_east, liste_south_east))
    
    # Eliminate combinations of badges where more than 3 badges on 6 have the same effect
    newlist_combinations = []
    for elt in listCombinaisons_survivor:     
        effects = []
        for idBadge in elt:
            effects.append(dictBadges[idBadge]["Effect"])
        cpt = Counter(effects)
        for type_effect in cpt.keys():
            cpt_effect = cpt[type_effect]
            if cpt_effect > 3:
                break
        if not cpt_effect > 3:
            newlist_combinations.append(elt)
    
                
    # Affect a priority to the badge based on the badge rarety (rarer = better)
    prioritySortedCombos = []
    for elt in newlist_combinations:
        rarety = []
        for idBadge in elt:
            rarety.append(dictBadges[idBadge]["Rarety"])
        cpt = Counter(rarety)
        priority = 0
        for rarety in cpt.keys():
            priority += int(cpt[rarety])*int(rarety)
        prioritySortedCombos.append((elt,priority))
    
    # Increase the badge priority related to the class of the survivor (related to the GLOBAL dictionary dictPriority)
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
    
    # Increase the badge set priority if at least 4 badges have the same letter (20% bonus) 
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

# Eliminate sets of badge with a priority lower than the total average of all sets priority.
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
    
# Create the combination of 3 badges sets, one for each survivor
# PRE-REQUISITE : One badge is unique and can only be used by only one survivor at the time
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

# Prepare string to write in the CSV
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
    # Read CSV Files : list of Badges, Traits of the 3 characters
    listOfBadges = readCSVFile("badges")
    survivor1 = readCSVFile("survivor1")
    survivor2 = readCSVFile("survivor2")
    survivor3 = readCSVFile("survivor3")
    # Retrieve name of the fields from badges CSV-extracted list
    mappingBadges = listOfBadges[0].split(";")
    listOfBadges.remove(listOfBadges[0])
    # Format the list of badges into dictionary
    dictBadges = setOnDictBadges(mappingBadges, listOfBadges)
    # Format the survivors and their traits into a dictionary
    dictSurvivor = setOnDictSurvivors(survivor1, survivor2, survivor3)
    # Eliminate the badges not interesting for the survivor, related to the GLOBAL dict dictPriorities 
    badgesPerClass, listOfClasses = eliminateBadgesNotIntersting(dictSurvivor, dictBadges)
    # Affect the badges to a survivor
    badges_survivor1, badges_survivor2, badges_survivor3, survivor1, survivor2, survivor3 = createCombosPerSurvivor(badgesPerClass, listOfClasses, dictBadges, dictSurvivor)
    # Process the list of badges to get the possible combinations of badges filtered by several criterias
    listPossibleCombos_survivor1 = getPossibleCombos(survivor1, badges_survivor1, dictBadges, dictSurvivor)
    listPossibleCombos_survivor2 = getPossibleCombos(survivor2, badges_survivor2, dictBadges, dictSurvivor)
    listPossibleCombos_survivor3 = getPossibleCombos(survivor3, badges_survivor3, dictBadges, dictSurvivor)
    # Eliminate the not interesting combinations (priority lower than the average priority)
    numberOfBadgesSets = 560
    listSetsOfBadges = None
    while listSetsOfBadges == None:
        listCombos_survivor1 = eliminateLowAverageSets(listPossibleCombos_survivor1, numberOfBadgesSets)
        listCombos_survivor2 = eliminateLowAverageSets(listPossibleCombos_survivor2, numberOfBadgesSets)
        listCombos_survivor3 = eliminateLowAverageSets(listPossibleCombos_survivor3, numberOfBadgesSets)
        # Get the better combination of badges for each of the 3 survivors
        listSetsOfBadges = createSetsOfBadgesFor3Survivors(survivor1, survivor2, survivor3, listCombos_survivor1, listCombos_survivor2, listCombos_survivor3)
        numberOfBadgesSets += 10
    # Prepare the CSV
    csv_string = prepareCSV(listSetsOfBadges, dictBadges)
    # Write the Output CSV
    createCSV(csv_string)