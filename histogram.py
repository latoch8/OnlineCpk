import matplotlib.pyplot as plt
import numpy as np
import os, glob, shutil, copy, time
import matplotlib.mlab as mlab

logsFormat = "res"
logsDir = "../*."+logsFormat
tempLogsDir = "temp/"
howManyDut = 1
delimiter = ";"
iniDelimiter = delimiter
testNameINI = "testsToPlot.txt"
refreshTime = 60 #w sekundach
testPass = 0
testAll = 0

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
    # global ctime
    #fpy calculate
    global testPass, testAll
    testPass = 0
    testAll = 0
    filesList = os.listdir(tempLogsDir)
    print(filesList)
    # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(tempLogsDir + filesList[0])
    for fileName in filesList:
        fileDir = tempLogsDir + fileName
        with open(fileDir) as f:
            lines = f.read().splitlines()
            for line in lines:
                allColumns = line.split(delimiter)
                index = 0
                testResult = allColumns[3]
                if "Pass" in testResult:
                    testAll += 1
                    testPass += 1
                elif "Fail" in testResult:
                    testAll += 1
                for oneColumn in allColumns:
                    for key in AllData:
                        if key == oneColumn: #if key is equal to test name asign next value
                            lowLimit = AllData[key]["limits"][0]
                            highLimit = AllData[key]["limits"][1]
                            value = float(allColumns[index+1])
                            if (value >= lowLimit) and (value <= 3*highLimit):
                                AllData[key]["data"].append(float(allColumns[index+1]))
                            # print(allColumns[index+1])
                    index += 1
        os.remove(fileDir)
    fpy = (testPass/testAll)*100
    fpy = round(fpy,2)
    print(fpy)
    return fpy

def prepareCharts(data):
    howManyCharts = len(data)
    col = howManyCharts
    row = 1
    fig, plot= plt.subplots(nrows=row, ncols=col)
    # mng = plt.get_current_fig_manager()
    # mng.window.state('zoomed')
    # mng.window.wm_geometry("+%d+%d" % (2000, 0))
    # mng.full_screen_toggle()
    return fig, plot

def plotData(data, fig, plot, fpy):
    # mi, sigma = 100, 15
    index = 0
    global testAll, testPass
    # plt.title("Wykres za dzień " + time.ctime(ctime))
    for key in data:
            plot[index].clear()
            print(key)
            a = data[key]["data"]
            limits = data[key]["limits"]
            lenght = len(set(a))
            plot[index].name = key
            plot[index].hist(a, bins = lenght)
            # bincenters = 0.5*(bins[1:]+bins[:-1])
            # y = mlab.normpdf( bincenters, mi, sigma)
            # l = plt.plot(bincenters, y, 'r--', linewidth=1)
            #linie pionowe
            plot[index].vlines(limits,0,1,transform=plot[index].get_xaxis_transform(), colors='r')
            #nazwy dla osi
            plot[index].set_title(key)
            index += 1
    fig.suptitle('FPY ' + str(fpy) + '%\n'+ str(testPass) + "/" + str(testAll), fontsize=18, color='blue', fontweight='bold')
    plt.pause(refreshTime)

#MAIN
onlyLimits = loadIniFile()
fig, plot = prepareCharts(onlyLimits)
try:
    while True:
        copyData() #copy newes file
        dataToPlot = copy.deepcopy(onlyLimits)
        fpy = loadData(dataToPlot) #load data from file
        plotData(dataToPlot, fig, plot, fpy)
        print(onlyLimits)
    plt.show()
except Exception as e:
	print(e)
input("Press Enter to close...")