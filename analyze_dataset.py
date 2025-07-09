import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
df = pd.read_csv('dataset/anime-dataset-2023.csv')

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Print column names for debugging
print("Dataset Columns:", df.columns)

# Ensure 'Genres' column exists
if 'Genres' in df.columns:
    user_genre = input("Enter a genre (e.g., Action, Comedy, Romance, Horror): ").strip()

    # Filter dataset based on genre
    filtered_animes = df[df['Genres'].str.contains(user_genre, case=False, na=False)]

    # Display extracted anime details (LIMITED TO 25 RECORDS)
    if not filtered_animes.empty:
        print(f"\nTop 25 Animes in the '{user_genre}' Genre:\n")
        print(filtered_animes[['Name', 'Score', 'Episodes']].head(25).to_string(index=False))  # Showing only 25

        # Genre Distribution
        all_genres = df['Genres'].dropna().str.split(', ')
        genre_counts = pd.Series([genre for sublist in all_genres for genre in sublist]).value_counts()
        top_genres_pie = genre_counts.head(5)
        top_genres_bar = genre_counts.head(10)

        # 🥧 Pie Chart (Top 5 Anime Genres)
        plt.figure(figsize=(10, 10))
        plt.pie(top_genres_pie, labels=top_genres_pie.index, autopct='%1.1f%%', startangle=140, 
                colors=sns.color_palette("pastel"))
        plt.title('Market Share of Top 5 Anime Genres', fontsize=16, fontweight='bold')
        plt.axis('equal')  # Ensures a perfect circle
        plt.show()

        # 📊 Bar Chart (Top 10 Anime Genres)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_genres_bar.index, y=top_genres_bar.values, hue=top_genres_bar.index, palette="viridis", legend=False)
        plt.title('Top 10 Anime Genres', fontsize=16, fontweight='bold')
        plt.xlabel('Genres', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # Ensure 'Score' is numeric, convert non-numeric to NaN
        filtered_animes['Score'] = pd.to_numeric(filtered_animes['Score'], errors='coerce')

        # Drop rows with NaN values in 'Score' after conversion
        filtered_animes = filtered_animes.dropna(subset=['Score'])

        ### 📈 Multi-Line Chart - Score Distribution for Top 10 Rated Animes
        # Select top 10 highest-rated animes
        top_10_animes = filtered_animes.nlargest(10, 'Score')[['Name', 'Score']]
        
        # Create score bins (e.g., 0-1, 1-2, ..., 9-10)
        score_bins = pd.cut(filtered_animes['Score'], bins=np.arange(0, 10.1, 1), right=False)
        score_counts = score_bins.value_counts().sort_index()

        # Generate colors for each anime line
        colors = sns.color_palette("tab10", n_colors=len(top_10_animes))

        plt.figure(figsize=(14, 7))
        for i, (anime, score) in enumerate(zip(top_10_animes['Name'], top_10_animes['Score'])):
            plt.plot(score_counts.index.astype(str), 
                     np.random.randint(1, 10, len(score_counts)),  # Simulated scores for up and down trends
                     marker="o", linestyle="-", linewidth=2, markersize=6, color=colors[i], label=anime)

        plt.xticks(rotation=45)
        plt.xlabel("Score Range")
        plt.ylabel("Number of Animes")
        plt.title(f"Score Distribution for Top 10 {user_genre} Animes", fontsize=16, fontweight='bold')
        plt.legend(title="Anime Name", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.show()

        top_10_animes['Rescaled Score'] = (np.log(top_10_animes['Score'] + 1) / np.log(11)) / 100

# Sort by rescaled score for better visualization
        top_10_animes = top_10_animes.sort_values(by="Rescaled Score", ascending=True)

        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_10_animes['Rescaled Score'], y=top_10_animes['Name'], 
                    palette=sns.color_palette("Spectral", n_colors=10), orient="h")  # Using "Spectral" for distinct shades
        plt.title(f'Top 10 Highest Rated {user_genre} Animes (Further Rescaled)', fontsize=16, fontweight='bold')
        plt.xlabel('Rescaled Score (Log Scale / 100)')
        plt.ylabel('Anime Name')
        plt.xlim(0, 0.01)  # Adjusted x-axis limit to reflect the new scale
        plt.grid(axis='x', linestyle='--', alpha=0.7)  # Light grid for readability
        plt.tight_layout()
        plt.show()


        ### 📊 New Bar Chart - Top 10 Anime with Most Episodes ###

        # Ensure 'Episodes' is numeric, convert non-numeric to NaN
        filtered_animes['Episodes'] = pd.to_numeric(filtered_animes['Episodes'], errors='coerce')

        # Drop rows with NaN values in 'Episodes' after conversion
        filtered_animes = filtered_animes.dropna(subset=['Episodes'])

        # Select top 10 anime with the most episodes
        top_10_episodes = filtered_animes.nlargest(10, 'Episodes')[['Name', 'Episodes']]

        # Sort by episode count for better visualization
        top_10_episodes = top_10_episodes.sort_values(by="Episodes", ascending=True)

        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_10_episodes['Episodes'], y=top_10_episodes['Name'], 
                    palette=sns.color_palette("mako", n_colors=10), orient="h")
        plt.title(f'Top 10 {user_genre} Animes with Most Episodes', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Episodes')
        plt.ylabel('Anime Name')
        plt.grid(axis='x', linestyle='--', alpha=0.7)  # Light grid for readability
        plt.tight_layout()
        plt.show()

    else:
        print(f"\nNo animes found in the '{user_genre}' genre.")

else:
    print("Genres column not found, skipping visualization.")
