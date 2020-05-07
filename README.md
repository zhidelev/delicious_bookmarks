# delicious_bookmarks

![Python application](https://github.com/zhidelev/delicious_bookmarks/workflows/Python%20application/badge.svg?branch=master)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=zhidelev_delicious_bookmarks&metric=alert_status)](https://sonarcloud.io/dashboard?id=zhidelev_delicious_bookmarks)

# About

**analyze_delicious.py** is a small script to get a nicer HTML document for default Delicious bookmarks export.

To use this script you need Python 3.8 to be installed in your system.

# Basic usage:

    python analyze_delicious.py -f file_name

there file_name is a path to the exported bookmarks document.

The result will be saved to report.html file. It's possible to specify another path with -o parameter. For example:

    python analyze_delicious.py -f file_name -o other_name.html

By default, script does not parse private links. To parse them you should use --private key.

    python analyze_delicious.py -f file_name --private
