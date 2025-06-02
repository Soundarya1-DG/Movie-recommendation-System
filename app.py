import streamlit as st
import requests
import pickle
import json
import os

API_KEY = "1d3a1ef6fcb1d7735b82d0265eac14ea"
USER_FILE = "users.json"

# ----------------------- AUTH FUNCTIONS ----------------------- #

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def add_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

def validate_login(username, password):
    users = load_users()
    return username in users and users[username] == password

# ----------------------- MOVIE FUNCTIONS ----------------------- #

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', '')
    overview = data.get('overview', 'Overview not available.')
    full_poster_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ''
    return full_poster_path, overview

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overviews = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, overview = fetch_movie_details(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)
        recommended_movie_overviews.append(overview)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_overviews

def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    trending_data = []
    for movie in data.get('results', [])[:10]:
        title = movie.get('title', 'Unknown')
        poster_path = movie.get('poster_path', '')
        overview = movie.get('overview', 'Overview not available.')
        popularity = movie.get('popularity', 'N/A')
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ''
        trending_data.append((title, poster_url, overview, popularity))
    return trending_data

# ----------------------- SESSION STATE ----------------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------------- LOGIN/SIGNUP PAGES ----------------------- #

def login_page():
    st.title("🔐 Login to Movie Recommender")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

def signup_page():
    st.title("📝 Signup for Movie Recommender")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    if st.button("Signup"):
        if add_user(username, password):
            st.success("Account created! Please login.")
        else:
            st.error("Username already exists")

# ----------------------- AUTH GATE ----------------------- #

if not st.session_state.logged_in:
    st.sidebar.title("Welcome")
    choice = st.sidebar.radio("Login / Signup", ["Login", "Signup"])
    if choice == "Login":
        login_page()
    else:
        signup_page()
    st.stop()

# ----------------------- MAIN APP ----------------------- #

# Logout Button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.sidebar.success(f"Logged in as: {st.session_state.username}")
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose Option", ["🎯 Recommended Movies", "🔥 Trending Movies"])

st.title("🎬 Movie Recommender System")

# Load Models
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Recommended Movies
if option == "🎯 Recommended Movies":
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)
    if st.button('Show Recommendation'):
        names, posters, overviews = recommend(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
                with st.expander("Show Overview"):
                    st.write(overviews[i])

# Trending Movies
elif option == "🔥 Trending Movies":
    st.subheader("🔥 Top 10 Trending Movies This Week")
    trending = get_trending_movies()
    for row in range(0, 10, 5):
        cols = st.columns(5)
        for i in range(5):
            idx = row + i
            if idx < len(trending):
                title, poster, overview, popularity = trending[idx]
                with cols[i]:
                    st.text(title)
                    st.image(poster)
                    with st.expander("Show Overview"):
                        st.write(overview)
                        st.markdown(f"**Popularity:** {popularity}")
