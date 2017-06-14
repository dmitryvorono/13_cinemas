import requests
from bs4 import BeautifulSoup
import argparse
import pprint
import random
import time
import itertools


fake_headers = [{"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
                    "Connection":"keep-alive",
                    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
                    },

                    {
                    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ru, en-US; q=0.7, en; q=0.3',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
                    },

                    {
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Length': '82',
                        'Content-Type': 'text/plain;charset=UTF-8',
                        'Connection': 'keep-alive'
                    }
            
                    ]

def initialize_proxies_list(filepath):
    with open(filepath, 'r') as proxies_file:
        return proxies_file.read().split()


def fetch_afisha_page():
    request = requests.get('https://www.afisha.ru/msk/schedule_cinema/')
    if request.status_code == requests.codes.ok:
        return request.content


def parse_afisha_list(raw_html):
    afisha_html_tree = BeautifulSoup(raw_html, 'html.parser')
    film_elements = afisha_html_tree.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    return [{'title': f.find('h3').text, 'count_cinema': len(f.find_all('tr'))} for f in film_elements]


def fetch_movie_info(movie_title, cycle_proxy):
    proxies = {'https': next(cycle_proxy)}
    print(proxies)
    session = requests.session()
    session.headers.update(random.choice(fake_headers))
    session.proxies.update(proxies)
    try:
        request = session.get('https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query={0}'.format(movie_title), timeout=30)
    except:
        return None
    if request.status_code == requests.codes.ok:
        return request.text


def get_html_text(html_tree, tag, attrs):
    target_element = html_tree.find(tag, attrs)
    if target_element is not None:
        return target_element.text


def parse_movie_info(raw_html):
    if raw_html is None:
        return {'rating': '0.0', 'count_votes': '0.0'}
    movie_info_tree = BeautifulSoup(raw_html, 'html.parser')
    rating = get_html_text(movie_info_tree, 'span', {'class': 'rating_ball'})
    count_votes = get_html_text(movie_info_tree, 'span', {'class': 'ratingCount'})
    return {'rating': rating, 'count_votes': count_votes}


def filter_movies(movies, count_cinemas):
    return list(filter(lambda f: f['count_cinema'] >= count_cinemas, movies))


def sorted_movies(movies):
    return sorted(movies, key=lambda f: float(f['rating']) if f['rating'] is not None else 0, reverse=True)


def output_movies_to_console(movies, count_cinemas=None):
    output_movies = sorted_movies(movies)
    if count_cinemas:
        output_movies = filter_movies(output_movies, count_cinemas)
    pprint.pprint(output_movies, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script bla-bla-bla')
    parser.add_argument('-c', '--cinema', type=int, help='If input in rating will not include films with count_cinema less than input value')
    args = parser.parse_args()
    html = fetch_afisha_page()
    films = parse_afisha_list(html)
    proxies_list = initialize_proxies_list('proxies.txt')
    cycle_proxy = itertools.cycle(proxies_list)
    if args.cinema:
        films = filter_movies(films, args.cinema)
    for f in films:
        print('Fetch: {0}'.format(f['title']))
        movie_info = fetch_movie_info(f['title'], cycle_proxy)
        f.update(parse_movie_info(movie_info))
    output_movies_to_console(films, args.cinema)
