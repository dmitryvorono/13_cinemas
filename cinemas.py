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
    #proxies = {'https': 'http://111.65.243.225:80'}
    #proxies = {'https': '195.140.253.65:80'}

    fake_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
    request = requests.get('https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query={0}'.format(movie_title), headers = fake_headers)
    if request.status_code == requests.codes.ok:
        return request.text


def get_html_text(html_tree, tag, attrs):
    target_element = html_tree.find(tag, attrs)
    if target_element is not None:
        return target_element.text


def parse_movie_info(raw_html):
    movie_info_tree = BeautifulSoup(raw_html, 'html.parser')
    rating = get_html_text(movie_info_tree, 'span', {'class': 'rating_ball'})
    count_votes = get_html_text(movie_info_tree, 'span', {'class': 'ratingCount'})
    return {'rating': rating, 'count_votes': count_votes}
    

def output_movies_to_console(movies):
    sorted_movies = sorted(movies, key = lambda f: float(f['rating']), reverse=True)
    print(sorted_movies)



test_list = [{'title': 'Мумия', 'count_cinema': 302, 'rating': '5.980', 'count_votes': '1564'}, {'title': 'Пираты Карибского моря: Мертвецы не рассказывают сказки', 'count_cinema': 226, 'rating': '6.681', 'count_votes': '37\xa0304'}, {'title': 'Чудо-женщина', 'count_cinema': 302, 'rating': '7.094', 'count_votes': '20\xa0615'}, {'title': 'Нелюбовь', 'count_cinema': 115, 'rating': '7.691', 'count_votes': '4835'}, {'title': 'Спасатели Малибу', 'count_cinema': 145, 'rating': '5.953', 'count_votes': '3752'}]




if __name__ == '__main__':
    '''
    html = fetch_afisha_page()
    films = parse_afisha_list(html)[:5]
    for f in films:
        print('Fetch: {0}'.format(f['title']))
        movie_info = fetch_movie_info(f['title'])
        #qq = open('text.html', 'r')
        f.update(parse_movie_info(movie_info))
    '''
    films = test_list
    output_movies_to_console(films)
