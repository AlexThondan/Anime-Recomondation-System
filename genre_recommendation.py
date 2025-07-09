import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the static directory for saving images
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv('dataset/anime-dataset-2023.csv')

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Ensure 'Genres' column exists
if 'Genres' not in df.columns:
    print("Error: 'Genres' column not found in dataset.")
    exit()

# Ask user for genre input
user_genre = input("Enter a genre (e.g., Action, Comedy, Drama): ").strip()

# Filter anime that contain the selected genre
filtered_animes = df[df['Genres'].str.contains(user_genre, case=False, na=False)]

# Handle invalid 'Score' entries (e.g., 'UNKNOWN') and convert valid ones to numeric
filtered_animes.loc[:, 'Score'] = pd.to_numeric(filtered_animes['Score'], errors='coerce')

# Remove rows with NaN scores after conversion (invalid scores like 'UNKNOWN')
filtered_animes = filtered_animes.dropna(subset=['Score'])

# Display anime list (LIMITED TO 25 RECORDS)
if not filtered_animes.empty:
    print(f"\n🎬 Top 25 Animes for Genre: {user_genre}")
    print(filtered_animes[['Name', 'Score', 'Episodes']].sort_values(by='Score', ascending=False).head(25).to_string(index=False))

    # 🎯 Bar Chart - Top 25 Anime by Score
    plt.figure(figsize=(12, 6))
    sns.barplot(
        x=filtered_animes.sort_values(by="Score", ascending=False)['Name'][:25],
        y=filtered_animes.sort_values(by="Score", ascending=False)['Score'][:25],
        hue=filtered_animes.sort_values(by="Score", ascending=False)['Name'][:25],  # ✅ Fix: Assign hue
        palette="viridis",
        legend=False  # ✅ Fix: Removes extra legend
    )
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Anime", fontsize=14)
    plt.ylabel("Score", fontsize=14)
    plt.title(f"Top 25 Anime in {user_genre} Genre by Score", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, 'top_anime_bar_chart.png'), dpi=300, bbox_inches='tight')
    plt.show()
    print("Bar chart saved and shown successfully!")

    # 🎯 Pie Chart - Anime Type Distribution
    type_counts = filtered_animes['Type'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(
        type_counts, labels=type_counts.index, autopct='%1.1f%%',
        colors=sns.color_palette("pastel"), wedgeprops={'edgecolor': 'black'}
    )
    plt.title(f"Distribution of Anime Types in {user_genre} Genre", fontsize=16, fontweight='bold')
    plt.savefig(os.path.join(STATIC_DIR, 'anime_type_pie_chart.png'), dpi=300, bbox_inches='tight')
    plt.show()
    print("Pie chart saved and shown successfully!")

else:
    print("\n⚠ No anime found for this genre. Try another genre.")
