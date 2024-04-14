from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
movies_df = pd.read_csv('movies.csv')
movies_df['Movie Name'] = movies_df['Movie Name'].str.lower()
movies_df['Genre'] = movies_df['Genre'].apply(lambda x: x.split(', ') if pd.notnull(x) else [])

@app.route('/', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_genre = request.form['genre']
        user_rating = float(request.form['rating'])
        recommendations = recommend_movies_by_genre_and_rating(user_genre, user_rating)
        return render_template('index.html', recommendations=recommendations)
    return render_template('index.html', recommendations=None)

def recommend_movies_by_genre_and_rating(genre, min_rating):
    genre_filtered = movies_df[movies_df['Genre'].apply(lambda x: genre.lower() in [g.lower() for g in x])]
    rating_filtered = genre_filtered[genre_filtered['Rating'] >= min_rating]
    if rating_filtered.empty:
        return "No movie found matching the criteria."
    else:
        return rating_filtered[['Movie Name', 'Rating']].sort_values(by='Rating', ascending=False).head(10).to_html(classes='table')

if __name__ == '__main__':
    app.run(debug=True)
