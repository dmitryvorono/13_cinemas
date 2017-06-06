import requests
from bs4 import BeautifulSoup


def fetch_afisha_page():
    request = requests.get('https://www.afisha.ru/msk/schedule_cinema/')
    if request.status_code == requests.codes.ok:
        return request.content


def parse_afisha_list(raw_html):
    afisha_html_tree = BeautifulSoup(raw_html, 'html.parser')
    film_elements = afisha_html_tree.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    return [{'title': f.find('h3').text, 'count_cinema': len(f.find_all('tr'))} for f in film_elements]


def fetch_movie_info(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    html = fetch_afisha_page()
    parse_afisha_list(html)
