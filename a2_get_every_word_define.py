# get_word_define.py
import htmlmin
import requests
from bs4 import BeautifulSoup

# url = 'http://www.oxfordlearnersdictionaries.com/us/definition/american_english/a_1'
proxies = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
cookies = {'oup-cookie': 'true', 'JSESSIONID': '9A3D476A9725353A4CDDD5D5D0E1841B',
           '__qca': 'P0-918953595-1500593442598', 'dictionary': 'english',
           '_ga': 'GA1.2.448180626.1500593443',
           '_gid': 'GA1.2.928219780.1500593443'
           }
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.95 Safari/537.36'}

# read word list
with open('oxford_3000_<a>.txt', 'r') as file:
    oxford_3000 = file.readlines()
print(oxford_3000[:5])
print(len(oxford_3000))

# start from last runtime
try:
    with open('oxford_3000_html.txt', 'r+', encoding='utf-8') as file:
        oxford_3000_html_finished = file.readlines()
    start = len(oxford_3000_html_finished)
except FileNotFoundError:
    start = 0

# for x in range(0, len(oxford_3000[:5])):  # first five lines
for x in range(start, len(oxford_3000)):  # from start to end
    word = oxford_3000[x].split(',')[0]
    url = oxford_3000[x].split(',')[1].replace('\n', '')
    r = requests.get(url=url, proxies=proxies, cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify())
    # print(soup.find(id='entryContent'))
    html = htmlmin.minify(str(soup.find(id='entryContent')).replace('\n', ''),
                          remove_empty_space=False,
                          remove_optional_attribute_quotes=False)
    output = word + u'ㅋ' + html
    with open('oxford_3000_html.txt', 'a+', encoding='utf-8') as file:
        print(output)
        file.writelines(output + '\n')
