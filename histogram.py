import matplotlib.pyplot as plt
import numpy as np
import os, glob, shutil, copy

logsFormat = "res"
logsDir = "../*."+logsFormat
tempLogsDir = "temp/"
howManyDut = 2
delimiter = ";"
iniDelimiter = delimiter
testNameINI = "testsToPlot.txt"
refreshTime = 60 #w sekundach

def loadIniFile():
    #load testNames to plote
    AllData = {}
    if not os.path.exists(testNameINI):
        # readAllTestName()
        open(testNameINI, 'a').close()
        print("Please fill ini file!")
    with open(testNameINI) as ini:
        allLine = ini.read().splitlines() 
        for oneLine in allLine:
            data = oneLine.split(iniDelimiter)
            name = data[0]
            limits = []
            try:
                limits = [float(data[1]), float(data[2])]
            except:
                print("Lack of limits for: ", name)
            AllData.update({name:{"data":[], "limits":limits}})
    return AllData

def copyData():
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

def loadData(AllData):
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
                            AllData[key]["data"].append(float(allColumns[index+1]))
                            # print(allColumns[index+1])
                    index += 1
        os.remove(fileDir)
    return AllData

def prepareCharts(data):
    howManyCharts = len(data)
    col = howManyCharts
    row = 1
    fig, plot= plt.subplots(nrows=row, ncols=col)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    return plot

def plotData(data, plot):
    # global fig, plot, plt
    index = 0
    for key in data:
            plot[index].clear()
            print(key)
            a = data[key]["data"]
            limits = data[key]["limits"]
            lenght = len(set(a))
            plot[index].name = key
            plot[index].hist(a, bins = lenght)
            #linie pionowe
            plot[index].vlines(limits,0,1,transform=plot[index].get_xaxis_transform(), colors='r')
            #nazwy dla osi
            plot[index].set_title(key)
            index += 1
    plt.pause(refreshTime)

#MAIN
onlyLimits = loadIniFile()
plot = prepareCharts(onlyLimits)
try:
    while True:
        copyData() #copy newes file
        dataToPlot = copy.deepcopy(onlyLimits)
        loadData(dataToPlot) #load data from file
        plotData(dataToPlot, plot)
        print(onlyLimits)
    plt.show()
except Exception as e:
	print(e)
input("Press Enter to close...")