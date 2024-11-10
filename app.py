import pandas as pd 
import streamlit as st
import pickle
import requests


df=pd.read_csv('cleaned_data\movies_data.csv')
movies_list=df['title'].values.tolist()

with open('model/vectors_cosine_similarity.pkl','rb') as file:
    similarity=pickle.load(file)


def fetch_movie_poster(movie_id):
    # st.write(movie_id)
    movie_poster=[]
    id=movie_id
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    # st.write(url)
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MGVlYzRjYTA0YTk5MGI4OWZmZjY1NTJlODNkYTZjNiIsIm5iZiI6MTczMTE4MDA0Ni43OTI3NTgsInN1YiI6IjY3MmZiMGI4M2QxYjE5YmYzZGJjMzc3ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5lgXvLygqnzbPurlwfQFVsZDukWU-C6FdxaA6XV5ic0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        movie_data = response.json()
        # poster_path = movie_data.get('poster_path')
        # Extract the poster_path from the response
        if 'poster_path' in movie_data:
            # Construct the full URL for the poster image
            poster_url = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}"
            # st.write(poster_url)
            
            # movie_poster.append(poster_url)
            return poster_url
        else:
            return None #"Poster not available"
        return movie_poster
    else:
        # poster_url
        return None #"Poster not available"
        # return f"Error fetching data: {response.status_code}"
        


def recommendation(movie):
    recommend_movies=[]
    recommend_poster=[]
    index=df[df['title'].str.strip().str.lower()==movie.strip().lower()].index[0]
    for index,similarity_rate in sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x: x[1])[1:6]:
        recommend_movies.append(df.iloc[index]['title'])
        
        # fetch movie poster using imdb api point
        movie_index=df.iloc[index].movie_id  
        recommend_poster.append(fetch_movie_poster(movie_index))
        print(recommend_poster)
        # st.write(recommend_poster)
        # print(recommend_movies)
    return recommend_movies,recommend_poster
        


st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommendation System")



st.sidebar.header("Search Settings")
st.sidebar.write("Enter a movie title to get recommendations based on its similarity.")
selected_movie = st.selectbox("Select a movie to search for recommendations:", movies_list)


if st.button("Get Recommendations"):
    st.sidebar.write(f"Showing recommendations for **{selected_movie}**...")
    st.write(f"Showing recommendations for **{selected_movie}**...")
    movie,poster=recommendation(selected_movie)
    # st.subheader(movie)  # Display movie name as subheader
    # st.image(poster, caption=movie, use_column_width=True)  # Display poster with movie name as caption
    # for i in movie:
    #     st.write(i)
    # col1,col2,col3,col4,col5=st.columns(5)
    # with col1:
    #     st.header(movie[0])
    #     st.image(poster[0])
    # with col2:
    #     st.header(movie[1])
    #     st.image(poster[1])
    # with col3:
    #     st.header(movie[2])
    #     st.image(poster[2])
    # with col4:
    #     st.header(movie[3])
    #     st.image(poster[3])
    # with col5:
    #     st.header(movie[4])
    #     st.image(poster[4])        
    columns = st.columns(5)
    for i in range(5): # Adjust this based on how many movies you want to display
        with columns[i]:
            # st.write(poster[i])
            st.text(movie[i])
            
            if poster[i]:
                st.image(poster[i])
            else:
                st.text('poster not available')


    
# Footer for additional styling

# st.markdown("---")
# st.markdown("Created with ❤️ using Streamlit.")

st.markdown("---")
st.markdown("""
    <style>
        .footer {
            font-size: 14px;
            color: #555555;
            text-align: center;
            margin-bottom: 3px;
        }
    </style>
    <div class="footer">
        Created with ❤️ using Streamlit.
    </div>
""", unsafe_allow_html=True)



