# Movie Buddy - Personalized Movie Recommendation System

Movie Buddy is a modular, developer-friendly, content-based movie recommendation system built with Streamlit. It leverages NLP techniques and cosine similarity to recommend similar movies based on a unified textual representation of metadata. Posters and ratings are dynamically fetched via the TMDb API.

---

## System Architecture Overview

The project consists of the following core modules:

1. **Data Ingestion**
2. **Data Transformation & Feature Engineering**
3. **Similarity Computation**
4. **Streamlit Frontend**

---

## Data Ingestion (`data_ingestion.py`)

- **Source**: Kaggle datasets
- **Input Files**: `movies.csv`, `credits.csv`
- **Steps**:
  - Read datasets using Pandas
  - Merge them on a common key (`id` or `title`)
  - Save the result as `merged_data.csv`

---

## Data Transformation (`data_transformation.py`)

Transforms and prepares data for similarity computation.

- **Processes**:
  - Filter necessary columns: `title`, `overview`, `genres`, `keywords`, `cast`, `crew`
  - Extract top 5 cast members and the director
  - Normalize and tokenize text data
  - Generate a `tags` column by combining all textual metadata
- **Outputs**:
  - `movie_data.csv`: Full metadata
  - `data.csv`: Simplified version with `id`, `title`, and `tags`

---

## Similarity Computation (`similarity.py`)

Computes cosine similarity between movies based on tag vectors.

- **Vectorization**: `CountVectorizer` with max 10,000 features and English stop words removal
- **Metric**: Cosine similarity
- **Output**: `similarity.pkl` (Pickle file with similarity matrix)

---

## Streamlit Frontend (`main.py`)

Interactive web interface for movie selection and recommendation.

- **User Flow**:
  1. Select a movie from a dropdown
  2. View movie details and similar recommendations

- **Features**:
  - Responsive layout with custom CSS
  - Data fetched via TMDb API:
    - Poster
    - Rating
    - Overview
    - Release year
  - Caching via `@st.cache_data` to reduce redundant API calls

- **Uses**:
  - `data.csv` for tags
  - `movie_data.csv` for display
  - `similarity.pkl` for recommendations

---

## API Key Handling

API credentials are managed securely via a `.env` file using the `python-dotenv` package.

---

## Project Dependencies

Listed in `requirements.txt`:

- streamlit
- pandas
- numpy
- scikit-learn
- requests
- python-dotenv
- pickle
- ast

---

## Installation & Setup

1. **Clone the repository using Git LFS**

```sh
git lfs install
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

4. **Run the application**

```sh
streamlit run main.py
```

---

## Usage

- Launch the app with `streamlit run main.py`
- Select a movie to view recommendations and details

---

## Deployment

Live demo: [Movie Buddy on Streamlit](https://movie-recomendation-system-skj.streamlit.app/)

---

## Contact

- **Developer**: Satyam Kumar Jha
- **Email**: [satyamjha4@gmail.com](mailto:satyamjha4@gmail.com)
- **GitHub**: [Movie Recommendation System](https://github.com/Satyamkumarjha4/Movie_Recomendation_System)

