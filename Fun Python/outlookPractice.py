import win32com.client
import win32com
import os
import sys


outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

accounts= win32com.client.Dispatch("Outlook.Application").Session.Accounts

import win32com.client
import win32com
import os
import sys

f = open("testfile.txt","w+")

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
accounts= win32com.client.Dispatch("Outlook.Application").Session.Accounts;

def emailleri_al(folder):
    messages = folder.Items
    a=len(messages)
    if a>0:
        for message2 in messages:
             try:
                sender = message2.SenderEmailAddress
                if sender != "":
                    print(sender)
             except:
                print("Error")
                print(account.DeliveryStore.DisplayName)
                pass

             try:
                message2.Save
                message2.Close(0)
             except:
                 pass


for account in accounts:
    global inbox
    inbox = outlook.Folders(account.DeliveryStore.DisplayName)
    print("****Account Name**********************************")
    print(account.DisplayName)
    print("***************************************************")
    folders = inbox.Folders
    print(folders[6])


    emailleri_al(folders[6])

    # emailleri_al('Inbox')
print("Finished Succesfully")

