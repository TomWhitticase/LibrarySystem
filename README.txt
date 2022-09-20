PROBLEM: search results for overdue books are highlighted red but when i run program in Haslegrave the highlight does not appear

Book search extra functionality:
    Search results are automatically updated when typing in the search bar entry.
    The search field (default is book title) can be changed by user.
    The results can be sorted by different properties (default is book ID)

Book checkout and return extra functionality:
    Multiple books can be checked out and returned at the same time.
    To checkout or return multiple books at once, enter book IDs into the entry boxes separating each
    ID by a comma.

Book Recommendations Explanation:
    5 books will be recommended to the member every time
        the 5 books recommended will be the 5 books with the highest ranking score
        ranking score is calculated by using 5 different scores 
    popularity score- this score is based on the total times the book has been taken out compared to all the other books
        e.g. a book that has been taken out the least will get a score of 0 and the book that has been taken out the most will
        get a score of 100
    genre score- this is based on how many books the user has taken out from the given books genre. e.g. if the book is
        in the members most read genre then it will get a score of 100 and if the book is in a genre the member has not read
        then its score will be 0
    purchase date score- this score is calculated by comparing the purchase date of a book wil with the purchase date of
        the database's oldest and newest books. e.g. the newest book in the database will get a score of 100 and the oldest book
        will get a score of 0.
    author score- this is based on how many books the user has taken out by the given books author. e.g. if the book is
        by the members most read author then it will get a score of 100 and if the book is by a author the member has not read
        then its score will be 0
    not read score- This score is calculated by finding out how many times the member has taken the book out and giving books
        that have been taken out the least a higher score. e.g. the member's most checked out book will have a score of 0 and
        any books they have not read will have a score of 100
    The total score is calculated using all these scores and the weightings given to each score. The librarian can adjust the
    weightings if they feel different properties are more important. e.g. if the librarian only wants to recommend books that
    are new they can make the purchase date weighting very high or if they only want to recommend books that are from the
    members preferred genre then they make the genre weighting very high.
    weightings can be adjusted in the 'adjust weighting' tab above the book ranking list in the recommend menu
    Default weightings are values that i personally have decided would result in appropriate book recommendations:
       
