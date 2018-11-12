import os
import requests

def json_Goodreads(isbn):
    """JSON response from GoodReads API as dictionary
    """
    KEY = os.getenv("KEY")
    res = requests.get('https://www.goodreads.com/book/review_counts.json',
                       params={"key": KEY, "isbns": isbn})

    resJson = res.json()
    resGoodreads = {'average_rating': None, 'work_ratings_count': None}

    if res.status_code == requests.codes.ok:        
        resGoodreads['average_rating'] = resJson['books'][0]['average_rating']
        resGoodreads['work_ratings_count'] = resJson['books'][0]['work_ratings_count']        
    
    return resGoodreads
