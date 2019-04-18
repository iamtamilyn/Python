import time
import os

import datetime
os.getenv('COMPUTERNAME')

taskTypes = {
    1: 'Files',
    2: 'Inquiries',
    3: 'Emails',
    4: 'Review',
    5: 'Call',
    6: 'Meeting'
}

test1 = datetime.datetime.fromtimestamp(1284286794)
test2 = datetime.datetime(2010, 1, 1, 17, 0, 0)

print(test1)
print(test2)
