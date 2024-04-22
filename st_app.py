import streamlit as st
import pandas as pd
import numpy as np
import pickle

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

def recommend(user_input):
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return data

def main():
    st.title('Book Recommender System')

    st.sidebar.header('User Input')
    user_input = st.sidebar.text_input('Enter a book title:')

    if st.sidebar.button('Recommend'):
        if user_input:
            data = recommend(user_input)
            st.write(pd.DataFrame(data, columns=['Book Title', 'Author', 'Image URL']))
        else:
            st.warning('Please enter a book title.')

if __name__ == '__main__':
    main()
