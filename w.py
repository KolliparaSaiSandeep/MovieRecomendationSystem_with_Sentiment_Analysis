import html5lib as html5lib
import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st
import pickle
import sklearn
import requests
import json
import webbrowser

a=[]
cla=pickle.load(open(r"C:\Users\ksai1\PycharmProjects\moviesrecommendetemrsys\Movies_Review_Classification.pkl",'rb'))
save_cv = pickle.load(open(r"C:\Users\ksai1\PycharmProjects\moviesrecommendetemrsys\count-Vectorizer (1).pkl",'rb'))

def ji(nam,b):
  print("hi")
  c = 'https://www.imdb.com'
  print(c+b)
  request=requests.get("https://www.imdb.com"+str(b)+"reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter=0")
  print("https://www.imdb.com"+str(b)+"reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter=0")
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
  st.write("Reload the app for seeing next review")


def test_model(sentence):
   sen = save_cv.transform([sentence]).toarray()
   res = cla.predict(sen)[0]
   if res == 1:
      return 'Positive review'
   else:
      return 'Negative review'
