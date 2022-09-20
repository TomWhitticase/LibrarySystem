import csv
from datetime import timedelta, date
from csv import DictWriter

import time
import random
import string

import database as database
import resetLogs as resetLogs



#reset the logs
resetLogs.reset()


members = []

minDate = '1/8/2018'
dayIncrements = 5
numMembers = 25
numLogs = 400
inOutRatio = 0.494 # 0 : all out  1: all in

def GenerateMemberID():
    newMember = ''.join(random.choice(string.ascii_lowercase) for i in range(4)) 
    if newMember in members:#if member id already exists generate a new one
        return GenerateMemberID()
    else:
        members.append(newMember)
        return newMember

database_rows = database.get_database()
book_IDs = []
for row in database_rows:
    book_IDs.append(row["ID"])

booksIn = book_IDs
booksOut = []

def CheckoutLogAtDate(book_ID, member_ID, checkoutDate):
    #add to logfile      
    with open('logfile.txt', 'a', newline='') as logfileCsv:                     
        logfileDict = DictWriter(logfileCsv, fieldnames=database.logfileFieldNames)       
        logfileDict.writerow({"ID":book_ID,"Checkout Date":checkoutDate,"Return Date":"0","Member ID":member_ID})





def CheckinLogAtDate(book_ID,myDate):
    logfile_rows = database.get_logfile()
    #iterate through database and change the member ID of the row with given book ID to the new member
    for row in logfile_rows:
        if row["ID"] == book_ID and row["Return Date"] == "0":
            row["Return Date"] = myDate         

    #apply changes to the file
    with open('logfile.txt', 'w', newline='') as logfileCsv:             
        logfileDict = DictWriter(logfileCsv, fieldnames=database.logfileFieldNames)
        #write field names to database
        logfileDict.writeheader()
        #write all rows to database
        for row in logfile_rows:
            logfileDict.writerow(row)

def GetAMemberID():
    if len(members) < numMembers:
        return GenerateMemberID()
    else:
        return random.choice(members)

def CheckOut(myDate):
    book_ID = random.choice(booksIn)
    member_ID = GetAMemberID()
    database.CheckoutDatabase(book_ID, member_ID)
    checkoutDate = myDate
    CheckoutLogAtDate(book_ID, member_ID,checkoutDate)
    booksOut.append(book_ID)
    booksIn.remove(book_ID)

def CheckIn(myDate):
    book_ID = random.choice(booksOut)
    database.ReturnDatabase(book_ID)
    
    CheckinLogAtDate(book_ID,myDate)
    booksIn.append(book_ID)
    booksOut.remove(book_ID)


def GenLogs():

    myDateList = minDate.split('/')
    myDate = date(int(myDateList[2]),int(myDateList[1]),int(myDateList[0]))
    
    logcount = 0
    while logcount < numLogs:
        if random.uniform(0,1) > inOutRatio: #random bool to choose if to check in a book or check out a book

            #check in
            if len(booksIn) > 0:
                CheckOut(myDate.strftime('%d/%m/%Y'))
                logcount += 1
        else:
            #check out
            if len(booksOut) > 0:
                CheckIn(myDate.strftime('%d/%m/%Y'))
                logcount += 1

        #increment day
        myDateList = myDate.strftime('%d/%m/%Y').split('/')
        myDate = date(int(myDateList[2]),int(myDateList[1]),int(myDateList[0])) + timedelta(days=dayIncrements)

        if myDate >= date.today():
            print("Reached todays date so stopped generating logs")
            break
    print("generated",logcount,"logs")
            
if __name__ == "__main__":
    GenLogs()
        