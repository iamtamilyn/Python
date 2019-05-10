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
window.iconbitmap('watticon.ico')
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
ttk.Style().configure("TNotebook", background='yellow')
ttk.Style().configure("TNotebook.Tab", foreground='black')


def queryDatabase(sqlStatement):
    print('executing',sqlStatement)
    global conn
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    cursor.execute(sqlStatement)
    results = []
    try: 
        for row in cursor:
            print('funcQlen',len(row))
            for x in range(0,len(row)):
                # print('funcQ',row[x])
                results.append(row[x])
        print('funcQr',row)
    except:
        results = None
    print('funcQ.',results)
    conn.commit()
    conn.close()
    return results

def getTaskTypeList():
    # get list of task types for combo box
    global taskTypes
    taskTypes = queryDatabase("SELECT taskTypeName FROM watt.taskType")
    taskListCombo['values']= taskTypes
    taskListCombo.current(0)

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
    global currentWorkingItemId
    taskTypeName = taskListCombo.get()
    if taskTypeName == "":
        messagebox.showinfo('Error: Missing Selection','Choose a Task Type')
        return
    # check for working item in progress
    check = workingTaskTypeLabel.cget("text")
    if check != "":
        endWorkItem()
    # record selected task
    clientCode = clientCodeTxt.get()
    workingNote = workedItemNote.get()
    startDateTime = time.strftime("%Y-%m-%d %H:%M:%S")
    results = []
    # sqlStatement = "SELECT taskTypeId FROM WATT.taskType WHERE taskTypeName = '" + taskTypeName + "'"
    results = queryDatabase("SELECT taskTypeId FROM WATT.taskType WHERE taskTypeName = '" + taskTypeName + "'")
    taskTypeid = results[0]

    sqlStatement = "INSERT INTO watt.worked (taskTypeId,clientCode,workedItemNote, startedAtTime) VALUES (" + str(taskTypeid) + ",'" + clientCode + "','" + workingNote + "','" + startDateTime + "')"
    queryDatabase(sqlStatement)

    sqlStatement = 'SELECT workedItemId,taskTypeHexColor AS lastEntry FROM watt.worked INNER JOIN watt.tasktype ON worked.taskTypeId = taskType.taskTypeId WHERE workedItemId = (SELECT MAX(workedItemId) AS lastEntry FROM watt.worked)'
    results = queryDatabase(sqlStatement)
    try: 
        print('test2a',results[0])
        currentWorkingItemId = results[0]
        print('test3a',results[1])
        setColor = '#' + results[1]
    except:
        print('old query do not work')

    status.configure(text= "Added Item!")
    set_timer()
    # set working item
    workingTaskTypeLabel.configure(text=taskTypeName)
    workingClientCodeLabel.configure(text=clientCode) 
    workingTaskNoteLabel.configure(text=workingNote)  
    endButton.grid(column=4, row=5,padx=(5, 5))
    taskListCombo.current()

    # clear text fields
    clientCodeTxt.delete(0, "end")
    clientCodeTxt.insert(0, "")
    workedItemNote.delete(0, "end")
    workedItemNote.insert(0, "")
    
    ttk.Style().configure("TNotebook", background=setColor)

def endWorkItem():
    endDateTime = time.strftime("%Y-%m-%d %H:%M:%S")
    sqlStatement = "UPDATE watt.worked SET endedAtTime = '" + endDateTime + "' WHERE workedItemId = " + str(currentWorkingItemId)
    # print(sqlStatement)
    queryDatabase(sqlStatement)

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
    ttk.Style().configure("TNotebook", background='#63666A')

def beforeAppExit():
    check = workingTaskTypeLabel.cget("text")
    if check != "":
        endWorkItem()
    window.destroy()

# initialize variables #
continueTimer = False
username = os.getlogin()
if username == 'Quincy N':
    # DESTKTOP STRING
    # serverString =  'Driver={SQL Server};Server=TPECK\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
    serverString =  'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
elif username == 'thchan':
    # LOCAL_username
    serverString = 'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\' + 'LOCAL_' + username.upper() + ';Database=WATTapplication;Trusted_Connection=yes'
elif username == 'hesmit':
    # heather - just computer name
    serverString = 'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + ';Database=WATTapplication;Trusted_Connection=yes'
else:
    # LAPTOP STRING # username_LOCAL
    # serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\TAPE_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
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
def databaseConnection():
    try:
        getTaskTypeList()
    except:
        print('no DB here')
        messagebox.showinfo('Error: Missing Database','Closing, Try Again with DB.')
        exit(0)    
    # dailyWATTreport()
databaseConnection()

window.protocol("WM_DELETE_WINDOW", beforeAppExit)
# ongoing loop
window.mainloop()
