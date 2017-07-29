# a6_get_audio_ogg.py
import os
import shutil

import requests
from bs4 import BeautifulSoup

from a3_get_images_in_css_file import copy_collection_media_to

proxies = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
cookies = {'oup-cookie': 'true', 'JSESSIONID': '9A3D476A9725353A4CDDD5D5D0E1841B',
           '__qca': 'P0-918953595-1500593442598', 'dictionary': 'english',
           '_ga': 'GA1.2.448180626.1500593443',
           '_gid': 'GA1.2.928219780.1500593443'
           }
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.95 Safari/537.36'}


def get_audio(file_name: str):
    print('Getting Audio:')
    with open(file_name, 'r', encoding='utf-8') as file:
        oxford_3000_html = file.readlines()

    prefix = 'us-oxford-learners-dict-audio-'  # Don't use char '_' and Fucking Anki!

    os.remove('z_oxford.txt')

    for i in oxford_3000_html:
        soup = BeautifulSoup(i.split('ㅋ')[1].replace('\n', ''), "html5lib")
        sound = soup.find_all('div', class_='audio_play_button')
        count = 0
        srcs = []
        for j in sound:
            '''A Card may have more than one Audio'''
            # print(j)
            # mp3 = j.get('data-src-mp3')
            ogg = j.get('data-src-ogg')
            id_ = 'audio' + str(count)
            src = prefix + ogg.split('/')[-1:][0].replace('/', '-').replace('_', '-')
            srcs.extend([src])
            onclick = "document.getElementById('" + id_ + "').play()"

            '''Add <button> Tag'''
            a = soup.new_tag('a', onclick=onclick, style=j.get('style'),
                             title=j.get('title'), valign=j.get('valign'))
            a['class'] = j.get('class')
            j.insert_after(a)

            '''Add <audio> Tag'''
            j.name = 'audio'
            del j['class']
            del j['style']
            del j['title']
            del j['valign']
            del j['data-src-mp3']
            del j['data-src-ogg']
            j['id'] = id_
            j['src'] = src

            '''Writing Download List to TXT File'''
            # print(','.join([src, mp3, ogg]))
            print(','.join([src, ogg]))
            with open('oxford_3000_<audio>.txt', 'a+') as file:
                file.write(','.join([src, ogg]))
                file.write('\n')

            count += 1

        '''Fix some bugs on html and Fucking Anki's "JS" "Support" '''
        headings = soup.select('span[class="heading"]')
        for heading in headings:
            heading['onclick'] = "this.parentElement.classList.toggle('is-active');"

        '''Writing Anki Cards which were changed for Card's Audio'''
        # print(soup)
        with open('z_oxford.txt', 'a+', encoding='utf-8') as file:
            file.write('ㅋ'.join([str(soup.select('div[class="top-container"]')[0]), str(soup.select('body')[0])]))
            file.write('ㅋ')
            for k in srcs:
                file.write('[sound:' + k + ']')
            file.write('\n')


def download_all_audio():
    with open('oxford_3000_<audio>.txt', 'r') as file:
        files = file.readlines()
    for i in files:
        url = i.split(',')[1].replace('\n', '')
        name = i.split(',')[0]
        print(name + '\t' + url)
        r = requests.get(url=url, proxies=proxies, cookies=cookies, headers=headers, stream=True)
        if r.status_code == 200:
            with open('collection.media/' + name, 'wb') as file:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, file)


if __name__ == '__main__':
    get_audio('oxford_3000_html.txt')
    download_all_audio()
    # copy_collection_media_to('a')
    copy_collection_media_to('/Users/acbetter/Library/Application Support/Anki2/User 1/collection.media')
