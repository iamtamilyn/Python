import time
import os

# import datetime
# os.getenv('COMPUTERNAME')

# taskTypes = {
#     1: 'Files',
#     2: 'Inquiries',
#     3: 'Emails',
#     4: 'Review',
#     5: 'Call',
#     6: 'Meeting'
# }

# test1 = datetime.datetime.fromtimestamp(1284286794)
# test2 = datetime.datetime(2010, 1, 1, 17, 0, 0)

# print(test1)
# print(test2)


def CallStoredProc(conn, procName, *args):
    sql = """
         DECLARE @ret int
         EXEC @ret = %s %s
         SELECT @ret""" % (procName, ','.join(['?'] * len(args)))
    return sql
results = CallStoredProc('conn', 'help_me','okay', 23)

def CallStoredProc2(conn, procName, *args):
    addOn = ''
    for arg in args:
        addOn += ',' + str(arg)

    print(addOn)
    sql = """
         DECLARE @ret int
         EXEC @ret = %s %s
         SELECT @ret""" % (procName, addOn)
    return sql
results2 = CallStoredProc2('conn', 'help_me','okay', 23)

print(results)
print(results2)