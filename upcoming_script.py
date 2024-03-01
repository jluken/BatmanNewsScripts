import re
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

comics = []

comic_listings = [  # Everything is currently formatted for Amazon listings
        'https://www.amazon.com/Detective-Comics-2016-1082-Ram-ebook/dp/B0CTD812JN/',
        'https://www.amazon.com/Batman-Brave-Bold-2023-10-ebook/dp/B0CTD9MW6H',
        'https://www.amazon.com/Penguin-2023-7-Tom-King-ebook/dp/B0CTDCC916/',
        'https://www.amazon.com/Harley-Quinn-2021-Tini-Howard-ebook/dp/B0CTDBY7JV'
]
#
#     [
#         'Batman #142',
#         'Chip Zdarsky (Author), Jorge Jiménez (Cover Art), Giuseppe Camuncoli (Cover Art, Penciller), Stefano Nesi (Cover Art, Inker), Tomeu Morey (Cover Art), Andrea Sorrentino (Penciller, Inker), Dave Stewart (Colorist), Alejandro Sanchez (Colorist)',
#         'The tragic “death” of the leader of the Red Hood Gang in a vat of chemicals has become the subject of myth…but what is the heartbreaking and gruesome tale of the monster who walked away from that violent birth? And how does it affect Batman’s distant future? “The Joker Year One” begins here!'
#     ],
#     [
#         'Suicide Squad: Kill Arkham Asylum #1',
#         'John Layman (Author), Dan Panosian (Cover Art), Jesús Hervás (Penciller, Inker), David Baron (Colorist)',
#         'Before the Suicide Squad sets their sights on the corrupted Justice League in the upcoming videogame Suicide Squad: Kill the Justice League, join us for this thrilling prequel and witness them kill Arkham Asylum! Amanda Waller has taken control of the recently rebuilt Arkham, and her brutal tactics and merciless methods have led to the most secure asylum Gotham has ever known. But when the cell doors open, and the inmates are left in a freefor-all deathmatch, Waller’s true intentions reveal themselves: identify the strongest, smartest, and most brutal to serve her on Task Force X.'
#     ],
# ]


headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'personal@domain.com'
}

for listing in comic_listings:
    req = requests.get(listing, headers=headers)
    html = BeautifulSoup(req.content, features="html.parser")
    comic = {}
    comic['title'] = html.find('span', id='productTitle').contents[0].strip()
    if html.find_all('div', id='drengr_DesktopTabbedDescriptionOverviewContent_feature_div'):
        comic['description'] = html.find('div', id='drengr_DesktopTabbedDescriptionOverviewContent_feature_div').contents[1].contents[0]
    elif html.find_all('div', id='bookDescription_feature_div'):  # Sometimes Amazon changes the format randomlu
        comic['description'] = html.find('div', id='bookDescription_feature_div').contents[1].contents[1].contents[1].contents[0]
    else:
        raise Exception('Just try running it again')

    creators = html.find_all('span', 'author')
    comic['writer'] = ', '.join([creator.find('a', 'a-link-normal').contents[0] for creator in creators
                                 if 'Author' in creator.find('span', 'a-color-secondary').contents[0]])
    comic['cover artist'] = ', '.join([creator.find('a', 'a-link-normal').contents[0] for creator in creators
                                       if 'Cover Art' in creator.find('span', 'a-color-secondary').contents[0]])
    comic['penciller'] = ', '.join([creator.find('a', 'a-link-normal').contents[0] for creator in creators
                                    if 'Penciller' in creator.find('span', 'a-color-secondary').contents[0]])
    comic['colorist'] = ', '.join([creator.find('a', 'a-link-normal').contents[0] for creator in creators
                                   if 'Colorist' in creator.find('span', 'a-color-secondary').contents[0]])
    comic['inker'] = ', '.join([creator.find('a', 'a-link-normal').contents[0] for creator in creators
                                if 'Inker' in creator.find('span', 'a-color-secondary').contents[0]])

    # creators = listing[1].split('), ')
    #
    # comic['writer'] = ', '.join([re.sub(' \(.*','', creator) for creator in creators if 'Author' in creator])
    # comic['cover artist'] = ', '.join([re.sub(' \(.*','', creator) for creator in creators if 'Cover Art' in creator])
    # comic['penciller'] = ', '.join([re.sub(' \(.*','', creator) for creator in creators if 'Penciller' in creator])
    # comic['colorist'] = ', '.join([re.sub(' \(.*', '', creator) for creator in creators if 'Colorist' in creator])
    # comic['inker'] = ', '.join([re.sub(' \(.*','', creator) for creator in creators if 'Inker' in creator])

    comics.append(comic)


with open('upcoming.txt', 'w') as f:
    f.write('[insert intro text]\n')
    f.write('<h3><b>Upcoming Comics</b></h3>\n')
    for comic in comics:
        f.write(f'<b>{comic["title"]}</b>\n')
        f.write('\n<span style="font-weight: 400;">[insert cover]</span>\n\n')
        f.write(f'<i><span style="font-weight: 400;">{comic["description"]}</span></i>\n')
        f.write('<ul>\n')
        f.write(f' \t<li><b>Written By:</b> {comic["writer"]}</li>\n')
        f.write(f' \t<li aria-level="1"><b>Penciled By:</b> {comic["penciller"]}</li>\n')
        f.write(f' \t<li aria-level="1"><b>Inks By:</b> {comic["inker"]}</li>\n')
        f.write(f' \t<li aria-level="1"><b>Colors By:</b> {comic["colorist"]}</li>\n')
        f.write(f' \t<li aria-level="1"><b>Cover By:</b> {comic["cover artist"]}</li>\n')
        f.write('</ul>\n')
        f.write('<b>Thoughts:</b><i><span style="font-weight: 400;"> [Insert Thoughts]</span></i>\n')
        f.write('\n')
        f.write(f'<b>Batman News Critic:</b><span style="font-weight: 400;"> [insert critic]</span>\n')
        if comic != comics[-1]:
            f.write('\n')
            f.write('<hr />\n')
            f.write('\n')
    f.write('<h3><b>Beyond the Bat</b></h3>\n')
    f.write('Welcome to Beyond the Bat, where we take a quick look at the rest of DC’s comics coming out this week.\n')
    f.write('\n')
    f.write('[insert gallery]\n')
    f.write('<h3><b>Graphic Novel Watch</b></h3>\n')
    f.write('Sometimes you need more than floppies. Sometimes you want something that can sit nicely on your shelf that proudly displays your favorite stories. That’s when you turn to graphic novels. Let’s see what bat collections are coming out this week:\n')
    f.write('\n')
    f.write('[insert gallery]\n')
    f.write('\n')
    f.write('<h3><b>Ratings</b></h3>\n')
    f.write('<b>Most Excited:</b><i> [insert best title]</i>- [insert reasoning]\n')
    f.write('\n')
    f.write('<b>Least Excited:</b><i> [insert trash title]</i>- [insert reasoning]\n')
    f.write('\n')
    f.write('<b>Wild Card:</b><i> [insert wild card title]</i>- [insert reasoning]\n')
    f.write('\n')
    f.write('Well that’s it for this week! Let us know in the comments what comics you’re looking forward to.\n')
