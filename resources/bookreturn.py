"""
Student ID: F1322708
Date Modified: 16/12/2021
"""
try:
    import resources.database as database
except:
    pass

#return the ID of the member who is loaning given book
def get_member_loaning_book(book_ID):
    """
    Gets the member ID of whoever is loaning given book.
    :param book_ID: book ID
    :return: member ID 
    """
    database_rows = database.get_database()
    #iterate through database and find row with the given book ID
    for row in database_rows:
        if row["ID"] == book_ID:
            return row["Member ID"] #return the member id 

def return_book(returnMessageLabel, book_IDs):
    """
    Returns a book and displays messages to the user on the GUI

    :param returnMessageLabel: label for showing text of results of function
    :param book_IDs: text of entry - list of book IDs seperated by commas
    :return: None
    """
    book_IDs = book_IDs.split(',')
    feedbackMessage = ""

    #input validation for book IDs
    if book_IDs == ['']:
        feedbackMessage += "Enter valid book ID(s)"  
        returnMessageLabel.config(text = feedbackMessage)
        return


    for book_ID in book_IDs:
        bookExists = database.BookExists(book_ID)
        bookCheckedOut = database.BookOnLoan(book_ID)   
        member_ID = get_member_loaning_book(book_ID)  #get the ID of the member who has boon on loan
            

        #if book does not exist return error message and end function
        if not bookExists:
            feedbackMessage += "ID = %s: Book does not exist with this ID:\n" % book_ID
        elif bookCheckedOut:           
            #return the book
            #update log file
            database.ReturnLog(book_ID)
            #update database
            database.ReturnDatabase(book_ID)


            #display returned book message
            feedbackMessage += "ID = %s: Book Returned from Member: %s\n" % (book_ID,member_ID)           
        else:
            #display error message
            feedbackMessage += "ID = %s: This book is not checked out\n" % book_ID
        returnMessageLabel.configure(text = feedbackMessage)
       

if __name__ == "__main__":
    import database
    testID = "29"
    print("Book:",testID,"is on loan to member:",get_member_loaning_book(testID))
  