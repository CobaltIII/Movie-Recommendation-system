# Movie-Recommendation-system
A movie recommendation system based on basics of matrices and searching (No Artificial Intelligence used)

### Data Used - 
   - 25m repository of data on _*movies and their ratings*_

### Concept Used - 

Search a movie and if that movie is found it finds movies that others liked based on if they liked your searched movie or not

We start with searching for a movie in the repository and then getting its unique movieId
We then search for all people who liked this movie (rated it a 4 or above out of 5)
We then get all the movies that these people liked and select the most niche ones pertaining to our searched movie and show the results.
