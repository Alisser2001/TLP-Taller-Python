from analysis import MovieAnalyzer
import pandas as pd

def main():
    analyzer = MovieAnalyzer('horror_movies_imdb.csv')
    print("=" * 60)
    print("HORROR MOVIES DATASET ANALYSIS")
    print("=" * 60)
    print("\n1. Dataset imported successfully")
    dataset = analyzer.import_dataset()
    print(f"Dataset shape: {dataset.shape}")
    print("\n2. First 5 movies:")
    print("-" * 40)
    first_five = analyzer.print_first_five()
    print(first_five[['Movie Title', 'Movie Year', 'Rating', 'Director']])
    print("\n3. Dataset length:")
    print("-" * 40)
    length = analyzer.get_dataset_length()
    print(f"Total movies: {length}")
    print("\n4. Dataset headers:")
    print("-" * 40)
    headers = analyzer.get_headers()
    for i, header in enumerate(headers, 1):
        print(f"{i}. {header}")
    print("\n5. Movies from 1980 onwards:")
    print("-" * 40)
    sub_df = analyzer.get_movies_from_1980()
    print(f"Movies from 1980+: {len(sub_df)}")
    print(f"Percentage of total: {len(sub_df) / length * 100:.1f}%")
    print("\n6. Sub-dataframe analysis:")
    print("-" * 40)
    analysis = analyzer.analyze_subdataframe(sub_df)
    print(f"Shortest movie: {analysis['shortest_movie']['Movie Title']} ({analysis['shortest_movie']['Runtime']} min)")
    print(
        f"Least profitable: {analysis['least_profitable']['Movie Title']} (${analysis['least_profitable']['Gross']:.2f}M)")
    print(f"Average duration: {analysis['average_duration']:.1f} minutes")
    print("\n7. Rating standard deviation:")
    print("-" * 40)
    std_dev = analyzer.get_rating_std_deviation(sub_df)
    print(f"Standard deviation of ratings: {std_dev:.3f}")
    print("\n8. Average votes by genre (Top 10):")
    print("-" * 40)
    avg_votes = analyzer.get_average_votes_by_genre()
    for genre, votes in avg_votes.head(10).items():
        print(f"{genre}: {votes:,.0f} votes")
    print("\n9. Directors and occurrences (Top 15):")
    print("-" * 40)
    directors = analyzer.get_directors_count()
    for director, count in directors.head(15).items():
        print(f"{director}: {count} movies")
    print("\n10. Best rated Horror + Mystery + Sci-Fi movies:")
    print("-" * 40)
    best_rated = analyzer.get_best_rated_horror_mystery_scifi()
    if not best_rated.empty:
        print(f"Found {len(best_rated)} movies with all three genres:")
        for _, movie in best_rated.head(10).iterrows():
            print(f"{movie['Movie Title']} ({movie['Movie Year']}) - Rating: {movie['Rating']}")
    else:
        print("No movies found with all three genres (Horror, Mystery, Sci-Fi)")
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()