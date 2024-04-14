# delicious_bookmarks

![Python application](https://github.com/zhidelev/delicious_bookmarks/workflows/Python%20application/badge.svg?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=zhidelev_delicious_bookmarks&metric=alert_status)](https://sonarcloud.io/dashboard?id=zhidelev_delicious_bookmarks)

## About

In the beginning `delicious bookmarks` was a python script for exporting data from `del.icio.us` website but now it's a web-service for keeping your bookmarks.

### Running web-service

    docker compose run -d

### Stipping web-service

    docker compose down

## Development

For development please install all dependencies with poetry and run FastAPI service

    poetry install --with test,dev
    cd backend/src
    uvicorn app.main:app --reload

## Performance testing

To run `locust` tests

    cd backend/src/tests
    locust

this will run basic performance test `locustfile.py` with configuration `locust.conf`

**analyze_delicious.py** is a small script to get a nicer HTML document for default Delicious bookmarks export.

To use this script you need Python 3.8 to be installed in your system.

## Basic usage

    python analyze_delicious.py -f file_name

there file_name is a path to the exported bookmarks document.

The result will be saved to report.html file. It's possible to specify another path with -o parameter. For example:

    python analyze_delicious.py -f file_name -o other_name.html

By default, script does not parse private links. To parse them you should use --private key.

    python analyze_delicious.py -f file_name --private

It's possible to export data to CSV file

    python analyze_delicious.py -f file_name -csv out.csv
