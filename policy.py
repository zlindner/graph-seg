import requests
import subprocess
from bs4 import BeautifulSoup
from nltk import tokenize


def load(url: str) -> list:
    '''Loads the privacy policy text from the given url'''

    try:
        # load raw html from url
        html = requests.get(url)
    except Exception:
        print('Error loading policy from %s' % url)
        exit()

    # parse sentences from raw html
    sentences = parse(html)

    return sentences


def parse(html) -> list:
    '''Extracts a list of sentences from the raw policy html'''

    soup = BeautifulSoup(html.text, features='html.parser')

    [head.decompose() for head in soup('head')]
    [header.decompose() for header in soup('header')]
    [footer.decompose() for footer in soup('footer')]
    [script.decompose() for script in soup('script')]
    [nav.decompose() for nav in soup('nav')]

    text = ''

    for p in soup.find_all('p'):
        if p.text != '':
            text += p.text.encode('ascii', 'ignore').decode('ascii') + ' '

    # tokenize text into sentences
    sentences = tokenize.sent_tokenize(text)

    return sentences
