"""
Student ID: F1322708
Date Modified: 16/12/2021
"""

#tkinter (GUI)
from tkinter import *
from tkinter import ttk
#matplotlib (graphs,charts)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#othermodules
import resources.booksearch as booksearch
import resources.bookcheckout as bookcheckout
import resources.bookreturn as bookreturn
import resources.bookrecommend as bookrecommend

#default values for the weights for ranking books to recommend
defaultRankingWeights = (3,5,2,1,10)#popularity,genre,purchase date,author,not read
    
#GUI
root = Tk()
root.title("Library System")
style = ttk.Style(root)
style.theme_use('vista')
root.resizable(False, False)
#main notebook for different tabs 
menu_notebook = ttk.Notebook(root)
menu_notebook.configure(width = 1200, height = 600)

#menus
search_menu = ttk.Frame(menu_notebook)
checkout_menu = ttk.Frame(menu_notebook)
return_menu = ttk.Frame(menu_notebook)
recommend_menu = ttk.Frame(menu_notebook)

#search for book menu
search_bar_text = StringVar()
search_bar_text.trace("w", lambda name, index, mode,\
    search_bar_text=search_bar_text: update_search_results())
search_bar_elements_frame = Frame(search_menu)
search_bar = ttk.Entry(search_bar_elements_frame, width = 40,textvariable = search_bar_text)
search_bar.grid(row = 0, column = 0,padx= 10)
search_by_label = ttk.Label(search_bar_elements_frame, text = "Search by:")
search_by_label.grid(row = 0, column = 1,padx= 10)
selected_search_key = StringVar()
search_field_combobox = ttk.Combobox(search_bar_elements_frame, textvariable = selected_search_key)
search_field_combobox['values'] = booksearch.database.searchableFields
search_field_combobox.current(0)
search_field_combobox['state'] = 'readonly'
search_field_combobox.grid(row = 0, column = 2,padx= 10)
def update_search_results():
    booksearch.search_books(search_results_box,search_bar_text.get(),selected_search_key.get(),selected_sort_key.get())
def searchfield_combobox_callback(event):
    update_search_results()
search_field_combobox.bind('<<ComboboxSelected>>', searchfield_combobox_callback)
ttk.Label(search_bar_elements_frame, text = "Sort by:").grid(row = 0, column = 3,padx= 10)
selected_sort_key = StringVar()
sort_field_combobox = ttk.Combobox(search_bar_elements_frame, textvariable = selected_sort_key)
sort_field_combobox['values'] = booksearch.database.sortableFields
sort_field_combobox.current(0)
sort_field_combobox['state'] = 'readonly'
sort_field_combobox.grid(row = 0, column = 4,padx= 10)
def sortfield_combobox_callback(event):
    update_search_results()
sort_field_combobox.bind('<<ComboboxSelected>>', sortfield_combobox_callback)
search_bar_elements_frame.pack(pady = 10)
search_results_box = ttk.Frame(search_menu)
search_results_box.pack(pady = 10)

#checkout book menu
#checkout book ID entry
ttk.Label(checkout_menu, text = "Book ID").pack(pady=10)
checkout_book_ID_entry_text = StringVar()
ttk.Entry(checkout_menu, width = 40,text = "Book ID",textvariable = checkout_book_ID_entry_text).pack(pady=10)
#checkout book member ID entry
ttk.Label(checkout_menu, text = "Member ID").pack(pady=10)
checkout_member_ID_entry_text = StringVar()
ttk.Entry(checkout_menu, width = 40, textvariable = checkout_member_ID_entry_text).pack(pady=10)
#checkout book button
ttk.Button(checkout_menu, text = "Check Out", command = lambda:\
     bookcheckout.check_out_book(checkout_message_label,checkout_book_ID_entry_text.get(),\
         checkout_member_ID_entry_text.get())).pack(pady=10)
#checkout message label
checkout_message_label = ttk.Label(checkout_menu, text = "")
checkout_message_label.pack(pady=10)

#return book menu
#return book ID entry
ttk.Label(return_menu, text = "Book ID").pack(pady=10)
return_book_ID_entry_text = StringVar()
ttk.Entry(return_menu, width = 40,textvariable = return_book_ID_entry_text).pack(pady=10)
#return book message label
returnMessageLabel = ttk.Label(return_menu, text = "")
#return book button
ttk.Button(return_menu, text = "Return Book", command =
    lambda : bookreturn.return_book(returnMessageLabel,return_book_ID_entry_text.get())).pack(pady=10)
returnMessageLabel.pack()

#recommend book menu
#recommend books ID entry
#recommend books entry frame
recommendBooksEntryFrame = ttk.Frame(recommend_menu)
recommendBooksResultsFrame = ttk.Frame(recommend_menu,borderwidth=1,relief=RIDGE)
recommendBooksGraphsFrame = ttk.Frame(recommendBooksResultsFrame,borderwidth=1,relief=RIDGE)
ttk.Label(recommendBooksEntryFrame, text = "Member ID:").grid(row = 0,column = 0,padx = 10)
recommendBooksMemberIDEntryText = StringVar()
ttk.Entry(recommendBooksEntryFrame, width = 40,textvariable = recommendBooksMemberIDEntryText)\
    .grid(row = 0,column = 1,padx = 10)
