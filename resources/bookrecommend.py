"""
Student ID: F1322708
Date Modified: 16/12/2021
"""
try:
    import resources.database as database
except:
    pass

from tkinter import *
from tkinter import ttk
import time

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#how many books should be recommended
NUM_RECOMMENDATIONS = 5

#returns a list of genres and how many times the member has taken out a book from the genre
def get_genre_counts(member_ID):
    """
    Gets a list of dictionaries containing genres with the amount of times a book has been checked
    out from that genre.
    :param member_ID: member ID
    :return: list of dictionaries - keys (genre, count)
    """
    books_checked_out = get_books_checked_out(member_ID)
    
    genreCountDicts = []
    for book_ID in books_checked_out:
        genre = get_genre(book_ID)
        i=0
        newGenre = True #flag for adding a new genre
        for i in range(len(genreCountDicts)):
            if genreCountDicts[i]["Genre"] == genre:
                genreCountDicts[i]["Count"] += 1
                newGenre = False
        if newGenre:
            genreCountDicts.append({"Genre":genre,"Count":1})


    return genreCountDicts

#returns a list of authors and how many times the member has taken out a book by the author
def get_author_counts(member_ID):
    """
    Gets the amount of times the member has taken out books for each genre
    :param member_ID: member ID
    :return: list of dictionaries - keys (author, count)
    """
    books_checked_out = get_books_checked_out(member_ID)
    
    authorCountDicts = []
    for book_ID in books_checked_out:
        author = get_author(book_ID)
        i=0
        newAuthor = True #flag for adding a new genre
        for i in range(len(authorCountDicts)):
            if authorCountDicts[i]["Author"] == author:
                authorCountDicts[i]["Count"] += 1
                newAuthor = False
        if newAuthor:
            authorCountDicts.append({"Author":author,"Count":1})


    return authorCountDicts

#return a list of all the genres
def get_genres():
    """
    Gets a list of all genres from the database.
    :return: string list of genres
    """
    database_rows = database.get_database()
    genres = []
    for row in database_rows:
        if row["Genre"] not in genres:
            genres.append(row["Genre"])
    return genres

#get the total amount of times a book has been checked out
def get_total_book_checkouts_count(book_ID):
    """
    Gets the total amount of times a book has been checked out.
    :param book_ID: book ID
    :return: amount of times book has been checked out (int)
    """
    database_rows = database.get_database()
    for row in database_rows:
        if row["ID"] == book_ID:
            book_title =row["Title"]
            break
    logfile_rows = database.get_logfile()
    count = 0
    book_IDs = database.GetBookIDsFromTitle(book_title)
    for row in logfile_rows:
        if  row["ID"] in book_IDs:
            count += 1
    return count

#returns data needed to create a bar chart showing the popularity of books in a given genre
def get_bar_chart_for_genre(genre):
    """
    Gets data required to create a bar chart showing book popularities in a genre
    :param genre: genre name (string)
    :return: tuple containing book names (x axis values) and their counts (y axis values)
    """
    book_names = []
    book_counts = []

    database_rows = database.get_database()
    #iterate through database to find all books from the given genre and their checkout count
    for row in database_rows:
        if row["Genre"] == genre:
            book_names.append(row["Title"])
            book_counts.append(get_total_book_checkouts_count(row["ID"]))         

    #sort x and y values by count
    zippedLists = zip(book_counts , book_names)
    sortedZippedLists = sorted(zippedLists, reverse = True)
    book_names = [element for _, element in sortedZippedLists]
    book_counts = sorted(book_counts, reverse= True)
    return (book_names, book_counts)

#return the genre of the given book
def get_genre(book_ID):
    """
    Gets genre of a book.
    :param book_ID: book ID
    :return: genre name (String)
    """
    database_rows = database.get_database()
    for row in database_rows:
        if row["ID"] == book_ID:
            return row["Genre"]

def get_author(book_ID):
    """
    Gets author of a book.
    :param book_ID: book ID
    :return: name of author (string)
    """
    database_rows = database.get_database()
    for row in database_rows:
        if row["ID"] == book_ID:
            return row["Author"]

#returns list of book IDs that given member has previously checked out
def get_books_checked_out(member_ID):
    """
    Gets books checked out by the member.
    :param member_ID: member ID
    :return: list of book IDs that have been checked out by member
    """
    logfile_rows = database.get_logfile()
    books_checked_out = []
    #iterate through logfile adding book ID to list if member ID is given member ID
    for row in logfile_rows:
        if row["Member ID"] == member_ID:
            books_checked_out.append(row["ID"])
    return books_checked_out

