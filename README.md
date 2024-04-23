# Web Scraping YTS Movie Data

## Overview

This Python script is designed to scrape movie data from the YTS.mx website and store it in a Pandas DataFrame. It utilizes the Requests library to send HTTP requests to the website and BeautifulSoup for parsing HTML content.

## Prerequisites

Before running the script, ensure you have the following dependencies installed:
- Python 3.x
- Requests library (`pip install requests`)
- BeautifulSoup library (`pip install beautifulsoup4`)
- Pandas library (`pip install pandas`)

## Usage

1. Clone the repository or download the Python script (`code.ipynb`).
2. Navigate to the directory containing the script in your terminal or command prompt.
3. Run the script using Python:

```bash
python code.ipynb
```

4. After execution, the script will create two files:
   - `yts.txt`: Contains the raw HTML content of the webpage for reference.
   - `output.xlsx`: Contains the scraped movie data in an Excel file format.

## Workflow

1. **Send a GET request**: The script sends a GET request to the YTS website using the Requests library to retrieve the HTML content of the specified URL.

2. **Parse HTML content**: BeautifulSoup is used to parse the HTML content obtained from the response.

3. **Save HTML content**: The parsed HTML content is saved to a text file named `yts.txt` for reference.

4. **Extract movie data**: The script extracts movie data such as title, genre, rating, and year from the parsed HTML content using BeautifulSoup.

5. **Create DataFrame**: The extracted movie data is stored in a list and then converted into a Pandas DataFrame.

6. **Export to Excel**: The DataFrame is exported to an Excel file named `output.xlsx` without including the index column.

## Contributing

Feel free to contribute to this project by submitting bug fixes, feature enhancements, or suggestions via GitHub issues and pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
