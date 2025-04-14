import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np
import os
import ast
from dotenv import load_dotenv
import time

# Page configuration
st.set_page_config(
    page_title="Movie Buddy - Personalized Recommendations",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0083B8;
        margin-bottom: 2rem;
    }
    .movie-title {
        font-weight: bold;
        font-size: 1rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    .poster-container {
        transition: transform 0.3s;
    }
    .poster-container:hover {
        transform: scale(1.05);
    }
    .recommendation-header {
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #0083B8;
        text-align: center;
    }
    .movie-info {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .rating-year {
        font-size: 0.9rem; 
        color: #606060;
    }
    .placeholder {
        height: 400px;
        background-color: #f0f2f6;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #606060;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #606060;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()
API_KEY = os.getenv('APIKEY')

# Cache API calls to improve performance
@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    """Fetch movie details including poster, rating, year, and overview"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return {
                "poster_path": None,
                "rating": "N/A",
                "year": "N/A",
                "overview": "Information not available"
            }
            
        data = response.json()
        
        return {
            "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}" if data.get('poster_path') else None,
            "rating": round(data.get('vote_average', 0), 1),
            "year": data.get('release_date', '')[:4] if data.get('release_date') else "N/A",
            "overview": data.get('overview', 'No overview available')
        }
    except Exception as e:
        st.error(f"Error fetching movie details: {e}")
        return {
            "poster_path": None,
            "rating": "N/A",
            "year": "N/A",
            "overview": "Information not available"
        }

def recommend(movie, num_recommendations=5):
    """Generate movie recommendations based on similarity"""
    try:
        # Find the movie in our dataset
        if movie not in movies['title'].values:
            return [], [], [], [], []
            
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_ratings = []
        recommended_movie_years = []
        recommended_movie_overviews = []
        
        # Get top N recommendations
        for i in distances[1:num_recommendations+1]:
            movie_id = movies.iloc[i[0]].id
            movie_details = fetch_movie_details(movie_id)
            
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_posters.append(movie_details["poster_path"])
            recommended_movie_ratings.append(movie_details["rating"])
            recommended_movie_years.append(movie_details["year"])
            recommended_movie_overviews.append(movie_details["overview"])

        return recommended_movie_names, recommended_movie_posters, recommended_movie_ratings, recommended_movie_years, recommended_movie_overviews
        
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], [], [], [], []

def load_data():
    """Load movie data and similarity matrix with error handling"""
    try:
        # Load movies dataset
        movies = pd.read_csv('artifacts/data.csv')
        
        # Load similarity matrix
        with open('artifacts/similarity.pkl', 'rb') as file:
            similarity = pickle.load(file)
            
        return movies, similarity
    except FileNotFoundError as e:
        st.error(f"Required data files not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Main app
try:
    # App Header
    st.markdown("<h1 class='main-header'>🎬 Movie Buddy</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Discover movies you'll love based on your favorites</p>", unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading movie database..."):
        movies, similarity = load_data()
    
    # Create tabs for different features
    tab1, tab2 = st.tabs(["Find Recommendations", "About"])
    
    with tab1:
        # Left column for selection
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Select a movie")
            # Sort movies alphabetically for easier navigation
            movie_list = sorted(movies['title'].values)
            
            # Add search box with autocomplete
            selected_movie = st.selectbox(
                "Type or select a movie",
                movie_list,
                index=None,
                placeholder="Search for a movie...",
            )
            
            # Genre filter (optional feature)
            show_filters = st.checkbox("Show filters")
            
            if show_filters:
                num_recommendations = st.slider("Number of recommendations", min_value=1, max_value=12, value=4)
            else:
                num_recommendations = 4
                
            # Only show button if a movie is selected
            if selected_movie:
                recommend_button = st.button('Get Recommendations', use_container_width=True, type="primary")
            else:
                st.info("Select a movie to get recommendations")
                recommend_button = False
        
        # Display selected movie info (if any)
        with col2:
            if selected_movie:
                try:
                    movie_id = movies[movies['title'] == selected_movie]['id'].values[0]
                    movie_details = fetch_movie_details(movie_id)
                    
                    st.subheader("Selected Movie")
                    selected_col1, selected_col2 = st.columns([1, 2])
                    
                    with selected_col1:
                        if movie_details["poster_path"]:
                            st.image(movie_details["poster_path"], width=360)
                        else:
                            st.markdown("<div class='placeholder' style='height:200px'>No Poster Available</div>", unsafe_allow_html=True)
                    
                    with selected_col2:
                        st.markdown(f"### {selected_movie}")
                        st.markdown(f"<span class='rating-year'>⭐ {movie_details['rating']} | {movie_details['year']}</span>", unsafe_allow_html=True)
                        st.markdown("#### Overview")
                        st.markdown(f"{movie_details['overview']}")
                        st.markdown("#### Genres")
                        # Load merged data for additional details
                        merged_data = pd.read_csv('artifacts/movie_data.csv')
                        
                        # Fetch genres
                        genres = merged_data[merged_data['title'] == selected_movie]['genres'].values[0]
                        if isinstance(genres, str):
                            genres = ast.literal_eval(genres)  # Convert string to list using ast.literal_eval
                        st.markdown(", ".join(sorted(genres)))  # Sort genres alphabetically
                        
                        # Fetch cast
                        st.markdown("#### Cast")
                        cast = merged_data[merged_data['title'] == selected_movie]['cast'].values[0]
                        if isinstance(cast, str):
                            cast = ast.literal_eval(cast)  # Convert string to list using ast.literal_eval
                        st.markdown(", ".join(sorted(cast[:5])))  # Sort and show top 5 cast members
                        
                        # Fetch director
                        st.markdown("#### Director")
                        director = merged_data[merged_data['title'] == selected_movie]['director'].values[0]
                        if isinstance(director, str):
                            director = ast.literal_eval(director)  # Convert string to list using ast.literal_eval
                        st.markdown(", ".join(sorted(director)))  # Sort directors alphabetically
                except Exception as e:
                    st.error(f"Error displaying movie information: {e}")
            else:
                st.markdown("<div class='placeholder'>Select a movie to see details</div>", unsafe_allow_html=True)
        
        # Show recommendations when button is clicked
        if recommend_button:
            with st.spinner('Finding movies you might like...'):
                recommended_names, recommended_posters, recommended_ratings, recommended_years, recommended_overviews = recommend(selected_movie, num_recommendations)
                
                if recommended_names:
                    st.markdown(f"<h3 class='recommendation-header'>Top {len(recommended_names)} Recommendations for \"{selected_movie}\"</h3>", unsafe_allow_html=True)
                    
                    # Create columns for recommendations
                    cols = st.columns(min(4, len(recommended_names)))
                    
                    for i in range(len(recommended_names)):
                        col_index = i % len(cols)
                        with cols[col_index]:
                            st.markdown(f"<div class='poster-container'>", unsafe_allow_html=True)
                            if recommended_posters[i]:
                                st.image(recommended_posters[i], width=250, caption=None)
                            else:
                                st.markdown("<div class='placeholder' style='height:225px'>No Poster</div>", unsafe_allow_html=True)
                                
                            st.markdown(f"<p class='movie-title'>{recommended_names[i]}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p class='rating-year'>⭐ {recommended_ratings[i]} | {recommended_years[i]}</p>", unsafe_allow_html=True)
                            
                            
                else:
                    st.warning("Could not generate recommendations for this movie. Please try another one.")
    
    with tab2:
        st.write("""
        # 🎬 Movie Buddy - Personalized Recommendation System

        ## 🔍 Project Flow & Architecture

        ---

        ### 📥 Data Ingestion (`data_ingestion.py`)

        - **Source**: Local CSV files downloaded from Kaggle.
        - **Files Used**: `movies.csv`, `credits.csv`.
        - **Process**:
        - Reads both CSVs.
        - Merges them on the `title` or `id` key.
        - Stores the merged file as a single CSV for further processing.

        ---

        ### 🔧 Data Transformation (`data_transformation.py`)

        - **Objective**: Clean, simplify, and engineer features for movie similarity.
        - **Key Steps**:
        - **Column Selection**: Extract only required columns (`title`, `overview`, `genres`, `keywords`, `cast`, `crew`).
        - **Cast**: From a dictionary list, extract top 5 actors' names.
        - **Crew**: Extract only the director’s name.
        - **Genres & Keywords**: Parse and keep only the names (removing IDs).
        - **Text Normalization**:
            - Convert multi-word names into single words (e.g., "Robert Downey Jr" → "RobertDowneyJr").
            - Convert the `overview` text into a list of words.
        - **Tags Creation**:
            - Combine `overview`, `cast`, `director`, `keywords`, and `genres` into a unified `tags` column.
        - **Output Files**:
            - `movie_data.csv`: Full movie metadata.
            - `data.csv`: Reduced version with `id`, `title`, and `tags`.

        ---

        ### 🧠 Similarity Computation (`similarity.py`)

        - **Vectorization**: `CountVectorizer` with:
        - Max 10,000 features.
        - English stop words removed.
        - **Similarity Measure**: Cosine similarity on vectorized `tags`.
        - **Output**: Serialized `similarity.pkl` file using Pickle.

        ---

        ### 🖥️ Main Flow (`main.py`) – Streamlit App

        #### ✅ User Flow

        1. User selects a movie.
        2. App displays:
        - Poster
        - Overview
        - Genres
        - Top 5 Cast
        - Rating & Year
        3. Recommends `N` similar movies based on cosine similarity.

        #### 🎨 UI/UX Highlights

        - Custom CSS for professional layout and interactivity.
        - Uses TMDb API to dynamically fetch:
        - Posters
        - Ratings
        - Year
        - Overview

        #### 🔄 Functional Highlights

        - Caching with `@st.cache_data` to reduce API calls.
        - Recommendation logic:
        - Matches selected movie index.
        - Sorts by similarity score.
        - Retrieves top N recommendations (excluding the selected one).

        #### 📂 Data Files Used

        - `artifacts/data.csv`: Used for loading titles and tags.
        - `artifacts/movie_data.csv`: Used for metadata like genres and cast.
        - `artifacts/similarity.pkl`: Precomputed cosine similarity matrix.

        ---

        ### 🔑 API Key Handling

        - TMDb API Key is loaded securely via `.env` file using `dotenv`.

        ---

        ### 📌 Dependencies

        - `streamlit`
        - `pandas`
        - `numpy`
        - `requests`
        - `scikit-learn`
        - `dotenv`
        - `pickle`
        - `ast`

        ---

        ### 🧾 Sample Output

        Upon selecting a movie like _Inception_, the user will see:
        - Poster of Inception
        - Key info like rating, release year, and overview
        - Genre and cast
        - 4 similar movies recommended with the same metadata shown

        ---

        ### 🚀 Future Improvements

        - Add genre/category filters for smarter recommendations.
        - Improve NLP processing on overview text.
        - Integrate user login to store watchlists or preferences.

        ---

        """)
        
    # Footer
    st.markdown("<div class='footer'>© 2025 Movie Buddy | Powered by The Movie Database (TMDb) API</div>", unsafe_allow_html=True)
    
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.markdown("Please try refreshing the page or contact support if the issue persists.")