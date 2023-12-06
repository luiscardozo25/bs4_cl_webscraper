import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
}

source = 'https://newyork.craigslist.org/search/hhh'
query_string = 'housing'.replace(' ', '+')

posts = []

#limited range for learning purposes
for i in range(0, 50, 50):
    params = {
        'query': query_string,
        's': i
    }

#API warning
    response = requests.get(source, params=params, headers=headers)
    if response.status_code != 200:
        print('API call failed')
        break

    soup = BeautifulSoup(response.text, 'html.parser')

# soup.ol was used to figure out the real class name of li as it does not appear in the inspect
    search_results = soup.ol 
    listings = search_results.find_all('li', {'class':'cl-static-search-result'})

    for listing in listings:
        post_url = listing.a['href']
        print(f'Processing post {post_url}...')

        result_info = listing.a
        post_title = result_info.find('div', {'class':'title'}).text
        post_price = result_info.find('div', {'class':'price'}).text        
        post_location = result_info.find('div', {'class':'location'}).text.\
            replace('(','').\
            replace('.)','').strip()
        
        posts.append([post_url, post_title, post_price, post_location])

df = pd.DataFrame(posts, columns=['post url', 'post title', 'post price', 'post location'])
df.to_csv(f'{query_string}.csv', index=False)