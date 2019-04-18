from tkinter import * 
from tkinter import ttk
from tkinter import scrolledtext
import os
import pyodbc
import time
import datetime

window = Tk()
window.title("Welcome to WATT")
window.geometry('650x350')

# tab 1: entryies
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
 
tab_control.add(tab1, text='   First    ')
tab_control.add(tab2, text='   Second    ')
 
lbl1 = Label(tab1, text= 'label1')
lbl1.grid(column=0, row=0)
 
lbl2 = Label(tab2, text= 'label2')
lbl2.grid(column=0, row=0)
 
tab_control.pack(expand=1, fill='both')
# tab1.config(background='#C70039')
# tab 2: Daily WATT - select from today's stuffs

# table for settings, pull in

# gets value options from DB
username = os.getlogin()

# DESTKTOP STRING
# serverString =  'Driver={SQL Server};Server=TPECK\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
serverString =  'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
# LAPTOP STRING
# serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\TAPE_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
# serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\' + username.upper() + '_LOCAL;Database=WATTapplication;Trusted_Connection=yes'



def getTaskTypeList():
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    sqlStatement = "SELECT taskTypeName FROM watt.taskType"
    cursor.execute(sqlStatement)
    global taskTypes
    taskTypes = []
    for row in cursor:
        taskTypeName = row.taskTypeName
        taskTypes.append(taskTypeName)
    conn.commit()
    conn.close()

def update_clock():
    now = time.strftime("%H:%M:%S")
    clockLabel.configure(text=now)
    window.after(1000, update_clock)

def set_timer():
    global startTime
    startTime = time.time()

    update_timer()

def update_timer():
    updatedTime = time.time()
    duration = updatedTime - startTime # seconds
    duration = time.strftime('%H:%M:%S', time.gmtime(duration) )
    # .strftime('%H:%M:%S')
    # duration = time.strftime("%H:%M:%S")
    # duration = duration.strftime('%H:%M:%S', duration)
    # duration = datetime.datetime.fromtimestamp(duration).strftime('%H:%M:%S')
    
    timerLabel.configure(text=duration)
    window.after(1000, update_timer)

def selected(event):
    taskTypeName = combo.get()
    lbl.configure(text = taskTypeName)

def clicked():
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    taskTypeName = combo.get()
    clientCode = clientCodeTxt.get()
    startDateTime = time.strftime("%Y-%m-%d %H:%M:%S")
    sqlStatement = "SELECT taskTypeId FROM WATT.taskType WHERE taskTypeName = '" + taskTypeName + "'"
    print(sqlStatement)
    cursor.execute(sqlStatement)
    for row in cursor:
        taskTypeid = row.taskTypeId

    sqlStatement = "INSERT INTO watt.worked (taskTypeId,clientCode,workedItemNote, startedAtTime) VALUES (" + str(taskTypeid) + ",'" + clientCode + "','" + taskNoteTxt.get() + "','" + startDateTime + "')"
    print(sqlStatement)
    cursor.execute(sqlStatement)
    conn.commit()
    conn.close()
    lbl.configure(text= "updated!")
    set_timer()
    # taskNoteTxt.set("")
    # clientCodeTxt.set("")
    # clear text fields

getTaskTypeList()

# theme combo selected event

clockLabel = Label(tab1, text="")
timerLabel = Label(tab1, text="")

# update_clock() # TESTING
# set_timer() # TESTING

combo = ttk.Combobox(tab1)
combo['values']= taskTypes
# (1,2,3,4,5,6)
# combo.current(0)
combo.bind("<<ComboboxSelected>>", selected)

# Tab 1 Objects
lbl = Label(tab1,text="Hello, " + username +"!", font=("Arial Bold", 10))
taskNotelbl = Label(tab1,text="Task Note", font=("Arial", 8))
clientCodelbl = Label(tab1,text="Code", font=("Arial", 8))
taskNoteTxt = Entry(tab1,width=20)
clientCodeTxt = Entry(tab1,width=20)
btn = Button(tab1, text="Start Task", command=clicked, width=25)

lbl.grid(column=0, row=0)
# Label Row 1

clientCodelbl.grid(column=1,row=1)
taskNotelbl.grid(column=2,row=1)
# Entry Row 2
combo.grid(column=0, row=2,padx=(5, 5))
clientCodeTxt.grid(column=1,row=2,padx=(5, 5))
taskNoteTxt.grid(column=2,row=2,padx=(5, 5))
btn.grid(column=3, row=2,padx=(5, 5))

clockLabel.grid(column=2,row=3)
timerLabel.grid(column=2,row=4)

# Tab 2 Objects
txtBox = scrolledtext.ScrolledText(tab2,width=40,height=10)
txtBox.grid(column=0,row=0)
# Current Queue/Duration Row



window.mainloop()
