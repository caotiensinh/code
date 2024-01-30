import requests
from bs4 import BeautifulSoup

def search_song(query):
    # Tạo URL tìm kiếm trên Genius
    search_url = f"https://genius.com/api/search/multi?q={query}"

    # Gửi yêu cầu HTTP và nhận dữ liệu HTML
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lấy các kết quả từ HTML
    results = soup.find_all('div', class_='mini_card')
    
    # Hiển thị kết quả
    for idx, result in enumerate(results, 1):
        title = result.find('h3').get_text(strip=True)
        artist = result.find('span', class_='secondary_info').get_text(strip=True)
        print(f"{idx}. {title} by {artist}")

# Nhập từ hoặc câu hát từ người dùng
search_query = input("Nhập từ hoặc câu hát: ")
search_song(search_query)
