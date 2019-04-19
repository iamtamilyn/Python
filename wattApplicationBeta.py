# from tkinter import * 
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import os
import pyodbc
import time
import datetime

# Set Window
window = tk.Tk()

window.title("WATT")
window.geometry('650x350')
window.iconbitmap('watt.ico')
window.config(background='#C70039')

# Set Style
# style = ttk.Style()
# style.theme_create( "MyStyle", parent="alt", settings={
#         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
#         "TNotebook.Tab": {"configure": {"padding": [10, 10] },}})
# style.theme_use("MyStyle")

# tab1.config(background='#C70039')

# Set Tabs
tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
 
tab_control.add(tab1, text='          Track Work         ')
tab_control.add(tab2, text='          Daily WATT         ')
tab_control.add(tab3, text='          Settings         ')
 
tab_control.pack(expand=True, fill=tk.BOTH)
ttk.Style().configure("TNotebook", background='white')
ttk.Style().configure("TNotebook.Tab", foreground='black')


def getTaskTypeList():
    # get list of task types for combo box
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
    taskListCombo['values']= taskTypes
    # combo.current(0)

def dailyWATTreport():
    # get report of work done
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    sqlStatement = "SELECT * FROM WATT.worked"
    cursor.execute(sqlStatement)
    results = ''
    for row in cursor:
        results += 'row =%r' %(row,)
    reportLabel.config(text=results)
    conn.commit()
    conn.close()

def set_timer():
    # set start time of the timer
    global startTime
    startTime = time.time()
    update_timer()

def update_timer():
    # continually calculate the time since the start time of the timer
    updatedTime = time.time()
    duration = updatedTime - startTime # seconds
    duration = time.strftime('%H:%M:%S', time.gmtime(duration) )
    timerLabel.configure(text=duration)
    window.after(1000, update_timer)

def stop_timer():
    global startTime
    startTime = time.time()
    timerLabel.configure(text="")
    update_timer()
    
def taskTypeSelected(event):
    # show selected task
    taskTypeName = taskListCombo.get()
    status.configure(text = taskTypeName)

def startWorkItem():
    # error if no task type selected
    taskTypeName = taskListCombo.get()
    if taskTypeName == "":
        messagebox.showinfo('Error: Missing Selection','Choose a Task Type')
        return
    # check for working item in progress
    check = workingTaskTypeLabel.cget("text")
    if check != "":
        endWorkItem()
    # record selected task
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    clientCode = clientCodeTxt.get()
    workingNote = workedItemNote.get()
    startDateTime = time.strftime("%Y-%m-%d %H:%M:%S")
    sqlStatement = "SELECT taskTypeId FROM WATT.taskType WHERE taskTypeName = '" + taskTypeName + "'"
    print(sqlStatement)
    cursor.execute(sqlStatement)
    for row in cursor:
        taskTypeid = row.taskTypeId

    sqlStatement = "INSERT INTO watt.worked (taskTypeId,clientCode,workedItemNote, startedAtTime) VALUES (" + str(taskTypeid) + ",'" + clientCode + "','" + workingNote + "','" + startDateTime + "')"
    print(sqlStatement)
    cursor.execute(sqlStatement)

    sqlStatement  = 'SELECT MAX(workedItemId) AS lastEntry FROM watt.worked'
    print(sqlStatement)
    cursor.execute(sqlStatement)
    for row in cursor:
        global currentWorkingItemId
        currentWorkingItemId = row.lastEntry

    conn.commit()
    conn.close()
    status.configure(text= "Added Item!")
    set_timer()
    # set working item
    workingTaskTypeLabel.configure(text=taskTypeName)
    workingClientCodeLabel.configure(text=clientCode) 
    workingTaskNoteLabel.configure(text=workingNote)  
    endButton.grid(column=4, row=5,padx=(5, 5))
    taskListCombo.current()

    # reset options
    clientCodeTxt.delete(0, "end")
    clientCodeTxt.insert(0, "")
    workedItemNote.delete(0, "end")
    workedItemNote.insert(0, "")
    # taskNoteTxt.set("")
    # clientCodeTxt.set("")
    # clear text fields

