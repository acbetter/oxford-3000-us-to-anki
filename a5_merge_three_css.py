# a5_merge_three_css.py
with open('a/interface.css', 'r', encoding='utf-8') as file:
    interface = file.read()

with open('a/oxford.css', 'r', encoding='utf-8') as file:
    oxford = file.read()

with open('card.css', 'r', encoding='utf-8') as file:
    card = file.read()

with open('z_oxford.css', 'w+', encoding='utf-8') as file:
    file.write(card)
    file.write(interface)
    file.write(oxford)
