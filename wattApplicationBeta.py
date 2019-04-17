from tkinter import *
from tkinter.ttk import *
import os
import pyodbc
import time

window = Tk()
window.title("Welcome to WATT")
window.geometry('650x250')
window.config(background='#C70039')
# tab 1: entryies
tab_control = Notebook(window)
tab1 = Frame(tab_control)
tab_control.add(tab1, text='Task Entry')

# tab 2: Daily WATT - select from today's stuffs

# table for settings, pull in

# gets value options from DB
username = os.getlogin()
# serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\TAPE_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\' + username.upper() + '_LOCAL;Database=WATTapplication;Trusted_Connection=yes'

taskTypes = {
    1: 'Files',
    2: 'Inquiries',
    3: 'Emails',
    4: 'Review',
    5: 'Call',
    6: 'Meeting'
}

def update_clock():
    now = time.strftime("%H:%M:%S")
    clockLabel.configure(text=now)
    window.after(1000, update_clock)

def selected(event):


    taskTypeid = combo.get()
    taskTypeName = taskTypes.get(int(taskTypeid), 'unknown')
    lbl.configure(text = taskTypeName)

def clicked():
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    taskTypeid = combo.get()
    clientCode = clientCodeTxt.get()
    startDateTime = time.strftime("%Y-%m-%d %H:%M:%S")
    sqlStatement = "INSERT INTO watt.task (taskTypeId,clientCode,taskNote, startedAtTime) VALUES (" + taskTypeid + ",'" + clientCode + "','" + taskNoteTxt.get() + "','" + startDateTime + "')"
    print(sqlStatement)
    cursor.execute(sqlStatement)
    conn.commit()
    conn.close()
    lbl.configure(text= "updated!")
    # taskNoteTxt.set("")
    # clientCodeTxt.set("")
    # clear text fields

# theme combo selected event

clockLabel = Label(text="")
# clockLabel.pack()
update_clock()

combo = Combobox(window)
combo['values']= (1,2,3,4,5,6)
# combo.current(0)
combo.bind("<<ComboboxSelected>>", selected)

lbl = Label(window,text="Hello, " + username +"!", font=("Arial Bold", 10))
taskNotelbl = Label(window,text="Task Note", font=("Arial", 8))
clientCodelbl = Label(window,text="Code", font=("Arial", 8))
taskNoteTxt = Entry(window,width=20)
clientCodeTxt = Entry(window,width=20)
btn = Button(window, text="Start Task", command=clicked, width=40)

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
# Current Queue/Duration Row



window.mainloop()
