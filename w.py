import pickle
import streamlit as st
import requests
import html5lib as html5lib
import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st
import sklearn
import json
import webbrowser


cla=pickle.load(open(r"D:\Movie recommendation system\Movies_Review_Classification.pkl",'rb'))
save_cv = pickle.load(open(r"D:\Movie recommendation system\count-Vectorizer.pkl",'rb'))


def ji(nam,b):
  print("hi")
  a=[]
  c = 'https://www.imdb.com'
  print(c+b)
  request=requests.get("https://m.imdb.com/title/"+str(b)+"/reviews?spoiler=hide&sort=totalVotes&dir=desc")
  soup=BeautifulSoup(request.text,'html.parser')
  mydivs = soup.find_all("div", {"class": "text"})
  l=0
  for i in mydivs:
   if(l<10):
      a.append(i.text)
   else:
      break
  res=[]
  g = []
  i = 0
  for i in range(len(a)):
    g.append(test_model(a[i]))
  st.write("SENTIMENTAL ANALYSIS OF FEATURED REVIEWS")
  data = {'Featured Reviews': a,
          'Sentiment': g}
  q=pd.DataFrame(data)
  st.write(q)


def test_model(sentence):
   sen = save_cv.transform([sentence]).toarray()
   res = cla.predict(sen)[0]
   if res == 1:
      return 'Positive review'
   else:
      return 'Negative review'

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

import requests
def imdbid(mov):
    url= "http://www.omdbapi.com/?apikey=fa2d3923&t="+mov
    response = requests.get(url)
    data = response.json()
    return data["imdbID"]


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        a=st.button("Review",key="review1")
        st.write(ji(recommended_movie_names[0],imdbid(recommended_movie_names[0])))
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        a=st.button("Review",key="review2")
        st.write(ji(recommended_movie_names[1],imdbid(recommended_movie_names[1])))
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        a=st.button("Review",key="review3")
        st.write(ji(recommended_movie_names[2],imdbid(recommended_movie_names[2])))
