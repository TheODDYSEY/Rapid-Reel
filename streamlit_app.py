import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas.io.sql as sqlio
from streamlit_ace import st_ace

# Database connection URL
DATABASE_URL = "postgresql://postgres:postgres@db:5432/movies_db"

# Connect to the database
engine = create_engine(DATABASE_URL)

def save_to_database(df):
    """
    Saves the DataFrame to a PostgreSQL database.
    """
    try:
        df.to_sql('movies', con=engine, if_exists='replace', index=False)
        print("Data saved to database successfully!")
    except Exception as e:
        print(f"Error saving to database: {e}")


def scrape_data():
    """
    Scrapes movie data from YTS website and returns a DataFrame.
    """
    # Define the URL
    url = "https://yts.mx/browse-movies/0/all/all/0/featured/0/all"
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract movie data from the parsed HTML and store it in a list
    movies_data = []
    for movie in soup.find_all('div', class_='browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4'):
        Title = movie.find('a', class_='browse-movie-title').text
        Genre = movie.find_all('h4')[1].text
        Rating = movie.find('h4', class_='rating').text.split(' / ')[0]
        Year = movie.find('div', class_='browse-movie-year').text
        movies_data.append([Title, Genre, Rating, Year])

    # Create a Pandas DataFrame from the extracted movie data
    df = pd.DataFrame(movies_data, columns=['Title', 'Genre', 'Rating', 'Year'])

    # Save to excel file
    df.to_excel('output.xlsx', index=False)

    # Get the current date, time, and day
    now = datetime.datetime.now()
    date_time_day = now.strftime("%Y-%m-%d, %H:%M:%S, %A")

    # Convert the DataFrame to a markdown table
    markdown_table = df.to_markdown()

    # Write the date, time, day, and markdown table to the report.md file
    with open('report.md', 'a') as f:
        f.write(f'\n## Date: {date_time_day}\n')
        f.write('\n## DataFrame\n')
        f.write(markdown_table)

    # Save the scraped data to the database
    save_to_database(df)

    return df


st.title('YTS Movie Scraper')
st.write('Welcome to the YTS Movie Scraper. Click the button below to scrape the latest movies from YTS.')

if st.button('Scrape Data'):
    df = scrape_data()
    st.success('Scraping completed!')

    # Create two columns
    col1, col2 = st.columns(2)

    # Display the scraped data in the first column
    col1.subheader('Movie Data')
    col1.dataframe(df.style.highlight_max())

    # Display the statistics in the second column
    col2.subheader('Statistics')
    col2.write(f'Number of movies scraped: {df.shape[0]}')
    col2.write(f"Top rated movie: {df.loc[df['Rating'].idxmax()]['Title']}")
    col2.write(f"Lowest rated movie: {df.loc[df['Rating'].idxmin()]['Title']}")

    st.subheader('Rating Distribution')
    st.bar_chart(df['Rating'].value_counts())

    st.subheader('Genre Distribution')
    genre_counts = df['Genre'].value_counts()
    st.bar_chart(genre_counts)

# Interactive SQL Terminal Section
st.subheader('Interactive Database Terminal')
query = st_ace(
    placeholder="Write your SQL query here (e.g., SELECT * FROM movies LIMIT 10);",
    language="sql",
    theme="monokai",
    height=200,
)

if st.button('Execute Query'):
    if query.strip():
        try:
            # Execute the query and fetch the result
            result_df = sqlio.read_sql_query(query, engine)
            st.success("Query executed successfully!")
            st.dataframe(result_df)
        except SQLAlchemyError as e:
            st.error(f"Error executing query: {e}")
    else:
        st.warning("Please write a SQL query before executing.")