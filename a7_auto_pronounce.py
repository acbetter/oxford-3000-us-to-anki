import re

with open('z_oxford.txt', 'r', encoding='utf-8') as file:
    files = file.readlines()
with open('z_oxford_auto_pronounce.txt', 'w+', encoding='utf-8') as file:
    for line in files:
        file.write(line[:-1])
        try:
            sound = re.findall(r'ㅋ\[(.*?)]', line)[0]
            file.write('ㅋ[' + sound + ']\n')
            print(sound)
        except IndexError:
            file.write('ㅋ\n')
            print('sound:none')
