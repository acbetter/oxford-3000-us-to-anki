# a4_get_font_of_interface_css.py
import os
import re
import shutil

import requests

proxies = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.95 Safari/537.36'}


def get_font(download: bool):
    """Step 1: Get resource list and Covert href-links to Anki's style"""
    with open('a/interface.css', 'r', encoding='utf-8') as file:
        interface = file.read()
    url = re.findall(r'@import url\((.*?)\);', interface)[0]
    r = requests.get(url=url, proxies=proxies, headers=headers)
    files = re.findall(r'url\("?(.*?)"?\)', r.text)

    prefix = '_us-oxford-learners-dict-fonts-'  # Use char '_' and Fucking Anki!
    """ https://apps.ankiweb.net/docs/manual.html#media-&-latex-references
    Anki Docs: The underscore tells Anki that the file is used by the template and it should be exported when sharing the deck.
    """

    def repl(match_obj):  # You can use lambda here.
        print(match_obj)
        return 'url("' + prefix + match_obj[1].replace('https://fonts.gstatic.com/s/', '') \
            .replace('/', '-').replace('_', '-') + '")'

    font = re.sub(r'url\("?(.*?)"?\)', repl, r.text)
    if not os.path.exists('collection.media'):
        os.mkdir('collection.media')

    '''Step 2: Downloads all fonts '''
    for i in files:
        url = i
        name = prefix + i.replace('https://fonts.gstatic.com/s/', '') \
            .replace('/', '-').replace('_', '-')
        print(name + '\t' + url)
        if download:  # downloading...
            r = requests.get(url=url, proxies=proxies, headers=headers, stream=True)
            if r.status_code == 200:
                with open('collection.media/' + name, 'wb') as file:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, file)

    '''Step 3: Save new css-style file to "a/which_css.css" '''
    interface = font + '.icon-tick:before {' + interface.split('.icon-tick:before {')[1]
    with open('a/interface.css', 'w+', encoding='utf-8') as file:
        file.write(interface)


if __name__ == '__main__':
    # get_font(download=False)
    get_font(download=True)
