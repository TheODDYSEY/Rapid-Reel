import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import datetime 


def scrape_data():
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
    col2.write(f'Top rated movie: {df.loc[df['Rating'].idxmax()]["Title"]}')
    col2.write(f'Lowest rated movie: {df.loc[df['Rating'].idxmin()]["Title"]}')
    st.subheader('Rating Distribution')
    st.bar_chart(df['Rating'].value_counts())

    st.subheader('Genre Distribution')
    genre_counts = df['Genre'].value_counts()
    st.bar_chart(genre_counts)
    