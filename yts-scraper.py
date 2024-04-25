import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime 
# Step 1: Send a GET request to the specified URL
# Define the URL
url = "https://yts.mx/browse-movies/0/all/all/0/featured/0/all"
response = requests.get(url)

# Step 2: Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Save the HTML content to a text file for reference
with open("yts.txt", "w", encoding="utf-8") as file:
    file.write(str(soup))
print("Page content has been saved to yts.txt")

# Step 4: Extract movie data from the parsed HTML and store it in a list
movies_data = []
for movie in soup.find_all('div', class_='browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4'):
    Title = movie.find('a', class_='browse-movie-title').text
    Genre = movie.find_all('h4')[1].text
    Rating = movie.find('h4', class_='rating').text.split(' / ')[0]
    Year = movie.find('div', class_='browse-movie-year').text
    movies_data.append([Title, Genre, Rating, Year])
    
    
# Step 5: Create a Pandas DataFrame from the extracted movie data
df = pd.DataFrame(movies_data, columns=['Title', 'Genre', 'Rating', 'Year'])    

# Display the resulting DataFrame
df

# save to excel file 
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