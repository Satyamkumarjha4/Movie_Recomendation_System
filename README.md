# Movie Buddy – Complete Movie Recommendation System Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Directory & File Structure](#directory--file-structure)
4. [Data Flow: From Raw Data to Recommendations](#data-flow-from-raw-data-to-recommendations)
5. [Module-by-Module Explanation](#module-by-module-explanation)
    - [Data Ingestion](#data-ingestion)
    - [Data Transformation](#data-transformation)
    - [Similarity Computation](#similarity-computation)
    - [Utilities](#utilities)
    - [Exception & Logging](#exception--logging)
    - [Streamlit Frontend](#streamlit-frontend)
6. [Setup & Installation](#setup--installation)
7. [Usage Instructions](#usage-instructions)
8. [API Key Management](#api-key-management)
9. [Extending the Project](#extending-the-project)
10. [Troubleshooting & FAQ](#troubleshooting--faq)
11. [Contact & Credits](#contact--credits)

---

## Project Overview

**Movie Buddy** is a modular, content-based movie recommendation system. It uses NLP and cosine similarity to recommend movies based on metadata (overview, genres, cast, crew, keywords). The system features a modern Streamlit web interface and fetches real-time movie details (posters, ratings, etc.) from the TMDb API.

**Key Features:**
- Content-based recommendations (no user history needed)
- Modular, extensible Python codebase
- Clean, interactive UI with Streamlit
- Real-time metadata from TMDb API
- Handles large datasets efficiently

---

## System Architecture

**High-Level Flow:**
1. **Data Ingestion:** Load and merge raw movie and credit data.
2. **Data Transformation:** Clean, normalize, and engineer features (tags).
3. **Similarity Computation:** Vectorize tags and compute cosine similarity matrix.
4. **Frontend:** User selects a movie, system recommends similar movies, and fetches details from TMDb API.

---

## Directory & File Structure

```
Movie_Recomendation_System/
│
├── main.py                  # Streamlit app (frontend)
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── README.md                # Project documentation
├── .env                     # (User-created) TMDb API key
│
├── src/
│   ├── utils.py             # Helper functions (parsing, stemming, save/load)
│   ├── logger.py            # Logging setup
│   ├── exception.py         # Custom exception class
│   └── components/
│       ├── data_ingestion.py        # Data loading/merging
│       ├── data_transformation.py   # Feature engineering
│       └── similarity.py            # Similarity matrix computation
│
├── artifacts/               # Generated data & models
│   ├── merged_data.csv      # Merged raw data
│   ├── movie_data.csv       # Full metadata after transformation
│   ├── data.csv             # Simplified data (id, title, tags)
│   └── similarity.pkl       # Cosine similarity matrix
│
├── notebook/                # Jupyter notebook for prototyping
│   ├── MSR.ipynb            # End-to-end workflow in notebook form
│   └── Dataset/
│       ├── tmdb_5000_movies.csv
│       └── tmdb_5000_credits.csv
│
├── .devcontainer/           # (Optional) Dev environment config
│   └── devcontainer.json
└── my_package.egg-info/     # Package metadata (auto-generated)
```

---

## Data Flow: From Raw Data to Recommendations

1. **Raw Data**: Downloaded from Kaggle (movies and credits CSVs).
2. **Data Ingestion**: Merges and filters relevant columns, saves as `merged_data.csv`.
3. **Data Transformation**: Cleans, normalizes, and creates a `tags` column (combining overview, genres, keywords, cast, director). Outputs `movie_data.csv` and `data.csv`.
4. **Similarity Computation**: Vectorizes `tags` using `CountVectorizer`, computes cosine similarity, and saves as `similarity.pkl`.
5. **Frontend**: Loads processed data and similarity matrix. User selects a movie, and the app recommends similar movies, fetching additional details from TMDb API.

---

## Module-by-Module Explanation

### Data Ingestion
- **File:** `src/components/data_ingestion.py`
- **Purpose:** Reads raw CSVs, merges them, selects relevant columns, and removes missing data.
- **Output:** `artifacts/merged_data.csv`
- **How it works:**
  - Reads `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.
  - Merges on `title`.
  - Keeps only `id`, `title`, `genres`, `keywords`, `overview`, `cast`, `crew`.
  - Drops rows with missing values.

### Data Transformation
- **File:** `src/components/data_transformation.py`
- **Purpose:** Cleans and processes metadata, creates a unified `tags` column for each movie.
- **Key Steps:**
  - Converts stringified lists (genres, keywords, cast, crew) to Python lists.
  - Extracts top 5 cast members and director.
  - Removes spaces in names for better tokenization.
  - Stems and lowercases overview text.
  - Combines all features into a single `tags` list.
  - Outputs:
    - `movie_data.csv`: Full metadata
    - `data.csv`: Only `id`, `title`, `tags`

### Similarity Computation
- **File:** `src/components/similarity.py`
- **Purpose:** Computes similarity between movies based on their tags.
- **How it works:**
  - Uses `CountVectorizer` (max 10,000 features, English stop words removed) to vectorize tags.
  - Computes cosine similarity between all movie vectors.
  - Saves the similarity matrix as `similarity.pkl`.

### Utilities
- **File:** `src/utils.py`
- **Functions:**
  - `save_object`, `load_object`: Save/load Python objects (e.g., pickle files).
  - `convert`: Parses stringified lists (e.g., genres, keywords, cast).
  - `fetch_director`: Extracts director from crew list.
  - `stem`: Applies stemming to text for normalization.

### Exception & Logging
- **Files:** `src/exception.py`, `src/logger.py`
- **Purpose:**
  - Custom exception class for detailed error messages.
  - Logging setup to track pipeline progress and errors.

### Streamlit Frontend
- **File:** `main.py`
- **Features:**
  - Modern, responsive UI with custom CSS.
  - Movie selection with autocomplete and optional filters.
  - Fetches posters, ratings, year, and overview from TMDb API.
  - Displays genres, top 5 cast, and director.
  - Shows N most similar movies (configurable by user).
  - Caches API calls for performance.
  - Error handling and user feedback.

---

## Setup & Installation

1. **Clone the repository**
   ```sh
   git clone <repo-link>
   cd Movie_Recomendation_System
   ```
2. **Set up a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Download the datasets**
   - Place `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in `notebook/Dataset/`.
5. **Set up your TMDb API key**
   - Create a `.env` file in the project root:
     ```
     APIKEY=your_tmdb_api_key_here
     ```
6. **Run the data pipeline (optional, if you want to regenerate artifacts)**
   ```sh
   python src/components/data_ingestion.py
   ```
7. **Launch the Streamlit app**
   ```sh
   streamlit run main.py
   ```

---

## Usage Instructions

- Open the app in your browser (Streamlit will provide a local URL).
- Select a movie from the dropdown (search or scroll).
- View details: poster, rating, year, overview, genres, cast, director.
- Get recommendations: N most similar movies, each with full metadata.
- Use filters to adjust the number of recommendations.

---

## API Key Management

- The TMDb API key is required for fetching posters, ratings, and overviews.
- Store your API key in a `.env` file in the project root as:
  ```
  APIKEY=your_tmdb_api_key_here
  ```
- The app loads this key using the `python-dotenv` package.

---

## Extending the Project

- **Add new features:**
  - Implement collaborative filtering or hybrid models.
  - Add user authentication and watchlists.
  - Integrate more advanced NLP (e.g., BERT embeddings).
- **Use new datasets:**
  - Update the ingestion and transformation scripts to handle new data formats.
- **Improve UI:**
  - Add more filters (genre, year, rating).
  - Enhance visualizations and interactivity.
- **Deployment:**
  - Deploy on Streamlit Cloud, Heroku, or your own server.

---

## Troubleshooting & FAQ

**Q: The app says data files are missing!**
- Ensure you have run the data pipeline and that `artifacts/data.csv`, `artifacts/movie_data.csv`, and `artifacts/similarity.pkl` exist.

**Q: TMDb API calls fail or return no poster/rating.**
- Check your `.env` file and API key validity.
- Ensure you have internet access.

**Q: Streamlit app won’t start or crashes.**
- Check Python version (3.7+ recommended).
- Ensure all dependencies are installed.
- Check logs for detailed error messages.

**Q: How do I regenerate the similarity matrix after changing data?**
- Rerun the data pipeline:
  ```sh
  python src/components/data_ingestion.py
  ```

---

## Contact & Credits

- **Developer:** Satyam Kumar Jha
- **Email:** satyamjha4@gmail.com
- **GitHub:** https://github.com/Satyamkumarjha4/Movie_Recomendation_System
- **Data Source:** [Kaggle TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- **API:** [The Movie Database (TMDb)](https://www.themoviedb.org/documentation/api)

---

**This documentation is designed to be fully self-explanatory. By following it, you can understand, run, and extend the Movie Buddy system from scratch.**

