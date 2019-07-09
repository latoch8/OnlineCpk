
import matplotlib.pyplot as plt
import numpy as np
import os, glob, shutil

logsFormat = "res"
logsDir = "../*."+logsFormat
tempLogsDir = "temp/"
howManyDut = 2
delimiter = ";"
testNameINI = "testsToPlot.txt"

def prepareData():
    #check and create folder
    if not os.path.exists(tempLogsDir):
        os.mkdir(tempLogsDir)
        print("Directory created!")
    else:
        print("Directory exist!")
    #find newes files
    files_path = os.path.join("", logsDir)
    files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 
    #copy newes files
    for i in range(howManyDut):
        # print (files[i])
        shutil.copy(files[i],tempLogsDir)

# def readAllTestName:
#     filesList = os.listdir(tempLogsDir)

def loadData():
    #load testNames to plote
    AllData = {}
    if not os.path.exists(testNameINI):
        # readAllTestName()
        open(testNameINI, 'a').close()
        print("Please fill ini file!")
    with open(testNameINI) as ini:
        testNameToPlote = ini.read().splitlines()   
        for testName in testNameToPlote:
            AllData.update({testName:[]})
    #load data
    filesList = os.listdir(tempLogsDir)
    print(filesList)
    for fileName in filesList:
        fileDir = tempLogsDir + fileName
        with open(fileDir) as f:
            lines = f.read().splitlines()
            for line in lines:
                allColumns = line.split(delimiter)
                index = 0
                for oneColumn in allColumns:
                    for key in AllData:
                        if key == oneColumn: #if key is equal to test name asign next value
                            AllData[key].append(float(allColumns[index+1]))
                            # print(allColumns[index+1])
                    index += 1
        os.remove(fileDir)
    return AllData

def plotAllData(data):
    howManyCharts = len(data)
    #dzielenie wykresow
    col = howManyCharts
    row = 1
    index = 0
    fig, plot= plt.subplots(nrows=row, ncols=col)
    for key in data:
        a = data[key]
        lenght = len(set(a))
        plot[index].name = key
        plot[index].hist(a, bins = lenght)
        index += 1
    plt.show()

#MAIN
prepareData()
dataToPlot = loadData()
plotAllData(dataToPlot)

# input("Press Enter...")