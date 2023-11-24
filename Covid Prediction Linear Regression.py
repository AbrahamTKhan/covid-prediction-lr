import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

newdf = pd.read_csv('data_2021-Nov-28.csv')

new = np.array(newdf[["newCasesBySpecimenDate"]])
new = new[::-1]


newdays = np.array(newdf["date"])
newdates = np.array([[1]])
for x in range(2, 667, 1):
    newdates = np.concatenate((newdates,[[x]]))

newdatesp = np.split(newdates, [120,230,380, 500, 600, 666])
newesp = np.split(new, [120,230,380, 500, 600, 666])
newreg = [0]
for i in range(0, 6, 1):
    newxmean = newdatesp[i].mean()
    newdiffx = np.array(newxmean - newdatesp[i])
    newdiffxsquared = np.array(newdiffx**2)
    newSSxx = newdiffxsquared.sum()

    newymean = newesp[i].mean()
    newdiffy = np.array(newymean - newesp[i])
    newSSxy = (newdiffx * newdiffy).sum()

    newm = newSSxy/newSSxx
    newb = newymean - newm*newxmean

    newreg.append(newm*newxmean+newb)

newpiece = [0,60,175,305, 450, 540, 667]
newpredictx = [630, 767]
newpredicty = [newreg[6],newm*767+newb]
###########################################################
caseFN = 'data_2022-Feb-25.csv'
casedf = pd.read_csv(caseFN) #Makes a data frame from the specified file name for cases

cases = np.array(casedf[["newCasesBySpecimenDate"]])
cases = cases[::-1] #Selects the column that holds the cases and reverses it

casesdays = np.array(casedf["date"])
casesdays = casesdays[::-1]
caseSize = len(casesdays)-1
casedates = np.array([[1]])
for x in range(2, caseSize+1, 1):
    casedates = np.concatenate((casedates,[[x]])) #Initialises variables holding values for the dates and size

casedatesp = np.split(casedates, [120,230,380, 500, 600, 660, 730,caseSize])
casesp = np.split(cases, [120,230,380, 500, 600, 660, 730,caseSize]) #Creates arrays for the piecewise splits
reg = [0]
caseSlopeIntercept = []
for i in range(0, 8, 1):
    xmean = casedatesp[i].mean()
    diffx = np.array(xmean - casedatesp[i])
    diffxsquared = np.array(diffx**2)
    SSxx = diffxsquared.sum() #Calculates the SSxx of each piece

    ymean = casesp[i].mean()
    diffy = np.array(ymean - casesp[i])
    SSxy = (diffx * diffy).sum() #Calculates the SSxy of each piece

    m = SSxy/SSxx
    b = ymean - m*xmean #Creates the slope and intercept of each piece
    caseSlopeIntercept.append([m,b])
    reg.append(m*xmean+b) #Creates each piecewise point

casepiece = [0,60,175,305, 450, 540, 650, 690, caseSize] #Creates array for the x value points of each split


deathdf = pd.read_csv('data_2022-Feb-25 (1).csv') #Repeats the above process for deaths

deaths = np.array(deathdf[["newDeaths28DaysByDeathDate"]])
deaths = deaths[::-1]


deathdays = np.array(deathdf["date"])
deathdays = deathdays[::-1]
deathSize = len(deathdays)-1
deathdates = np.array([[1]])
for x in range(2, deathSize+1, 1):
    deathdates = np.concatenate((deathdates,[[x]]))

deathdatesp = np.split(deathdates, [90,210,380, 500, 600, 650, 720, deathSize])
deathsp = np.split(deaths, [90,210,380, 500, 600, 650, 720,deathSize])
deathreg = [0]
for i in range(0, 8, 1):
    deathxmean = deathdatesp[i].mean()
    deathdiffx = np.array(deathxmean - deathdatesp[i])
    deathdiffxsquared = np.array(deathdiffx**2)
    deathSSxx = diffxsquared.sum()

    deathymean = deathsp[i].mean()
    deathdiffy = np.array(deathymean - deathsp[i])
    deathSSxy = (deathdiffx * deathdiffy).sum()

    deathm = deathSSxy/deathSSxx
    deathb = deathymean - deathm*deathxmean

    deathreg.append(deathm*deathxmean+deathb)

deathpiece = [0,45,150,335, 440, 550, 625, 685, deathSize]

root = Tk() #Creates the initial elements for the UI
Label(root,text="Covid-19 Modelling and Forecast Tool",font=("Arial", 44)).pack()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 5))

canvas = FigureCanvasTkAgg(fig, master=root) #Canvas for updating subplots
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, root) 

def test_equal():
    assert reg[1] == 2065.366666666667
    assert m == -2287.527521367522
    assert deathm == -0.07658119658119658
def test_x():
    assert caseSize == 756
    assert deathSize == 724
    assert caseFN == 'data_2022-Feb-25.csv'

if __name__ == "__main__": #Unit testing to verify the validaty of the program
    test_equal()
    test_x()
    print("Everything passed")