#main function
def recommend_books(pie_chart_frame,bar_chart_frame,rank_tree,recommend_message_label,\
    member_ID,rank_weightings, selected_genre = "None",genre_combobox = ttk.Combobox,\
        results_from_book_ranking = ttk.Label): 
    """
    Main function for recommending books that makes the pie chart and bar chart and calls function
    to rank all books.
    :param pie_chart_frame: pie chart frame
    :param bar_chart_frame: bar chart frame
    :param rank_tree: tree for ranking table
    :param recommend_message_label: label for showing results of functions to user on GUI
    :param member_ID: member ID
    :param rank_weightings: weighting for calculating total score
    :param selected_genre: genre to make bar chart
    :param genre_combobox: combobox for selecting genre to make bar chart
    :param results_from_book_ranking: label for showing the books to recommend
    :return: none
    
    """
    
    
    
    #input validation - give error message if member ID is not valid
    if database.validate_memberID(member_ID):
        recommend_message_label.configure(text = "Book recommendations for: "+member_ID)
    else:
        recommend_message_label.configure(text = "Enter a valid member ID")
        return

    #make book ranking list
    booksToRecommend = get_book_recommend_list(rank_tree,member_ID,rank_weightings)
    #display the top ranked books to recommend
    #database.clearFrame(results_from_book_ranking)
    book_titles = ""
    for title in booksToRecommend:
        book_titles += "\n       "+title

    database.clearFrame(results_from_book_ranking)
    results_from_book_ranking.configure(text = "Recommend these books to %s: %s" % (member_ID,book_titles))
        

    #clear the graphs
    database.clearFrame(pie_chart_frame)
    database.clearFrame(bar_chart_frame)

    
    genres_and_count = get_genre_counts(member_ID)                 
        
    #find favourite genre(s)
    max_count = 0
    favourite_genres = []
    for row in genres_and_count:
        if row["Count"] > max_count:
            max_count = row["Count"]
            favourite_genres = [row["Genre"]]
        elif row ["Count"] == max_count:
            favourite_genres.append(row["Genre"])
    
    #sort genres and count by count
    genres_and_count = sorted(genres_and_count, key=lambda x: x["Count"], reverse = True)


    #pie chart of genres
    labels = []
           
    for row in genres_and_count:
        labels.append(row["Genre"])
           
    sizes = []
    for row in genres_and_count:
        sizes.append(row["Count"])
    #pie chart
    
    fig1, ax1 = plt.subplots(figsize=(4,2))
    ax1.pie(sizes, autopct="%1.1f%%")
    
    if len(labels) == 0:
        title = "Member has not checked out any books\nRecommendations will not be personalised"
        title_offset = 0.5
    else:
        title_offset = 0.3
        if len(favourite_genres) == 1:
            title = "Preferred Genre: "+favourite_genres[0]
        else:
            title = "Preferred Genres: "
            for i in range(len(favourite_genres)):  
                if i == 0:
                    title += favourite_genres[i]
                else:        
                    title += " ," +favourite_genres[i]
        
        ax1.legend(loc = "center right", fontsize = 8, labels=labels, bbox_to_anchor=(0,0.5))

    title_fontsize = 12
    for _ in favourite_genres:
        title_fontsize -= 1
    plt.title(title,x = title_offset,y=1,fontsize=title_fontsize)
    ax1.axis('equal')
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig1, master=pie_chart_frame) 
    canvas.draw()
    canvas.get_tk_widget().pack()

    #bar chart
    if selected_genre == "None":
        if len(labels) > 0:
            selected_genre = labels[0]
        else:
            selected_genre = get_genres()[0]
        i = genre_combobox['values'].index(selected_genre)
        genre_combobox.current(i)
        
    fig2, ax2 = plt.subplots(figsize=(4,2))
    bar_chart_data = get_bar_chart_for_genre(selected_genre)
    x = bar_chart_data[0]
    y = bar_chart_data[1]


    ax2.barh(x,y)
    plt.gca().invert_yaxis()
    #ax2.axis('equal')
    ax2.set_xlabel("Total Checkouts")
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig2, master=bar_chart_frame) 
    canvas.draw()
    canvas.get_tk_widget().pack()

