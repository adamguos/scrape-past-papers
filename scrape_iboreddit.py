from lxml import html
import requests
import sys
import os

def get_files(url):
    print("Scraping directory: " + url.split('/')[-2])
    page = requests.get(url)
    tree = html.fromstring(page.content)

    links = tree.xpath("//td[contains(@class, 'indexcolname')]/a/@href")

    pdfs = []

    for link in links:
        if ('French' in link or 'Spanish' in link or "German" in link):
            continue
        elif (link.count("/") == 1):
            pdfs += get_files(url + link)
        elif (link.split('.')[-1] == 'pdf'):
            pdfs.append(url + link)
    
    return pdfs

def trim_links(links, base):
    r = []
    for link in links:
        if (link.find(base) != -1):
            r.append(link[(link.find(base) + len(base)):])
        else:
            r.append(link)
    return r

def parse_spaces(links):
    r = []
    for link in links:
        r.append(link.replace("%20", " "))
    return r

def download_files(dllinks, dirname, base):
    for dllink in dllinks:
        dlpath = dirname + "/" + dllink
        print("Downloading: " + dlpath)
        os.makedirs(os.path.dirname(dlpath), exist_ok=True)
        r = requests.get(base + dllink)
        with open(dlpath, "wb") as f:
            f.write(r.content)

dllinks = parse_spaces(trim_links(get_files(sys.argv[1]), sys.argv[1]))
dirname = 'pdfs/' + parse_spaces([sys.argv[1].split('/')[-2]])[0]
download_files(dllinks, dirname, sys.argv[1])