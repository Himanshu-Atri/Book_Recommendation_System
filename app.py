from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('model\popular_books.pkl', 'rb'))
pt = pickle.load(open('model\pt.pkl', 'rb'))
similar_books = pickle.load(open('model\similar_books.pkl', 'rb'))
books = pickle.load(open('model\\books.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                           book_names = list(popular_df['Book-Title'].values),
                           authors = list(popular_df['Book-Author'].values),
                           years = list(popular_df['Year-Of-Publication'].values),
                           rating_counts = list(popular_df['rating_count'].values),
                           average_ratings = list(popular_df['average_rating'].values),
                           img_urls = list(popular_df['Image-URL-M'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods = ['POST'])
def recommend():
    user_input = request.form.get('user_input')
    
    if(len(pt[pt['Book-Title'].str.contains(user_input, case=False, na=False)].index) == 0):
        return render_template('recommend.html')
    ind = pt[pt['Book-Title'].str.contains(user_input, case=False, na=False)].index[0]
    similar_items = similar_books[ind]
    top_4 = sorted(list(enumerate(similar_items)), key = lambda x: x[1], reverse=True)[1:5]
    book_info = []
    for i, j in top_4:
        
        book_name = pt[pt.index == i]['Book-Title'].values[0]
        author = books[books['Book-Title'] == book_name].iloc[0]['Book-Author']
        year = books[books['Book-Title'] == book_name].iloc[0]['Year-Of-Publication']
        img_url = books[books['Book-Title'] == book_name].iloc[0]['Image-URL-M']
        book_info.append([book_name, author, year, img_url])
    
    return render_template('recommend.html', data = book_info)
    
if __name__ == '__main__':
    app.run(debug=True)