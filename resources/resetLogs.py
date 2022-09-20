import csv
from csv import DictWriter
import database as database

def reset():
    #clear the logfile
    with open('logfile.txt', 'w', newline='') as logfile:             
        logfile.write("ID,Checkout Date,Return Date,Member ID\n")
        print("Logfile has been cleared")

    #set all books in database to available
    database_rows = database.get_database()
    book_IDs = []
    for row in database_rows:
        book_IDs.append(row["ID"])

    for book_ID in book_IDs:
        database.ReturnDatabase(book_ID)
    print("database has been cleared")


if __name__ == "__main__":
    reset()