def endWorkItem():
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()

    endDateTime = time.strftime("%Y-%m-%d %H:%M:%S")

    sqlStatement = "UPDATE watt.worked SET endedAtTime = '" + endDateTime + "' WHERE workedItemId = " + str(currentWorkingItemId)
    print(sqlStatement)
    cursor.execute(sqlStatement)
    conn.commit()
    conn.close()

    # un-set working item
    workingTaskTypeLabel.configure(text="")
    workingClientCodeLabel.configure(text="") 
    workingTaskNoteLabel.configure(text="")  
    timerLabel.configure(text="00:00:00")
    status.configure(text= "Ended Item!")

    # Hide End Button
    endButton.grid_forget()
    # Stop Timer
    stop_timer()

def beforeAppExit():
    check = workingTaskTypeLabel.cget("text")
    if check != "":
        endWorkItem()
    window.destroy()

# initialize variables #
username = os.getlogin()
continueTimer = False
# DESTKTOP STRING
# serverString =  'Driver={SQL Server};Server=TPECK\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
# serverString =  'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
# LAPTOP STRING
# serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\TAPE_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
# serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\' + username.upper() + '_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
serverString = 'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\' + username.upper() + '_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
print(serverString)

# Create Tab 1 Objects
spacing = tk.Label(tab1,text="")
status = tk.Label(tab1,text="Hello, " + username +"!", font=("Arial Bold", 10))
taskListLabel = tk.Label(tab1,text="Task Type")
taskListCombo = ttk.Combobox(tab1, width=15)
taskListCombo.bind("<<ComboboxSelected>>", taskTypeSelected)
clientCodeLabel = tk.Label(tab1,text="Client Code", font=("Arial", 8), width=10)
workedItemNoteLabel = tk.Label(tab1,text="Note", font=("Arial", 8))
clientCodeTxt = tk.Entry(tab1,width=20)
workedItemNote = tk.Entry(tab1,width=20)
startButton = tk.Button(tab1, text="Start", command=startWorkItem, width=15)
currentWorkingLabel = tk.Label(tab1,text="")
workingTaskTypeLabel = tk.Label(tab1,text="")
workingClientCodeLabel = tk.Label(tab1,text="")
workingTaskNoteLabel = tk.Label(tab1,text="")
timerLabel = tk.Label(tab1, text="")
endButton = tk.Button(tab1, text="End", command=endWorkItem, width=15)

# Organize Tab 1 Objects 
    # Row 0 (messages)
status.grid(column=0, row=1,pady=5)
    # Row 1 (Labels)
clientCodeLabel.grid(column=1,row=2)
workedItemNoteLabel.grid(column=2,row=2)
    # Row 2 (Entry)
taskListCombo.grid(column=0, row=3,padx=(5, 5))
clientCodeTxt.grid(column=1,row=3,padx=(5, 5))
workedItemNote.grid(column=2,row=3,padx=(5, 5))
startButton.grid(column=3, row=3,padx=(5, 5))

    # Row 3 (Spacing)
currentWorkingLabel.grid(column=1,row=4)
    # Row 4 (In Progress)
workingTaskTypeLabel.grid(column=0,row=5)
workingClientCodeLabel.grid(column=1,row=5)
workingTaskNoteLabel.grid(column=2,row=5)
timerLabel.grid(column=3,row=5)
endButton.grid(column=4, row=5,padx=(5, 5))
endButton.grid_forget()


# Tab 2 Objects
# txtBox = scrolledtext.ScrolledText(tab2,width=40,height=10)
# txtBox.grid(column=0,row=0)
reportLabel = tk.Label(tab2,text='',font=("Arial", 8))
reportLabel.grid(column=0,row=2)
 

# Start Up Functions
getTaskTypeList()
dailyWATTreport()

window.protocol("WM_DELETE_WINDOW", beforeAppExit)
# ongoing loop
window.mainloop()
