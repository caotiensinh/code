import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def search_song(query):
    # Create the search URL on Genius
    search_url = f"https://zingmp3.vn/tim-kiem/tat-ca?"
    search_url += urlencode({'q': query})

    # Send the HTTP request and get the HTML data
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the search results from the HTML
    results = soup.select('.mini_card')
    
    # Display the search results
    for idx, result in enumerate(results, 1):
        title = result.select_one('h3').get_text(strip=True)
        artist = result.select_one('.secondary_info').get_text(strip=True)
        print(f"{idx}. {title} by {artist}")

# Get the song title or lyrics from the user
search_query = input("Nhập từ hoặc câu hát: ")
search_song(search_query)