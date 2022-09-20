"""
Student ID: F1322708
Date Modified: 16/12/2021
"""
import csv
from csv import DictWriter

from datetime import date
import time


databaseName = 'data/database.txt'
databaseFieldNames = ["ID","Genre","Title","Author","Purchase Date","Member ID"] 
logfileName = 'data/logfile.txt'
logfileFieldNames = ["ID","Checkout Date","Return Date","Member ID"]  
searchableFields = ["Title","Author","Genre","Member ID"]
sortableFields = ["ID","Genre","Title","Author","Purchase Date","Member ID"]


maxLoanTime = 60 #books loaned for more than 60 days will be identified as overdue

#gets title of a book given the books ID
def get_book_title(id):
    """
    Gets book title from books ID.
    :param id: book ID (string)
    :return: title of book (string)
    """
    database_rows = get_database()
    #iterate through each row in database to find row with given ID
    for row in database_rows:
        if row["ID"] == id:
            return row["Title"] #if row with a matching book ID has been found then return the title

#get database as a list of dictionaries
def get_database():
    """
    Gets the database as list of dictionaries.
    :return: list of dictionaries of database rows
    """
    database_rows = get_list_of_dicts(databaseName)
    return database_rows

#get logfile as a list of dictionaries
def get_logfile():
    """
    Gets the logfile as list of dictionaries.
    :return: list of logfile of database rows
    """
    logfile_rows = get_list_of_dicts(logfileName)
    return logfile_rows
    
#returns file with given name as list of dictionaries
def get_list_of_dicts(fileName):   
    with open(fileName,mode ='r') as fileCsv:
        
        fileDict = csv.DictReader(fileCsv)
        fileRows = list(fileDict)
        return fileRows

#returns the time in days a book has been on loan
def get_loan_time(book_ID):
    """
    Gets the time in days book has been on loan.
    :param book_ID: book ID
    :return: days book has been on loan (int)
    """
    logfile_rows = get_logfile()
    #iterate through logfile to find most recent checkout log of the given book
    for row in logfile_rows:
        if row["ID"] == book_ID and row["Return Date"] == "0": #return date == "0" indicates the book is checked out
            checkoutDateList = row["Checkout Date"].split('/')
            checkoutDate = date(int(checkoutDateList[2]),int(checkoutDateList[1]),int(checkoutDateList[0]))
            return (date.today() - checkoutDate).days

#member ID validation
def validate_memberID(member_ID):
    """
    Validates the member ID
    :param member_ID: member ID inputted
    :return: Boolean expressing whether the inputted member ID is valid
    """
    #return false if member_ID is blank, not 4 characters long, or contains any numbers
    if member_ID == "" or len(member_ID) != 4 or ' ' in member_ID or any(x.isdigit() for x in member_ID):
        return False
    else:
        return True

#get number of times any book has been taken out
def get_total_book_loans():
    """
    Gets the total number of times any book has been taken out.
    :return: total book loan (int)
    """
    logfile_rows = get_logfile()
    return len(logfile_rows)

#get the purchase dates of the oldest book in and newest book in database
def get_purchase_date_bounds():
    """
    Gets the purchase date of oldest and newest books.
    :return: tuple of date of oldest book and newest book
    """
    database_rows = get_database()
    database_rows = sorted(database_rows, key=lambda x: time.strptime(x["Purchase Date"], "%d/%m/%Y"))
    min = time.strptime(database_rows[0]["Purchase Date"], "%d/%m/%Y")
    max = time.strptime(database_rows[-1]["Purchase Date"], "%d/%m/%Y")
    return (min,max)

#get database but with duplicate books removed
def get_unique_books():
    """
    Gets database but with duplicate books removed
    :return: database rows
    """
    database_rows = get_database()
    uniqueBooks = []
    #remove duplicate books
    book_titles = []
    for row in database_rows:
        if not (row["Title"] in book_titles):
            uniqueBooks.append(row)
            book_titles.append(row["Title"])
        
    return uniqueBooks

#get amount of times most popular book has been loaned
def get_highest_loan_count():
    """
    Gets the checkout count of book that has been checked out the most
    :return: checkout count (int)
    """
    logfile_rows = get_logfile()
    uniqueBooks = get_unique_books()

    highestCount = 0
    for row in uniqueBooks:
        id = row["ID"]
        i = 0
        count = 0
        for i in range(len(logfile_rows)):
            if logfile_rows[i]["ID"] == id:
                count += 1
        if count > highestCount:
            highestCount = count

    return highestCount

#add to logfile
def CheckoutLog(book_ID, member_ID):
    """
    Adds the checkout log to logfile
    :param book_ID: book ID 
    :param member_ID: member ID
    :return: None
    
    """
    #add to logfile      
    with open(logfileName, 'a', newline='') as logfileCsv:                     
        logfileDict = DictWriter(logfileCsv, fieldnames=logfileFieldNames)
        checkoutDate = date.today().strftime('%d/%m/%Y')
        logfileDict.writerow({"ID":book_ID,"Checkout Date":checkoutDate,"Return Date":"0","Member ID":member_ID})

