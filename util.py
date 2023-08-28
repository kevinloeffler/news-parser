import pickle
import requests
from os import path


def load_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def save_crawled_pages(crawled_pages: list[str], filename):
    with open('crawled-pages/' + filename + '.pkl', 'wb') as output:
        pickle.dump(crawled_pages, output, pickle.HIGHEST_PROTOCOL)


def load_crawled_pages(filename: str) -> list[str]:
    with open('crawled-pages/' + filename + '.pkl', 'rb') as input_file:
        return pickle.load(input_file)


def create_unique_filename(filename: str, suffix: str) -> str:
    if not path.exists(filename + suffix):
        return filename + suffix
    index = 1
    while path.exists(filename + f'_{index}' + suffix):
        index += 1
    return filename + f'_{index}' + suffix
