import xlrd

path = r'C:\Users\SynthesisDNASCRIPT\Desktop\Proto6\Quartet_Control.xlsm'

#Parameters

stirVel=0
firstRemoval=0
atTheEnd=0
PremixVolume=0
NucsVolume=0
EBVolume=0
DBVolume1=0
DBVolume2=0
WashVolume=0
BBVolume1=0
BBVolume2=0
VolumesSheet=0
Elong_time=0
VacuumTime=0
BBTime=0
DBTime=0
WashTime=0
params=[stirVel,firstRemoval,atTheEnd,PremixVolume,DBVolume1,DBVolume2,WashVolume,BBVolume1,BBVolume2,VolumesSheet,Elong_time,VacuumTime,BBTime,DBTime,WashTime]

def getExcelSheet(path):
    wb = xlrd.open_workbook(path)
    synthesis_sheet = wb.sheet_by_name("Syntheses")
    return synthesis_sheet

def getSequences(synthesis_sheet):

    sequences=[]
    well=1
    for col in range(12):
        for row in range(8):
            value=synthesis_sheet.cell_value(7+row,1+col)
            if value!='':
                sequences.append((well,value))
            well+=1

    return sequences

def splitSequences(sequences,cycle):

    ended_wells = []
    A_wells=[]
    C_wells=[]
    G_wells=[]
    T_wells=[]
    M_wells=[]
    N_wells=[]
    O_wells=[]
    P_wells=[]
    X_wells=[]

    nucleos=['A','C','G','T','M','N','O','P','X']
    nucleo_arrays=[ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells]

    for nucleo in range(1,9+1):
        for sample in range(len(sequences)):
            if (cycle<=len(sequences[sample][1]) and sequences[sample][1][cycle-1]==nucleos[nucleo-1]):
                nucleo_arrays[nucleo].append(sequences[sample][0])

    for sample in range(len(sequences)):
        if cycle > len(sequences[sample][1]):
            ended_wells.append(sequences[sample][0])

    return nucleo_arrays

def splitSequencesDegenerate(sequences,cycle):

    ended_wells = []
    A_wells=[]
    C_wells=[]
    G_wells=[]
    T_wells=[]

    nucleo_arrays=[ended_wells,A_wells,C_wells,G_wells,T_wells]


    for sample in range(len(sequences)):
        arrays_to_fill=[]
        if (cycle<=len(sequences[sample][1])):
            letter=sequences[sample][1][cycle-1]
            if letter=="A":
                arrays_to_fill = [A_wells]
            if letter=="C":
                arrays_to_fill = [C_wells]
            if letter=="G":
                arrays_to_fill = [G_wells]
            if letter=="T":
                arrays_to_fill = [T_wells]
            if letter == "R":
                arrays_to_fill = [A_wells,G_wells]
            if letter == "Y":
                arrays_to_fill = [C_wells, T_wells]
            if letter == "S":
                arrays_to_fill = [G_wells, C_wells]
            if letter == "W":
                arrays_to_fill = [A_wells, T_wells]
            if letter == "K":
                arrays_to_fill = [G_wells, T_wells]
            if letter == "M":
                arrays_to_fill = [A_wells, C_wells]
            if letter == "B":
                arrays_to_fill = [C_wells, G_wells, T_wells]
            if letter == "D":
                arrays_to_fill = [A_wells, G_wells, T_wells]
            if letter == "H":
                arrays_to_fill = [A_wells, C_wells, T_wells]
            if letter == "V":
                arrays_to_fill = [A_wells, C_wells, G_wells]
            if letter == "N":
                arrays_to_fill = [A_wells,C_wells, G_wells, T_wells]

            if arrays_to_fill != []:
                for array in arrays_to_fill:
                    array.append([sequences[sample][0],len(arrays_to_fill)])

    for sample in range(len(sequences)):
        if cycle > len(sequences[sample][1]):
            ended_wells.append(sequences[sample][0])

    return nucleo_arrays

def getUsedWells(sequences):
    #returns all the wels in the synthesis
    usedWells=[]
    for sample in sequences:
        usedWells.append(sample[0])
    return usedWells

def getActiveWells(sequences,cycle):
    #Return all the wells in the synthesis minus the finished ones
    usedWells=getUsedWells(sequences)
    ended_wells=splitSequences(sequences,cycle)[0]
    activeWells=[]

    for well in usedWells:
        if well not in ended_wells:
            activeWells.append(well)

    return activeWells

def getActiveWellsButX(sequences,cycle):
    #Return all the wells in the synthesis minus the finished ones
    usedWells=getUsedWells(sequences)
    ended_wells=splitSequences(sequences,cycle)[0]
    X_wells=splitSequences(sequences,cycle)[9]
    activeWells=[]

    for well in usedWells:
        if (well not in ended_wells) and (well not in X_wells):
            activeWells.append(well)

    return activeWells

def getEndedWellsPlusX(sequences,cycle):
    #Return all the wells in the synthesis minus the finished ones
    usedWells=getUsedWells(sequences)
    ended_wells=splitSequences(sequences,cycle)[0]
    X_wells = splitSequences(sequences, cycle)[9]
    activeWells=[]

    for well in X_wells:
        ended_wells.append(well)

    return ended_wells

def findIndexes(eltToFind,synthesis_sheet):

    for row in range(synthesis_sheet.nrows):
        for col in range(synthesis_sheet.ncols):
            if synthesis_sheet.cell_value(row,col)==eltToFind:
                return (row,col)

'''
def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())

'''

def inter(listOfListsOfWell):

    final_list=listOfListsOfWell[0]
    for wellList in listOfListsOfWell:
        final_list=[well for well in final_list if well in wellList]

    return final_list

def union(listOfListsOfWell):

    final_list=[]
    for wellList in listOfListsOfWell:
        for well in wellList:
            if well not in final_list:
                final_list.append(well)

    return final_list

if __name__ == "__main__":

    synthesis_sheet=getExcelSheet(path)
    sequences=getSequences(synthesis_sheet)
    print(sequences)

    print(getEndedWellsPlusX(sequences,1))
    #params=getParameters(synthesis_sheet)
    #print(getUsedWells(sequences))
    #print(getActiveWells(sequences,4))