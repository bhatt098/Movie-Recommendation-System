import pandas as pd 
import streamlit as st
import pickle

df=pd.read_csv('cleaned_data\movies_data.csv')
movies_list=df['title'].values.tolist()

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommendation System")


st.sidebar.header("Search Settings")
st.sidebar.write("Enter a movie title to get recommendations based on its similarity.")
selected_item = st.selectbox("Select a movie to search for recommendations:", movies_list)


if st.button("Get Recommendations"):
    pass
    
    
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit.")