def get_book_recommend_list(rank_tree,member_ID,rank_weightings):
    """
    Gets a table containing all the books ranked by their scores calculated by different atrtributes and weightings
    and returns a list of books to recommend

    :param rank_tree: tree for table
    :param member_ID: member ID
    :param rank_weightings: weightings used to calculate total score from the different attribute scores
    :return: list of books to recommend
    """


    #clear tree
    rank_tree.delete(*rank_tree.get_children())

    #add all books to ranking list
    database_rows = database.get_database()
    uniqueBooks = database.get_unique_books()
        

    get_highest_loan_count = database.get_highest_loan_count()


    #calculate the highest checkout count of the preferred genre
    genres_and_count = get_genre_counts(member_ID)
    highestGenreCount = 0
    for row in genres_and_count:
        rowCount = int(row["Count"])
        if rowCount > highestGenreCount:
            highestGenreCount = rowCount

    #calculate the highest checkout count of the author genre
    authorsAndCount = get_author_counts(member_ID)
    highestAuthorCount = 0
    for row in authorsAndCount:
        rowCount = int(row["Count"])
        if rowCount > highestAuthorCount:
            highestAuthorCount = rowCount


    #calculate most loans by member score
    most_loans_by_member = 0
    _bookIDs = get_books_checked_out(member_ID)
    for _bookID in _bookIDs:
        _count = database.BookLoanCountMember(database.get_book_title(_bookID),member_ID)
        if _count > most_loans_by_member:
            most_loans_by_member = _count
    


    treeRows = []
    for row in uniqueBooks:

        _title = row["Title"]
        
        #calculate overall popularity score
        _popularityScore = (get_total_book_checkouts_count(row["ID"]) / get_highest_loan_count) * 100

        
        #calculate genre score
        if highestGenreCount == 0: #if member has not taken out any books then genre count will defaultto 100 for all books
            _genreScore = 100
        else:

            genreCount = 0
            bookGenre = row["Genre"]
            i=0
            for i in range(len(genres_and_count)):
                if genres_and_count[i]["Genre"] == bookGenre:
                    genreCount = int(genres_and_count[i]["Count"])
            _genreScore = (genreCount / highestGenreCount) * 100


        #calculate author score
        if highestAuthorCount == 0: #if member has not taken out any books then author count will default to 100 for all books
            _authorScore = 100
        else:

            authorCount = 0
            bookAuthor = row["Author"]
            i=0
        
            for i in range(len(authorsAndCount)):
                if authorsAndCount[i]["Author"] == bookAuthor:
                    authorCount = int(authorsAndCount[i]["Count"])
            _authorScore = (authorCount / highestAuthorCount) * 100

        #calculate not read score
        memberBookLoanCount = database.BookLoanCountMember(row["Title"],member_ID)
        if memberBookLoanCount == 0:
            _notReadScore = 100
        else:
            _notReadScore = 100 - (database.BookLoanCountMember(row["Title"],member_ID) / most_loans_by_member) * 100


        #calculate purchase date score
        purchaseDateBounds = database.get_purchase_date_bounds()
        purchaseDate = time.strptime(row["Purchase Date"], "%d/%m/%Y")
        _purchaseDateScore = ((time.mktime(purchaseDate)-time.mktime(purchaseDateBounds[0]))/(time.mktime\
            (purchaseDateBounds[1])-time.mktime(purchaseDateBounds[0]))) * 100

        popularityWeightInpValue = abs(rank_weightings[0])  
        genreWeightInpValue = abs(rank_weightings[1])
        purchaseDateWeightInpValue = abs(rank_weightings[2])
        authorWeightInpValue = abs(rank_weightings[3])
        notReadWeightInpValue = abs(rank_weightings[4])

        weightTotal = popularityWeightInpValue + purchaseDateWeightInpValue + genreWeightInpValue + \
            authorWeightInpValue + notReadWeightInpValue
        if weightTotal == 0: #prevent divide by zero error if user has input all 0s for weightings
            popularityWeightInpValue = 1
            purchaseDateWeightInpValue = 1
            genreWeightInpValue = 1
            authorWeightInpValue = 1
            notReadWeightInpValue = 1
            weightTotal = popularityWeightInpValue + purchaseDateWeightInpValue + genreWeightInpValue\
                 + authorWeightInpValue + notReadWeightInpValue
        

        
        authorWeight = authorWeightInpValue / weightTotal
        popularityWeight = popularityWeightInpValue / weightTotal
        purchaseDateWeight = purchaseDateWeightInpValue/ weightTotal
        genreWeight = genreWeightInpValue/ weightTotal
        notReadWeight = notReadWeightInpValue / weightTotal

        #calculate total score
        _totalScore = _popularityScore*popularityWeight + _purchaseDateScore*purchaseDateWeight +\
             _genreScore*genreWeight + _authorScore*authorWeight + _notReadScore*notReadWeight
        
        treeRows.append({"Title": _title,"Total Score":_totalScore,"Popularity":_popularityScore,\
            "Genre":_genreScore,"Purchase Date":_purchaseDateScore,"Author":_authorScore,"Not Read":_notReadScore})
        
    #sort the tree rows by their total score descending
    treeRows = sorted(treeRows, key=lambda x: x["Total Score"],reverse = True)

    for i,row in enumerate(treeRows):
        _tags = ()
        if i < NUM_RECOMMENDATIONS:
            _tags = ("recommend")

        #format scores into 2 decimal places
        _totalScore = "%.2f" % row["Total Score"]
        _popularity = "%.2f" % row["Popularity"]
        _genre = "%.2f" % row["Genre"]
        _purchaseDate = "%.2f" % row["Purchase Date"]
        _author = "%.2f" % row["Author"]
        _notRead = "%.2f" % row["Not Read"]
        
        rank_tree.insert('', END, values=[row["Title"],_totalScore,_popularity,_genre,_purchaseDate\
            ,_author,_notRead], tags = _tags)
    #highlight the books to recommend
    rank_tree.tag_configure("recommend", background = "deep sky blue")

    book_titles = [row["Title"] for row in treeRows]
    return book_titles[:NUM_RECOMMENDATIONS]


#Testing
if __name__ == "__main__":
    import database
    print(get_genre("0"))
    print(get_genre_counts("tomw"))
    print(get_total_book_checkouts_count("0"))
    print(get_books_checked_out("tomw"))
    print(get_genres())