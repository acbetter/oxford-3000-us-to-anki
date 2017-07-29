# a1_get_3000_words_list.py
import requests
from bs4 import BeautifulSoup

'''Ready to Get'''
url_us = 'http://www.oxfordlearnersdictionaries.com/us/wordlist/american_english/oxford3000/Oxford3000_A-B/'
url_uk = 'http://www.oxfordlearnersdictionaries.com/uk/wordlist/american_english/oxford3000/Oxford3000_A-B/'
proxies = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
cookies = {'oup-cookie': 'true',
           'JSESSIONID': '9A3D476A9725353A4CDDD5D5D0E1841B',
           '__qca': 'P0-918953595-1500593442598',
           'dictionary': 'english',
           '_ga': 'GA1.2.448180626.1500593443',
           '_gid': 'GA1.2.928219780.1500593443'
           }
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.95 Safari/537.36'}

'''Let's Start'''
url = url_us  # You can choose to use US or UK define and pronounce
r = requests.get(url=url, proxies=proxies, cookies=cookies, headers=headers)
soup = BeautifulSoup(r.text, "html5lib")
print(soup.prettify())

'''Get url_list'''
url_list = [url]
for tag in soup.find(id="entries-selector").find_all('a'):
    print(tag['href'])
    url_list.extend([tag['href']])
# url_list = ['http://xxxxx/oxford3000/Oxford3000_A-B/',
#             'http://xxxxx/oxford3000/Oxford3000_C-D/',
#             'http://xxxxx/oxford3000/Oxford3000_E-G/',
#             'http://xxxxx/oxford3000/Oxford3000_H-K/',
#             'http://xxxxx/oxford3000/Oxford3000_L-N/',
#             'http://xxxxx/oxford3000/Oxford3000_O-P/',
#             'http://xxxxx/oxford3000/Oxford3000_Q-R/',
#             'http://xxxxx/oxford3000/Oxford3000_S/',
#             'http://xxxxx/oxford3000/Oxford3000_T/',
#             'http://xxxxx/oxford3000/Oxford3000_U-Z/']

'''Get 3000 Words'''
oxford_3000 = {}
for i in url_list:
    url = i
    print(url)  # url = 'http://xxxxx/oxford3000/Oxford3000_A-B/'
    r = requests.get(url=url, proxies=proxies, cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    '''Get first page words for A-B or C-D'''
    for k in soup.find(id="entrylist1").find_all('a'):
        oxford_3000[k.text] = k['href']
    '''Get other pages words like: Oxford3000_A-B/?page=2'''
    for j in soup.find(id="paging").find_all('a'):
        url = j['href']
        print(url)  # url = 'http://xxxxxx/oxford3000/Oxford3000_A-B/?page=2'
        r = requests.get(url=url, proxies=proxies, cookies=cookies, headers=headers)
        soup = BeautifulSoup(r.text, "html5lib")
        for k in soup.find(id="entrylist1").find_all('a'):
            oxford_3000[k.text] = k['href']

'''Print Words'''
print(oxford_3000)
print(len(oxford_3000))

'''Save To File'''
with open('oxford_3000_<a>.txt', 'w+') as file:
    for key, value in oxford_3000.items():
        file.write(','.join([key, value]))
        file.write('\n')
