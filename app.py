import streamlit as st
import pandas as pd
from pickle4 import pickle
import requests
import bz2file as bz2

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    recommended_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    posters = []
    for i in recommended_movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, posters

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=21f7e0cb18010d8a186cb8241f816bbf&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity_data = bz2.BZ2File('similarity.pbz2', 'rb')
similarity = pickle.load(similarity_data)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'I would like to see movies like:',
   movies['title'].values)

st.write('You selected:', selected_movie_name)

if st.button('Recommend'):
    # poster = fetch_poster(2700)
    # st.image(poster)
    names, poster_paths = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster_paths[0])
    with col2:
        st.text(names[1])
        st.image(poster_paths[1])
    with col3:
        st.text(names[2])
        st.image(poster_paths[2])
    with col4:
        st.text(names[3])
        st.image(poster_paths[3])
    with col5:
        st.text(names[4])
        st.image(poster_paths[4])
    
    

    
