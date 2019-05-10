import time
import os
import math
import pyodbc
# import datetime
# os.getenv('COMPUTERNAME')


def queryDatabase(sqlStatement):
    serverString =  'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
    print('executing',sqlStatement)
    global conn
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    cursor.execute(sqlStatement)
    results = []
    try: 
        for row in cursor:
            print('funcQlen',len(row))
            results.append(row)
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
    taskTypes = queryDatabase("SELECT taskTypeId, taskTypeName FROM watt.taskType")
    print(taskTypes)
    taskTypesDict = dict(taskTypes)
    print(taskTypesDict)
    # taskListCombo['values']= taskTypes
    # taskListCombo.current(0)

def main():
    getTaskTypeList()
    

if __name__ == "__main__":
    main()