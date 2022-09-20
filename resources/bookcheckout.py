"""
Student ID: F1322708
Date Modified: 16/12/2021
"""

try:
    import resources.database as database
except:
    pass

#config
maxLoanTime = 60

def check_out_book_in_files(book_ID,member_ID):
    """
    Calls functions to update data in the database and logfile
    :param book_ID: book id (string)
    :param member_ID: member id (string)
    :return: None
    """
    #add a log to the logfile
    database.CheckoutLog(book_ID,member_ID)
    #update the database
    database.CheckoutDatabase(book_ID,member_ID)

def get_members_books_on_loan(member_ID):
    """
    Gets a list of books on loan by the member.
    :param member_ID: member ID (string)
    :return: list of records of books 
    """

    database_rows = database.get_database()
    booksOnLoan = []
    #iterate through each row in database to find rows with given member_ID
    for row in database_rows:
        if row["Member ID"] == member_ID:
            booksOnLoan.append(row["ID"]) #if book is on loan to member then add its id to the booksOnLoan list
    return booksOnLoan #return list of IDs of books on loan to given member


def get_overdue_books(member_ID):
    """
    Gets a list of the members overdue books.
    :param member_ID: member ID (string)
    :return: list of records of books 
    """


    #get list of books the member has on loan
    booksOnLoan = get_members_books_on_loan(member_ID)
    overdueBooks = []
    #iterate through members loaned books and add any overdue books to a list
    for book_ID in booksOnLoan:
        if database.BookOverdue(book_ID): 
            overdueBooks.append(book_ID)
    return overdueBooks #return list of overdue books

def check_out_book(checkout_message_label,book_IDs,member_ID):
    """
    Performs validation and GUI messages for checking out books then calls function to update the files.
    :param checkout_message_label: GUI label to show user results of the function
    :param book_IDs: entry text for inputing list of book IDs to check out
    :param member_ID: member id
    :return: None
    """

    book_IDs = book_IDs.split(',')
    feedbackMessage = ""

    #input validation for member ID
    if member_ID == "" or len(member_ID) != 4 or any(char.isdigit() for char in member_ID):
        feedbackMessage += "\"%s\" is not a valid member ID\n"  % member_ID
        checkout_message_label.config(text = feedbackMessage)
        return

    #input validation for book IDs
    if book_IDs == ['']:
        feedbackMessage += "Enter valid book ID(s)"  
        checkout_message_label.config(text = feedbackMessage)
        return

    for book_ID in book_IDs:
        #required data
        bookExists = database.BookExists(book_ID)
        bookCheckedOut = database.BookOnLoan(book_ID)
        overdueBooks = get_overdue_books(member_ID)
        if len(overdueBooks) == 0:
            memberOverdue = False
        else:
            memberOverdue = True
        book_title = database.get_book_title(book_ID)

        
        #validation
        if not bookExists:
            feedbackMessage += "ID = %s: Book does not exist with this ID:\n" % book_ID
        elif bookCheckedOut:
           feedbackMessage += "ID = %s: This book is already checked out\n" % book_ID
        elif memberOverdue:
            feedbackMessage += "%s has one or more overdue book loans: Book ID(s) = "  % member_ID
            feedbackMessage += overdueBooks[0] +" : " + database.get_book_title(overdueBooks[0])
            overdueBooks.pop(0)
            for book_ID in overdueBooks:
                feedbackMessage += "," + book_ID +" : " + database.get_book_title(book_ID) 
            feedbackMessage += "\n"
            break
        else:
            #checkout message
            feedbackMessage += "ID = %s:%s has been checked out to %s\n" % (book_ID,book_title,member_ID)

            #update the logfile and database
            check_out_book_in_files(book_ID,member_ID)

    checkout_message_label.configure(text = feedbackMessage)

#Testing
if __name__ == "__main__":  
    print(get_overdue_books("tomw"))
    print(get_members_books_on_loan("tomw"))

    
