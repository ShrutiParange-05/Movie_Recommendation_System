import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- Load Data --------------------
movies = pickle.load(open('movies.pkl', 'rb'))  # Must contain a 'title' column
similarity = pickle.load(open('similarity.pkl', 'rb'))

# List of movie titles for the dropdown
movies_list = movies['title'].values

# -------------------- Poster Fetch Function --------------------
def fetch_poster(movie_title):
    api_key = 'c98909c8'  # 🔑 Replace with your own OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    poster_url = data.get('Poster')
    if poster_url and poster_url != "N/A":
        return poster_url
    else:
        return 'https://via.placeholder.com/200x300?text=No+Poster'

# -------------------- Recommendation Logic --------------------
def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_indices:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommendation System')

selected_movie = st.selectbox("Select a Movie", movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            st.text(names[idx])
            st.image(posters[idx], width=180)
