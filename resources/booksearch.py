"""
Student ID: F1322708
Date Modified: 16/12/2021
"""
import time

from tkinter import *
from tkinter import ttk

try:
    import resources.database as database
except:
    pass

def search_books(search_results_box,searchTerm,searchField,sortField):
    """
    Gets search results to show to user and adds them to the search table on GUI.

    :param search_results_box: Frame containing GUI elements to manipulate
    :param searchTerm: search term entered into search bar by user
    :param searchField: field being used to search
    :param sortField:field being used to sort
    :return: None
    
    """

    
    #clear the previous results
    database.clearFrame(search_results_box)

    #get the search results
    searchResults = get_search_results(searchTerm,searchField)

    #sort the data by given field
    if sortField == "Purchase Date":      
       #searchResults = sorted([time.strptime(dt[sortField], "%d/%m%Y") for dt in searchResults])
       searchResults = sorted(searchResults, key=lambda x: time.strptime(x[sortField], "%d/%m/%Y")) 
    elif sortField == "ID":
        searchResults = sorted(searchResults, key=lambda x: int(x[sortField])) 
    else:
        searchResults = sorted(searchResults, key=lambda x: x[sortField]) 

    # define columns
    columns = ("ID", "Title", "Author", "Genre","Purchase Date","Loaned to Member")

    tree = ttk.Treeview(search_results_box, columns=columns, show='headings')

    tree.column("ID",width= 30)
    tree.configure(height= 20)
    tree.column("Purchase Date",width= 100)


    # define headings
    for columnName in columns:
        tree.heading(columnName, text = columnName)


    # generate sample data
    searchResultsRows = []
    for row in searchResults:

        _id = row["ID"]
        _title = row["Title"]
        _author = row["Author"]
        _genre = row["Genre"]
        _purchaseDate = row["Purchase Date"]

        if row["Member ID"] == "0":
             _loanedToMember = "Available"
        else:
            _loanedToMember = row["Member ID"]

        

        
        searchResultsRows.append((_id,_title,_author,_genre,_purchaseDate,_loanedToMember))

    



    # add data to the treeview
    for row in searchResultsRows:
        book_ID = row[0]
        _tags = ("")
        if database.BookOnLoan(book_ID) and database.BookOverdue(book_ID): # if book is on loan and overdue
            _tags=("overdue")
            
        tree.insert('', END, values=row, tags=_tags)
       
    #highlight all overdue books in red 
    tree.tag_configure("overdue", background = "red")

    tree.grid(row=0, column=0, sticky='nsew')

    #add a scrollbar
    scrollbar = ttk.Scrollbar(search_results_box, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

def get_search_results(searchText,key):
    """
    Gets list of book records to show to user
    :param search_results_box: label for giving message to user on GUI
    :param searchTerm: the search string enterd by user into the search bar
    :param searchField: field being used for searching
    :param sortField: field being used to sort search results
    :return: list of search results to display to user
    """
    searchResults = []
    database_rows = database.get_database()

    searchText = searchText.casefold() #make search ignore case of characters

    
    
    
    #for each database, if search term is found in value of search field then add row to search results
    for row in database_rows:
        if searchText in row[key].casefold():
            searchResults.append(row)

    #return list of search results          
    return searchResults

#Testing
if __name__ == "__main__":
    import database
    print("===TESTING FOR BOOKSEARCH.PY===")
    testSearchTerm = "game"
    print("Searching for book by title using search term \'%s\'"%testSearchTerm)
    searchResults = get_search_results(testSearchTerm,"Title")
    for row in searchResults:
        print(row)
    
