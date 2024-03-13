import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer as Tf
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")

def clean(title):
    cleanedtitle = re.sub("[^a-zA-Z0-9 ]" , "" , title)
    return cleanedtitle
    #strips the titles of filler characters
    
movies["clean_title"] = movies["title"].apply(clean)


vectorizer = Tf(ngram_range=(1,2)) 
                            #looks at pairs of words too, like not just
                            #"toy" , it looks at "toy story" too
        
tfidf = vectorizer.fit_transform(movies["clean_title"])

def searching(title):
    title = clean(title)
    query_vector = vectorizer.transform([title])
    similarity = cosine_similarity(query_vector , tfidf).flatten()
    indices = np.argpartition(similarity , -5)[-5:]
    results = movies.iloc[indices][::-1]
    return results

ratings = pd.read_csv("ratings.csv")


def find_same_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_recs = similar_recs.value_counts() / len(similar_users)

    similar_recs = similar_recs[similar_recs > 0.1]
    
    all_users = ratings[(ratings["movieId"].isin(similar_recs.index)) & (ratings["rating"] > 4)]
    all_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    
    
    rec_percents = pd.concat([similar_recs , all_recs] , axis = 1)
    rec_percents.columns = ["similar" , "all"]
    
    rec_percents["score"] = rec_percents["similar"] / rec_percents["all"]
    rec_percents = rec_percents.sort_values("score" , ascending = False)
    return rec_percents.head(15).merge(movies , left_index = True , right_on = "movieId")[["score" ,"title"]]
Menu = """Choose an option : 
  -  Enter 1 to Try the recommendation program on your own
  -  Enter 2 to Look at the sample recommendations for "Toy Story"
  -  Enter 3 to Look at the sample recommendations for "The Avengers 2012" 
  -  Enter 4 to Look at the sample recommendations for "Yeh Jawaani Hai Deewani 2013"
  -  Enter 5 to Look at the sample recommendations for "Aux yeux de tous"
  -  Enter 6 to Exit"""


print(Menu)

choice = 0

while choice != 6:
    
    choice = str(input("Enter your choice : "))
    
    if choice == "1":
        searchquery = str(input("Enter the movie you like : "))
        results = searching(searchquery)
        movie_id = results.iloc[0]["movieId"]
        print(find_same_movies(movie_id))
        
    elif choice == "2":
        print("***** Choice = Toy Story ****")
        searchquery = "Toy Story"
        results = searching(searchquery)
        movie_id = results.iloc[0]["movieId"]
        print(find_same_movies(movie_id))
        
    elif choice == "3":
        print("***** Choice = The Avengers 2012 ****")
        searchquery = "The Avengers 2012" 
        results = searching(searchquery)
        movie_id = results.iloc[0]["movieId"]
        print(find_same_movies(movie_id))
        
    elif choice == "4":
        print("***** Choice = Yeh Jawaani Hai Deewani 2013 ****")
        searchquery = "Yeh Jawaani Hai Deewani 2013"
        results = searching(searchquery)
        movie_id = results.iloc[0]["movieId"]
        print(find_same_movies(movie_id))
        
    elif choice == "5":
        print("***** Choice = Aux yeux de tous ****")
        searchquery = "Aux yeux de tous"
        results = searching(searchquery)
        movie_id = results.iloc[0]["movieId"]
        print(find_same_movies(movie_id))
        
    else:
        print("Oops, Invalid input, try again please")
    


searchquery = str(input("Enter the movie you like : "))

results = searching(searchquery)
movie_id = results.iloc[0]["movieId"]
print(find_same_movies(movie_id))
