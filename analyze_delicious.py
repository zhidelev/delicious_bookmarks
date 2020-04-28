from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse
from jinja2 import FileSystemLoader, Environment
from collections import defaultdict
from datetime import datetime
import os
import sqlite3
from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import CDN


env = Environment(loader=FileSystemLoader("templates"), autoescape=True)


class Url:
    def __init__(self, url):
        self.url = url

    def get_domain(self) -> str:
        return urlparse(self.url).netloc
    
    def __str__(self):
        return self.url


class LinkInfo:
    def __init__(self, info):
        self.info = info
        self.url = Url(self.info["href"])

    @property
    def is_private(self) -> bool:
        if self.info["private"] == "1":
            return True
        else:
            return False

    @property
    def href(self) -> str:
        return self.info["href"]

    @property
    def text(self) -> str:
        if self.info["text"] in ["", "None"]:
            return self.url.get_domain()
        return self.info["text"]
    
    @property
    def date(self) -> str:
        if len(self.info['add_date']) == 4:
            return self.info['add_date']
        t_date = datetime.fromtimestamp(int(self.info['add_date']))
        return "{:%Y-%m-%d}".format(t_date)
    
    @property
    def timestamp(self) -> int:
        if len(self.info['add_date']) == 4:
            return 0
        else:
            return int(self.info['add_date'])

    def __str__(self) -> str:
        if not self.is_private:
            return f"LinkInfo: {self.url.get_domain()}"
        else:
            return "LinkInfo is private."

    def get_tags(self) -> list:
        return self.info["tags"].split(",")

class Stats:
    def __init__(self):
        self.privacy = defaultdict(int)
        self.tags = defaultdict(int)
        self.domains = defaultdict(int)

    def update_stats(self, link) -> None:
        if link.is_private:
            self.privacy['private'] += 1
        if not link.is_private:
            self.privacy['public'] += 1
        
        for tag in link.get_tags():
            self.tags[tag] += 1
        
        self.domains[link.url.get_domain()] += 1



def get_links(filename, private):
    with open(filename) as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for link in soup.find_all("a"):
            temp = LinkInfo({**link.attrs, **{"text": link.text}})
            if not temp.is_private:
                yield temp
            if private:
                if temp.is_private:
                    yield temp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze your Delicious bookmarks.")
    parser.add_argument("-f", action="store", dest="filename", help="Path to file with bookmarks.")
    parser.add_argument("-o", action="store", dest="output_file", help="Path to output file", default="report.html")
    parser.add_argument(
        "--private", action="store_true", dest="process_private", default=False, help="Process private links"
    )

    results = parser.parse_args()

    report = env.get_template("template.html")

    with open(results.output_file, "wt") as f:
        f.write(report.render(links=(l for l in get_links(results.filename, results.process_private))))

    db_filename = "links_storage.db"
    schema_filename = "links_schema.sql"

    db_is_new = not os.path.exists(db_filename)

    with sqlite3.connect(db_filename) as conn:
        if db_is_new:
            with open(schema_filename) as f:
                conn.executescript(f.read())
        
            cursor = conn.cursor()

            for link in get_links(results.filename, results.process_private):
                cursor.execute("INSERT INTO links VALUES (?, ?, ?, ?, ?)", (None, str(link.url), int(link.is_private), link.timestamp, 0))
    
    s = Stats()
    for link in get_links(results.filename, results.process_private):
        s.update_stats(link)
    
    statistics = env.get_template('statistics.html')
    with open('statistics.html', "wt") as f:
        f.write(statistics.render(statistics=s))
