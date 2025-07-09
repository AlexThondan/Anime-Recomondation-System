from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def index():
    # Load dataset
    df = pd.read_csv('dataset/anime-dataset-2023.csv')

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Ensure 'Genres' column exists
    if 'Genres' in df.columns:
        # Genre Distribution
        all_genres = df['Genres'].dropna().str.split(', ')
        genre_counts = pd.Series([genre for sublist in all_genres for genre in sublist]).value_counts()
        top_genres_pie = genre_counts.head(5)
        top_genres_bar = genre_counts.head(10)

        # 🥧 Save Pie Chart (Top 5 Anime Genres)
        plt.figure(figsize=(10, 10))
        plt.pie(top_genres_pie, labels=top_genres_pie.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"), wedgeprops={'edgecolor': 'black'})
        plt.title('Top 5 Anime Genres', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('static/top_genres_pie_chart.png')
        plt.close()

        # 📊 Save Bar Chart (Top 10 Anime Genres)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_genres_bar.index, y=top_genres_bar.values, hue=top_genres_bar.index, palette="viridis", legend=False)
        plt.title('Top 10 Anime Genres', fontsize=16, fontweight='bold')
        plt.xlabel('Genres', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('static/top_genres_bar_chart.png')
        plt.close()

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