caseSlopePredict = (caseSlopeIntercept[3][0]+caseSlopeIntercept[4][0]+caseSlopeIntercept[5][0]+caseSlopeIntercept[6][0]+caseSlopeIntercept[7][0])/5
caseInterceptPredict = (caseSlopeIntercept[5][1]+caseSlopeIntercept[4][1]+caseSlopeIntercept[5][1]+caseSlopeIntercept[6][1]+caseSlopeIntercept[7][1])/5
def draw_chart(): #Function that displays all the data on the subplots
    predictDays = 100
    if(predictInput.get() == "2 weeks"):
        predictDays = 14
    if (predictInput.get() == "1 month"):
        predictDays = 30
    if (predictInput.get() == "3 months"):
        predictDays = 90
    if (predictInput.get() == "6 months"):
        predictDays = 180
    if (predictInput.get() == "1 year"): #Changes number of predicted days based on input
        predictDays = 365
    deathpredictx = [deathSize, deathSize + predictDays]
    deathpredicty = [deathreg[8],deathm*(deathSize + predictDays)+deathb] #Creates lists for plotting the predictions
    casepredictx = [caseSize, caseSize + predictDays]
    casepredicty = [reg[8],caseSlopePredict*(caseSize + predictDays)+caseInterceptPredict]
    
    ax1.clear()
    ax1.set_title('Cases')
    ax1.set_xlabel('Time in Days')
    ax1.set_ylabel('# of Daily Infections')
    ax1.plot(casesdays,cases)
    ax1.plot(casepiece,reg, 'r')
    ax1.plot(casepredictx,casepredicty,'g')
    ax1.plot([caseSize,caseSize],[0,275000], 'g') #Refreshes and replots the subplots

    ax1.plot(newpredictx, newpredicty, 'y')
    ax1.plot([630, 630],[0,275000], 'y')
    
    ax2.clear()
    ax2.set_title('Deaths')
    ax2.set_xlabel('Time in Days')
    ax2.set_ylabel('# of Daily Infections')
    ax2.plot(deathdays,deaths)
    ax2.plot(deathpiece,deathreg, 'r')
    ax2.plot(deathpredictx,deathpredicty,'g')
    ax2.plot([deathSize,deathSize],[0,1500], 'g')
    
    if (caseInput.get() == "2 weeks"):
        ax1.set_xticks(ax1.get_xticks()[::6])
        ax1.set_xlim(xmin=caseSize-14,xmax=caseSize+25)
        ax2.set_xticks(ax2.get_xticks()[::6])
        ax2.set_xlim(xmin=deathSize-14,xmax=deathSize+25)
    if (caseInput.get() == "1 month"):
        ax1.set_xticks(ax1.get_xticks()[::10])
        ax1.set_xlim(xmin=caseSize-30,xmax=caseSize+40)
        ax2.set_xticks(ax2.get_xticks()[::10])
        ax2.set_xlim(xmin=deathSize-30,xmax=deathSize+40)
    if (caseInput.get() == "3 months"):
        ax1.set_xticks(ax1.get_xticks()[::20])
        ax1.set_xlim(xmin=caseSize-90,xmax=caseSize+65)
        ax2.set_xticks(ax2.get_xticks()[::20])
        ax2.set_xlim(xmin=deathSize-90,xmax=deathSize+65) #Adjusts the zoom and ticks based on user input
    if (caseInput.get() == "6 months"):
        ax1.set_xticks(ax1.get_xticks()[::40])
        ax1.set_xlim(xmin=caseSize-180, xmax=caseSize+85)
        ax2.set_xticks(ax2.get_xticks()[::40])
        ax2.set_xlim(xmin=deathSize-180, xmax=deathSize+85)
    if (caseInput.get() == "1 year"):
        ax1.set_xticks(ax1.get_xticks()[::80])
        ax1.set_xlim(xmin=caseSize-365, xmax=caseSize+100)
        ax2.set_xticks(ax2.get_xticks()[::80])
        ax2.set_xlim(xmin=deathSize-365, xmax=deathSize+100)
    if(caseInput.get() == "All"):
        ax1.set_xticks(ax1.get_xticks()[::150])
        ax1.set_xlim(xmin=0, xmax=caseSize+predictDays+5)
        ax2.set_xticks(ax2.get_xticks()[::144])
        ax2.set_xlim(xmin=0, xmax=deathSize+predictDays+5)
        
    global label1
    global label2
    global label3
    label1["text"] = "Total Days Predicted: \n" + str(predictDays) + " days"
    label2["text"] = "Average Cases Predicted per Day: \n" + str(round(sum(casepredicty)/len(casepredicty),2))
    label3["text"] = "Average Deaths Predicted per Day: \n" + str(round(sum(deathpredicty)/len(deathpredicty),2)) #Refreshes the statistics labels
    canvas.draw_idle()
   
Button(root,text="Update Timeframe",command=draw_chart,height=2, width=20, font="Verdana 9").pack() #Creates button

caseInput = tk.StringVar()
predictInput = tk.StringVar()
case_cb = ttk.Combobox(root, textvariable=caseInput)
case_cb['values'] = ["2 weeks", "1 month", "3 months", "6 months", "1 year", "All"]
case_cb.current(5)
death_cb = ttk.Combobox(root, textvariable=predictInput)
death_cb['values'] = ["2 weeks", "1 month", "3 months", "6 months", "1 year"] #Creates comboboxes
death_cb.current(3)
case_cb['state'] = 'readonly'
death_cb['state'] = 'readonly'

caseLabel = Label(root,text="Select Logged Timeframe:")
caseLabel.pack(side=LEFT,padx=(250,5))
case_cb.pack(side=LEFT)
death_cb.pack(side=RIGHT,padx=(5,225))
deathLabel = Label(root,text="Select Prediction Timeframe:") #Packs comboboxes and complementary label
deathLabel.pack(side=RIGHT)

label1 = Label(root,text="")
label1.pack(pady=(10,0))
label2 = Label(root,text="") #Creates placeholder statistic labels
label2.pack()
label3 = Label(root,text="")
label3.pack()

root.mainloop()
