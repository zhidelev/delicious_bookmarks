# # -*- coding: utf-8 -*-

# import argparse
# import logging
# import logging.config
# import pathlib
# from collections import defaultdict
# from datetime import datetime
# from urllib.parse import urlparse
# from typing import List
# from dataclasses import dataclass
# import csv

# # from bs4 import BeautifulSoup
# # from jinja2 import Environment, FileSystemLoader

# logging.config.fileConfig("logging.conf")
# logger = logging.getLogger("root")
# # env = Environment(loader=FileSystemLoader("templates"), autoescape=True)


# @dataclass
# class Url:
#     """Wrapper for URL"""

#     addr: str

#     def get_domain(self) -> str:
#         """Returns a domain for the URL

#         :returns: a string with domain
#         :rtype: str

#         """

#         return urlparse(self.addr).netloc

#     def __str__(self):
#         return self.addr


# @dataclass
# class LinkInfo:
#     """Represents information for a link extracted from export file"""

#     info: dict

#     @property
#     def is_private(self) -> bool:
#         """Checks if link in LinkInfo is marked as private.

#         :returns: True if private or False overwise
#         :rtype: bool

#         """

#         return True if self.info["private"] == "1" else False

#     @property
#     def href(self) -> str:
#         """Returns 'href' attribute

#         :returns: link from href
#         :rtype: str

#         """

#         return self.info["href"]

#     @property
#     def text(self) -> str:
#         """Returns text description for a link

#         Returns text in 'text' attribute if set. If 'text' is empty of None returns a domain.

#         :returns: Text description or domain
#         :rtype: str

#         """

#         if self.info["text"] in ["", "None"]:
#             return Url(self.info["href"]).get_domain()
#         return self.info["text"]

#     @property
#     def date(self) -> str:
#         """Returns link adding date in human-readable view

#         :returns: string with date
#         :rtype: str

#         """

#         if len(self.info["add_date"]) == 4:
#             return self.info["add_date"]
#         t_date = datetime.fromtimestamp(int(self.info["add_date"]))
#         return "{:%Y-%m-%d}".format(t_date)

#     @property
#     def timestamp(self) -> int:
#         """Returns timestamp of adding date

#         :returns: date timestamp or 0 if date is invalid
#         :rtype: int

#         """

#         if len(self.info["add_date"]) == 4:
#             return 0
#         else:
#             return int(self.info["add_date"])

#     def __str__(self) -> str:
#         if not self.is_private:
#             return f"LinkInfo: {Url(self.info['href']).get_domain()}"
#         else:
#             return "LinkInfo is private."

#     def get_tags(self) -> List[str]:
#         """Gets a list of tags from 'tags' attribute

#         :returns: list with tags or empty list
#         :rtype: list

#         """

#         return self.info["tags"].split(",")

#     def get_domain(self):
#         """Gets a  domain for a 'href' attribute

#         :returns: domain address
#         :rtype: str

#         """

#         return Url(self.info["href"]).get_domain()


# class Stats:
#     def __init__(self):
#         self.privacy = defaultdict(int)
#         self.tags = defaultdict(int)

#     def update_stats(self, link) -> None:
#         if link.is_private:
#             self.privacy["private"] += 1
#         if not link.is_private:
#             self.privacy["public"] += 1

#         for tag in link.get_tags():
#             self.tags[tag] += 1


# def get_links(filename, private=False):
#     with open(filename, encoding="utf-8") as f:
#         soup = BeautifulSoup(f.read(), "html.parser")
#         for link in soup.find_all("a"):
#             temp = LinkInfo({**link.attrs, **{"text": link.text}})
#             if private:
#                 yield temp
#             else:
#                 if not temp.is_private:
#                     yield temp


# def export_to_csv(filename, links):
#     with open(filename, encoding="utf-8", mode="w") as f:
#         writer = csv.writer(f, dialect="unix")
#         writer.writerow(("Timestamp", "Href"))

#         writer.writerows(((link.timestamp, link.href) for link in links))
#         f.flush()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Analyze your Delicious bookmarks.")
#     parser.add_argument("-f", action="store", dest="filename", help="Path to file with bookmarks.")
#     parser.add_argument("-o", action="store", dest="output_file", help="Path to output file", default="report.html")
#     parser.add_argument(
#         "--private", action="store_true", dest="process_private", default=False, help="Process private links"
#     )
#     parser.add_argument("-csv", action="store", dest="csv_file", help="Path to CSV file for export", default=None)
#     results = parser.parse_args()
#     logger.info("Starting with %s" % results)
#     template = env.get_template("template.html")

#     try:
#         input_file = pathlib.Path(results.filename)

#         with open(results.output_file, "wt") as f:
#             f.write(template.render(links=(link for link in get_links(input_file, results.process_private))))

#         if results.csv_file:
#             export_to_csv(results.csv_file, get_links(input_file, results.process_private))

#     except TypeError:
#         logger.exception("No file is provided", exc_info=True)
#     except FileNotFoundError:
#         logger.exception("No such file", exc_info=True)
#     except PermissionError:
#         logger.exception("Permission problem", exc_info=True)
#     finally:
#         exit()

#     # db_filename = "links_storage.db"
#     # schema_filename = "links_schema.sql"

#     # db_is_new = not os.path.exists(db_filename)

#     # with sqlite3.connect(db_filename) as conn:
#     #     if db_is_new:
#     #         with open(schema_filename) as f:
#     #             conn.executescript(f.read())

#     #         cursor = conn.cursor()

#     #         for link in get_links(results.filename, results.process_private):
#     #             cursor.execute(
#     #                 "INSERT INTO links VALUES (?, ?, ?, ?, ?)",
#     #                 (None, str(link.url), int(link.is_private), link.timestamp, 0),
#     #             )
