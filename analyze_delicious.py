from bs4 import BeautifulSoup
import json
import copy
from urllib.parse import urlparse
import argparse

stat = {"dates": {}, "privates": 0, "publics": 0, "tags": {}}

class Url:
    def __init__(self, url):
        self.url = url
    
    def get_domain(self) -> str:
        return urlparse(self.url).netloc

class LinkInfo:
    def __init__(self, info):
        self.info = info
        self.url = Url(self.info['href'])
    
    def __str__(self) -> str:
        if not self.is_private:
            return f"LinkInfo: {self.url.get_domain()}"
        else:
            return "LinkInfo is private."

    @property
    def is_private(self):
        return bool(int(self.info['private']))

    def get_tags(self):
        return self.info['tags'].split(",")


def get_links(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        for link in soup.find_all('a'):
            yield LinkInfo(link.attrs)

def process_stats(link_attrs, statistic):
    if link_attrs['href'] in statistic.keys():
        statistic[link_attrs['href']] += 1
    else:
        statistic[link_attrs['href']] = 1
    
    if link_attrs["add_date"] not in statistic["dates"].keys():
        statistic["dates"][link_attrs['add_date']] = 1
    else:
        statistic["dates"][link_attrs['add_date']] += 1

    if link_attrs['private']:
        statistic["privates"] += 1
    else:
        statistic["publics"] += 1
    
    tags = link_attrs["tags"].split(",")
    for tag in tags:
        if tag in statistic['tags'].keys():
            statistic["tags"][tag] += 1
        else:
            statistic['tags'][tag] = 1
    
    # yield link_attrs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze your Delicious bookmarks.")
    parser.add_argument("-f", action="store", dest="filename", help="Path to file with bookmarks.")

    results = parser.parse_args()
    
    # with open("output.json", "w") as fp:
    #     fp.write(json.dumps([l for l in get_links(f)]))
    
    st = copy.deepcopy(stat)
    
    for l in get_links(results.filename):
        # process_stats(l, st)
        print(l)
    
    # print(st)
    # print(st['tags'])