recommend_message_label = ttk.Label(recommendBooksEntryFrame, text = "")
#blank genre pie chart
pie_chart_frame = ttk.Frame(recommendBooksGraphsFrame)
fig1 = plt.figure(figsize=(4,2))
canvas = FigureCanvasTkAgg(fig1, master=pie_chart_frame) 
canvas.draw()
canvas.get_tk_widget().pack()
#blank bar chart
bar_chart_frame = ttk.Frame(recommendBooksGraphsFrame)
fig2 = plt.figure(figsize=(4,2))
canvas = FigureCanvasTkAgg(fig2, master=bar_chart_frame) 
canvas.draw()
canvas.get_tk_widget().pack()
##combobox down for genres for the bar chart of total bookcheckouts
dropDownFrame = ttk.Frame(recommendBooksGraphsFrame)
selected_genre = StringVar()
genre_combobox = ttk.Combobox(dropDownFrame, textvariable = selected_genre)
genre_combobox['values'] = bookrecommend.get_genres()
genre_combobox.current(0)
genre_combobox['state'] = 'readonly'
#book ranking list frame
bookRankingFrame = ttk.Frame(recommendBooksResultsFrame)
results_from_book_ranking = ttk.Label(bookRankingFrame, text = "Recommend these books to member: "\
    +"\n" * bookrecommend.NUM_RECOMMENDATIONS, font= "TkDefaultFont 14")
#ranking books notebook
rankingNotebook = ttk.Notebook(bookRankingFrame)
bookRankingTreeFrame = ttk.Frame(rankingNotebook)
bookRankingWeightsFrame = ttk.Frame(rankingNotebook)

def filter_float_input(text):
    """
    Function for validating the input of an entry so only floats can be inputted.

    :param text: the text from an entry
    :return: text from an entry as a float or 0 if can't be converted
    """
    
    isFloat = True
    #normalise value
    if '-' in text:
        text.replace('-','')
    #convert to float
    try:
        float(text)
    except ValueError:
        isFloat = False
    if isFloat:
        return text
    else:
        return "0"

#callback for when a weighting entry is edited
def weight_entry_callback(var, index, mode):
    popularityWeightEntryText.set(filter_float_input(popularityWeightEntryText.get()))
    genreWeightEntryText.set(filter_float_input(genreWeightEntryText.get()))
    purchaseDateWeightEntryText.set(filter_float_input(purchaseDateWeightEntryText.get()))
    authorWeightEntryText.set(filter_float_input(authorWeightEntryText.get()))
    notReadWeightEntryText.set(filter_float_input(notReadWeightEntryText.get()))
#popularity score GUI elements
popularityWeightEntryText = StringVar()
popularityWeightEntryText.set(defaultRankingWeights[0])
ttk.Label(bookRankingWeightsFrame, width = 40,text = "Popularity Score Weighting:")\
    .grid(column = 0,row=0,padx=5, pady=5)
ttk.Entry(bookRankingWeightsFrame, width = 5,textvariable = popularityWeightEntryText)\
    .grid(column = 1,row=0,padx=5, pady=5)
popularityWeightEntryText.trace_add("write", weight_entry_callback)
#genre score GUI elements
genreWeightEntryText = StringVar()
genreWeightEntryText.set(defaultRankingWeights[1])
ttk.Label(bookRankingWeightsFrame, width = 40,text = "Genre Score Weighting:")\
    .grid(column = 0,row=1,padx=5, pady=5)
ttk.Entry(bookRankingWeightsFrame, width = 5,textvariable = genreWeightEntryText)\
    .grid(column = 1,row=1,padx=5, pady=5)
genreWeightEntryText.trace_add("write", weight_entry_callback)
#purchase date score GUI elements
purchaseDateWeightEntryText = StringVar()
purchaseDateWeightEntryText.set(defaultRankingWeights[2])
ttk.Label(bookRankingWeightsFrame, width = 40,text = "Purchase Date Score Weighting:")\
    .grid(column = 0,row=2,padx=5, pady=5)
ttk.Entry(bookRankingWeightsFrame, width = 5,textvariable = purchaseDateWeightEntryText)\
    .grid(column = 1,row=2,padx=5, pady=5)
purchaseDateWeightEntryText.trace_add("write", weight_entry_callback)
#author score GUI elements
authorWeightEntryText = StringVar()
authorWeightEntryText.set(defaultRankingWeights[3])
ttk.Label(bookRankingWeightsFrame, width = 40,text = "Author Score Weighting:")\
    .grid(column = 0,row=3,padx=5, pady=5)
ttk.Entry(bookRankingWeightsFrame, width = 5,textvariable = authorWeightEntryText)\
    .grid(column = 1,row=3,padx=5, pady=5)
