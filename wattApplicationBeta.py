from tkinter import * 
from tkinter import ttk
from tkinter import scrolledtext
import os
import pyodbc
import time

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

clockLabel = Label(tab1, text="")
# clockLabel.pack()
update_clock()

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

# Tab 2 Objects
txtBox = scrolledtext.ScrolledText(tab2,width=40,height=10)
txtBox.grid(column=0,row=0)
# Current Queue/Duration Row



window.mainloop()
