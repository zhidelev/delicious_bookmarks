from bs4 import BeautifulSoup
import json
import copy

stat = {"dates": {}, "privates": 0, "publics": 0, "tags": {}}

def get_links():
    with open("delicious.html") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        for link in soup.find_all('a'):
            yield link.attrs

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
    # parse path to delicious file
    
    with open("output.json", "w") as f:
        f.write(json.dumps([l for l in get_links()]))
    
    st = copy.deepcopy(stat)
    
    for l in get_links():
        process_stats(l, st)
    
    # print(st)
    print(st['tags'])