# a3_get_images_in_css_file.py
import os
import re
import shutil

import requests

proxies = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
cookies = {'oup-cookie': 'true', 'JSESSIONID': '9A3D476A9725353A4CDDD5D5D0E1841B',
           '__qca': 'P0-918953595-1500593442598', 'dictionary': 'english',
           '_ga': 'GA1.2.448180626.1500593443',
           '_gid': 'GA1.2.928219780.1500593443'
           }
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.95 Safari/537.36'}


def get_css(*args, download: bool):  # which_css.css
    for which_css in args:
        print(which_css)
        """Step 1: Get resource list and Covert href-links to Anki's style"""
        with open(which_css, 'r', encoding='utf-8') as file:
            css = file.read()

        # Use Regex to get Images List
        files = re.findall(r'url\("?../images/(.*?)"?\)', css)
        print(len(files))

        prefix = '_us-oxford-learners-dict-images-'  # Use char '_' and Fucking Anki!
        """ https://apps.ankiweb.net/docs/manual.html#media-&-latex-references
        Anki Docs: The underscore tells Anki that the file is used by the template and it should be exported when sharing the deck.
        """

        def repl(match_obj):  # You can use lambda here.
            print(match_obj)
            return 'url("' + prefix + match_obj[1].replace('/', '-').replace('_', '-') + '")'

        # Replace css file's image link with Anki Style
        css = re.sub(r'url\("?../images/(.*?)"?\)', repl, css)

        if not os.path.exists('collection.media'):
            os.mkdir('collection.media')

        '''Step 2: Downloads all images '''
        for i in files:
            url = 'http://www.oxfordlearnersdictionaries.com/us/external/images/' + i
            name = prefix + i.replace('/', '-').replace('_', '-')
            print(name + '\t' + url)
            if download:  # downloading...
                r = requests.get(url=url, proxies=proxies, cookies=cookies, headers=headers, stream=True)
                if r.status_code == 200:
                    with open('collection.media/' + name, 'wb') as file:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, file)

        '''Step 3: Save new css-style file to "a/which_css.css" '''
        with open('a/' + which_css, 'w+', encoding='utf-8') as file:
            file.write(css)


def copy_collection_media_to(dst: str):
    src = 'collection.media'
    # shutil.copytree(src=src, dst=dst)
    for file in os.listdir(src):
        file_name = os.path.join(src, file)
        if os.path.isfile(file_name):
            shutil.copy2(src=file_name, dst=dst)


if __name__ == '__main__':
    get_css('oxford.css', download=True)
    get_css('interface.css', download=True)
    # get_css('oxford.css', 'interface.css', download=False)  # update css file after you modify the css file
    copy_collection_media_to('a')
