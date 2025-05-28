# 🎬 Movie Recommender System

This project is a **content-based movie recommendation web app** built with **Streamlit**, using a precomputed similarity matrix and integrated with the **TMDB API** to fetch real-time movie data, posters, and trending content.

---

## 🚀 Features

- 🔐 **User Authentication** (Sign Up / Login with credentials)
- 🎯 **Personalized Movie Recommendations** based on your selected movie
- 🔥 **Trending Movies This Week** from TMDB API
- 🖼️ **Poster Display + Overviews** for both recommendations and trending titles
- 💡 **Error Handling** for API failures and missing data
- 🛡️ **Session State Management** using Streamlit

---

## 🗂️ Project Structure

movie-recommender-system/
│
├── app.py # Main Streamlit application
├── auth.py # Authentication functions (imported in app.py)
├── users.json # Stores user credentials (auto-created/updated)
├── model/
│ ├── movie_list.pkl # DataFrame containing movie titles and TMDB IDs
│ └── similarity.pkl # Cosine similarity matrix between movies
├── requirements.txt # List of required packages
└── README.md # This file


---

## ⚙️ How It Works

- On login/signup, users can:
  - Browse **Trending Movies**
  - Select a movie and get **Top 5 Recommendations**
- Movie metadata is enhanced using the **TMDB API** to show posters, overviews, and popularity scores.
- Recommender is based on **cosine similarity** between movie feature vectors.

---

## 📦 Required Files for GitHub

Ensure your file includes:

- ✅ `app.py`
- ✅ `auth.py`
- ✅ `model/movie_list.pkl`
- ✅ `model/similarity.pkl`
- ✅ `README.md`
- ✅ `requirements.txt`
- ❌ `users.json` (optional; gets created automatically when a user signs up)

---

## 🔑 TMDB API Setup

1. Create an account on [The Movie Database](https://www.themoviedb.org/)
2. Get an API key from your account's developer settings
3. In `app.py`, replace the `API_KEY` value:

```python
API_KEY = "your_tmdb_api_key"

## 🖥️ Installation & Running the App

Step 1: Clone the Repository
git clone https://github.com/yourusername/movie-recommender-system.git
cd movie-recommender-system

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Run the App
streamlit run app.py




