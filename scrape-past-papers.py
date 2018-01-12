from lxml import html
import requests
import shutil
import os

def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return local_filename

cat = 7
params = {
    'eng':  ['99', ['']],
    'his':  ['89', ['1 Peacemak', '2', '3 Asia']],
    'phy':  ['93', ['']],
    'mat':  ['91', ['']],
    'che':  ['79', ['']]
}

for param in params:
    for paper in params[param][1]:
        url = 'http://exam-mate.com/pastpapers?cat=7&subject=' + params[param][0] + '&paper=' + paper
        page = requests.get(url)
        tree = html.fromstring(page.content)

        dllinks = tree.xpath("//a[contains(concat(' ', @class, ' '), ' download-btn ')]/@href")
        print('Downloading ' + str(len(dllinks)) + ' files')

        for link in dllinks:
            if os.path.exists(link.split('/')[-1]):
                print('File ' + link.split('/')[-1] + ' already exists, moving on to next file')
            else:
                print('Download of ' + download_file(link) + ' complete')

        print(str(len(dllinks)) + ' files downloaded')