#add return date to the existing log
def ReturnLog(book_ID):
    """
    Updates the log of the book being taken out to add the return date
    :param book_ID: book ID
    :return: None
    """
    logfile_rows = get_logfile()
    #iterate through database and change the member ID of the row with given book ID to the new member
    for row in logfile_rows:
        if row["ID"] == book_ID and row["Return Date"] == "0":
            row["Return Date"] = date.today().strftime('%d/%m/%Y')         

    #apply changes to the file
    with open(logfileName, 'w', newline='') as logfileCsv:             
        logfileDict = DictWriter(logfileCsv, fieldnames=logfileFieldNames)
        #write field names to database
        logfileDict.writeheader()
        #write all rows to database
        for row in logfile_rows:
            logfileDict.writerow(row)

#update database - checking out books
def CheckoutDatabase(book_ID, member_ID):
    database_rows = get_database()
    #iterate through database and change the member ID of the row with given book ID to the new member
    for row in database_rows:
        if row["ID"] == book_ID:
            row["Member ID"] = member_ID

    #apply changes to the file
    with open(databaseName, 'w', newline='') as databaseCsv:             
        databaseDict = DictWriter(databaseCsv, fieldnames=databaseFieldNames)
        #write field names to database
        databaseDict.writeheader()
        #write all rows to database
        for row in database_rows:
            databaseDict.writerow(row)

#update database - returning books
def ReturnDatabase(book_ID):
    """
    Updates database to show book has been returned by changing the member ID field of the book
    :param book_ID: book ID:
    :return: None
    """
    database_rows = get_database()
    #iterate through database and change member ID of given book to 0 (0 indicating book is not checked out)
    for row in database_rows:
        if row["ID"] == book_ID:
            row["Member ID"] = "0"

    #apply changes to the file
    with open(databaseName, 'w', newline='') as databaseCsv:             
        databaseDict = DictWriter(databaseCsv, fieldnames=databaseFieldNames)
        #write field names to database
        databaseDict.writeheader()
        #write all rows to database
        for row in database_rows:
            databaseDict.writerow(row)

#clears all widgets from a frame
def clearFrame(frame):
    for child in frame.winfo_children():
        child.destroy()
                
def BookOnLoan(id):
    """
    Gets boolean value indicating if a book is on loan.
    :param id: book ID
    :return: true if book is on loan
    """
    database_rows = get_database()
    #iterate through each row in database to see if a book with given ID is on loan
    for row in database_rows:
        if row["ID"] == id:
            if row ["Member ID"] == "0": #member ID == "0" indicated book is not on loan
                return False
            else:
                return True
   
#checks if a book exists in the database
def BookExists(id):
    """
    Checks if a book is in databse
    :param id: book ID
    :retuturn: True if book is found in database
    """
    database_rows = get_database()
    #iterate through each row in database to see if a book with given ID exists
    for row in database_rows:
        if row["ID"] == id:
            return True #if row with a matching book ID has been found then return true
    return False #once every line has been checked and no matches have been found return false

#check if book is overdue
def BookOverdue(book_ID):
    """
    Check if a book is overdue.
    :param book_ID: book ID
    :return: True is a book is overdure (on loan more than 60 days)
    """
    if get_loan_time(book_ID) > maxLoanTime: #max loan time = 60 days
        return True
    else:
        return False  

#get number of times a book has been checked out by a member
def BookLoanCountMember(book_title,member_ID):
    """
    Gets number of times abook has been checkedd out by given member.
    :param book_title: book title
    :param member_ID: member ID
    :return: book loan count (int)
    
    """
    book_IDs = GetBookIDsFromTitle(book_title)
    logfile_rows = get_logfile()
    count = 0
    for book_ID in book_IDs:
        for i in range(len(logfile_rows)):
            row = logfile_rows[i]
            if row["ID"] == book_ID and row["Member ID"] == member_ID:
                count += 1
    return count

def GetBookIDsFromTitle(book_title):
    """
    Gets a list of book IDs of books with a given title
    :param book_title: book title
    :return: list of book IDs
    """
    database_rows = get_database()
    book_IDs = []
    for row in database_rows:
        if row["Title"] == book_title:
            book_IDs.append(row["ID"])
    return book_IDs

if __name__ == "__main__":
    print("===TESTING FOR DATABASE.PY===")
    print("Printing every row of the database...")
    database_rows = get_database()
    for row in database_rows:
        print(row)

    print("Testing get_loan_time")
    testID = "1"
    print("Book: ID=",testID," has been on loan for",get_loan_time(testID),"days")

 
    print("Tetsing get_unique_books")
    print(get_unique_books())

    print(BookLoanCountMember("Dracula","tomw"))

