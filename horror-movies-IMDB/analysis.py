import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

class MovieAnalyzer:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self._clean_data()

    def _clean_data(self):
        self.df['Votes'] = self.df['Votes'].astype(str).str.replace(',', '').astype(int)
        self.df['Gross'] = self.df['Gross'].astype(str).str.replace('$', '').str.replace('M', '').replace('', '0')
        self.df['Gross'] = pd.to_numeric(self.df['Gross'], errors='coerce').fillna(0)

    def import_dataset(self) -> pd.DataFrame:
        return self.df

    def print_first_five(self) -> pd.DataFrame:
        return self.df.head(5)

    def get_dataset_length(self) -> int:
        return len(self.df)

    def get_headers(self) -> list:
        return list(self.df.columns)

    def get_movies_from_1980(self) -> pd.DataFrame:
        return self.df[self.df['Movie Year'] >= 1980].copy()

    def analyze_subdataframe(self, sub_df: pd.DataFrame) -> Dict[str, Any]:
        shortest_movie = sub_df.loc[sub_df['Runtime'].idxmin()]
        least_profitable = sub_df.loc[sub_df['Gross'].idxmin()]
        avg_duration = sub_df['Runtime'].mean()

        return {
            'shortest_movie': shortest_movie,
            'least_profitable': least_profitable,
            'average_duration': avg_duration
        }

    def get_rating_std_deviation(self, sub_df: pd.DataFrame) -> float:
        return sub_df['Rating'].std()

    def get_average_votes_by_genre(self) -> pd.Series:
        genre_votes = []
        for _, row in self.df.iterrows():
            genres = [g.strip() for g in row['Genre'].split(',')]
            for genre in genres:
                genre_votes.append({'Genre': genre, 'Votes': row['Votes']})

        genre_df = pd.DataFrame(genre_votes)
        return genre_df.groupby('Genre')['Votes'].mean().sort_values(ascending=False)

    def get_directors_count(self) -> pd.Series:
        return self.df['Director'].value_counts()

    def get_best_rated_horror_mystery_scifi(self) -> pd.DataFrame:
        target_genres = {'Horror', 'Mystery', 'Sci-Fi'}
        filtered_movies = []

        for _, row in self.df.iterrows():
            movie_genres = {g.strip() for g in row['Genre'].split(',')}
            if target_genres.issubset(movie_genres):
                filtered_movies.append(row)

        if filtered_movies:
            result_df = pd.DataFrame(filtered_movies)
            return result_df.sort_values('Rating', ascending=False)
        else:
            return pd.DataFrame()