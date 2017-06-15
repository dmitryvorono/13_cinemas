# Cinemas

This project generate rating films showing in Moscow. List cinemas get in afish.ru, rating - kinopoisk.ru

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt # alternatively try pip3
```
Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

Also, you can add some fresh proxies in proxies.txt

# Usage

usage: cinemas.py [-h] [-c CINEMA]

optional arguments:

  -h, --help            show this help message and exit

  -c CINEMA, --cinema CINEMA
                        If input in rating will not include films with
                        count_cinema less than input value

# Example

I want to find films whose showing more then 100 cinemas:

```bash
$ python cinemas.py -c 100
```

Output rating:

```bash
Чудо-женщина 7.044
Пираты Карибского моря: Мертвецы не рассказывают сказки 6.681
Мумия 5.870
Тачки-3 None
Весь этот мир None
Очень плохие девчонки None
```

Some films do not have a rating, because they just started. Such films have rating None.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)