authorWeightEntryText.trace_add("write", weight_entry_callback)
#not read score GUI elements
notReadWeightEntryText = StringVar()
notReadWeightEntryText.set(defaultRankingWeights[4])
ttk.Label(bookRankingWeightsFrame, width = 40,text = "Not Read Score Weighting:")\
    .grid(column = 0,row=4,padx=5, pady=5)
ttk.Entry(bookRankingWeightsFrame, width = 5,textvariable = notReadWeightEntryText)\
    .grid(column = 1,row=4,padx=5, pady=5)
notReadWeightEntryText.trace_add("write", weight_entry_callback)
#updates the bar chart for book checkouts in the selected genre
def update_genre_results():
    bookrecommend.recommend_books(pie_chart_frame,bar_chart_frame,rank_tree,
        recommend_message_label,recommendBooksMemberIDEntryText.get(),GetRankWeightings(),\
            selected_genre.get(),results_from_book_ranking = results_from_book_ranking)
    return

#make the empty tree for ranking books 
columns = ("Title","Total Score","Popularity","Genre","Purchase Date","Author","Not Read")
rank_tree = ttk.Treeview(bookRankingTreeFrame, columns=columns, show='headings')
rank_tree.configure(height= 16)
columnWidths = 90
rank_tree.column("Title",width= 150)
rank_tree.column("Total Score",width= columnWidths)
rank_tree.column("Popularity",width= columnWidths)
rank_tree.column("Genre",width= columnWidths)
rank_tree.column("Purchase Date",width= columnWidths)
rank_tree.column("Author",width= columnWidths)
rank_tree.column("Not Read",width= columnWidths)
# define headings
for columnName in columns:
    rank_tree.heading(columnName, text = columnName)
rank_tree.grid(row=0, column=0, sticky='nsew')
# add a scrollbar
scrollbar = ttk.Scrollbar(bookRankingTreeFrame, orient=VERTICAL, command=rank_tree.yview)
rank_tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')
#returns the rank weightings inputed into the entries 
def GetRankWeightings():
    popularityWeight = float(popularityWeightEntryText.get())
    genreWeight = float(genreWeightEntryText.get())
    purchaseDateWeight = float(purchaseDateWeightEntryText.get())
    authorWeight = float(authorWeightEntryText.get())
    notReadWeight = float(notReadWeightEntryText.get())
    return (popularityWeight,genreWeight,purchaseDateWeight,authorWeight,notReadWeight)
#callback that updates the genre book checkout bar chart
def genre_combobox_callback(event):
    update_genre_results()
genre_combobox.bind('<<ComboboxSelected>>', genre_combobox_callback)
Label(dropDownFrame, text="Total Book Checkout Counts for Genre:").grid(row=0,column=0,padx=5,pady=5)
genre_combobox.grid(row=0,column=1,padx=5,pady=5)
recommendButton = ttk.Button(recommendBooksEntryFrame, text ="Recommend Books",\
    command=lambda : bookrecommend.recommend_books(pie_chart_frame,bar_chart_frame,\
        rank_tree,recommend_message_label,recommendBooksMemberIDEntryText.get(),GetRankWeightings(),\
            genre_combobox = genre_combobox,results_from_book_ranking = results_from_book_ranking))
recommendButton.grid(row = 0 ,column = 2,padx = 10)
recommend_message_label.grid(row = 1,column = 1,padx = 10)
recommendBooksEntryFrame.pack(pady=10)
#add the pie chart
pie_chart_frame.grid(row = 0, column = 0,padx= 10,pady = 10)
#add the combobox
dropDownFrame.grid(row = 1, column = 0,padx= 5)
#end of drop down for genres
#add the bar chart
bar_chart_frame.grid(row = 2, column = 0,padx= 5,pady = 5)
#add the pie chart and bar chart
recommendBooksGraphsFrame.grid(row = 0, column = 0,padx=10,pady=10)
#add book ranking list
bookRankingWeightsFrame.pack(padx=10,pady=10)
bookRankingTreeFrame.pack(padx=10,pady=10)
bookRankingFrame.grid(row = 0, column = 1,padx=10,pady=10)
results_from_book_ranking.pack(side=TOP, anchor=NW)
#add rank list and adjust weightings to the recommend notebook
rankingNotebook.add(bookRankingTreeFrame,text="Book Rankings")
rankingNotebook.add(bookRankingWeightsFrame,text="Adjust Weightings")
#updates the recommend results when tab is changed between rank list and adjust weightings
def ranking_tab_change(event):
    update_genre_results()
#when rank notebook tab is changed function will be called to update the recommend results
rankingNotebook.bind('<<NotebookTabChanged>>', ranking_tab_change)
rankingNotebook.pack()
recommendBooksResultsFrame.pack()
#add frames to the main notebook
menu_notebook.add(search_menu, text = "Search Books")
menu_notebook.add(checkout_menu, text = "Check Out Book")
menu_notebook.add(return_menu, text = "Return Book")
menu_notebook.add(recommend_menu, text = "Recommend Books")
menu_notebook.pack(expand = False,padx = 10, pady = 10)
#starting search results - all books will be shown
update_search_results()
root.mainloop()

