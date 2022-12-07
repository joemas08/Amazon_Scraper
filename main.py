import requests
from bs4 import BeautifulSoup

HEADER_FOR_GET_REQUEST = (
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0',
        'Accept-Language': 'en-US, en;q=0.5'
    }
)


def get_single_listing():
    data_out_file = open('data_out.txt', 'w')

    plant_book_url = 'https://www.amazon.com/dp/1591866901'
    web_response = requests.get(plant_book_url, headers=HEADER_FOR_GET_REQUEST)
    # print(web_response.text)

    b_soup_format = BeautifulSoup(web_response.content, 'html.parser')
    # print(b_soup_format)
    product_title_string_mod = ''
    try:
        product_title = b_soup_format.find('span', attrs={'id': 'productTitle'})
        # print(type(product_title))
        # print(product_title)
        product_title_string = product_title.string
        # print(type(product_title_string))
        # print(product_title_string)
        product_title_string_mod = product_title_string.strip().replace(',', '')
        # print(product_title_string_mod)
        # print(type(product_title_string_mod))
    except AttributeError:
        product_title_string = 'NA'
        # print('product Title = ', product_title_string)

    data_out_file.write(f'{product_title_string_mod}')

    data_out_file.close()


def get_listings_by_keyword(search_keywords: str):
    base_url = 'https://www.amazon.com/s?k='
    query_terms = search_keywords.replace(' ', '+')
    url_page_param = '&page=1'
    search_url = f'{base_url}{query_terms}{url_page_param}'

    web_response = requests.get(search_url, headers=HEADER_FOR_GET_REQUEST)
    # print(web_response.content)
    soup_format = BeautifulSoup(web_response.content, 'html.parser')
    # print(soup_format)
    search_results = soup_format.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for product_listing in search_results:

        try:
            product_listing_title = product_listing.h2.text
            print(product_listing_title)
        except AttributeError:
            print('No Product Title')

        try:
            product_listing_rating = product_listing.find('i', {'class': 'a-icon'})
            print(product_listing_rating.text)
            num_ratings = product_listing.find('span', {'class': 'a-size-base'})
            print(f'No. of Ratings: {num_ratings.text}')
        except AttributeError:
            print('No Product Ratings')
        try:
            int_price = product_listing.find('span', {'class': 'a-price-whole'})
            dec_price = product_listing.find('span', {'class': 'a-price-fraction'})
            print(f'${int_price.text}{dec_price.text}')
        except AttributeError:
            print('No Product Price Listed')

        try:
            product_url_link = 'https://www.amazon.com' + product_listing.h2.a['href']
            print(product_url_link)
        except AttributeError:
            print('No Product Link')
        print('=' * 110)


if __name__ == '__main__':
    search_term = input("Enter term to search on Amazon : ")
    get_listings_by_keyword(search_term)
