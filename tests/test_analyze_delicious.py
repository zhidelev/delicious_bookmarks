# -*- coding: utf-8 -*-

import copy
from os.path import join

import pytest

from analyze_delicious import LinkInfo, Stats, Url, get_links

temp_url = "https://plumbr.eu/handbook/garbage-collection-algorithms-implementations/concurrent-mark-and-sweep"
temp_link = {"href": "https://www.smartvideos.ru/", "add_date": "2012", "private": "1", "tags": "education,imported"}

temp_link_public = copy.deepcopy(temp_link)
temp_link_public["private"] = "0"

temp_link_long_date = copy.deepcopy(temp_link)
temp_link_long_date["add_date"] = "1487678923"

temp_link_empty_tags = copy.deepcopy(temp_link)
temp_link_empty_tags["tags"] = ""

delicious_links = join("datasets", "delicious_links_private.html")


@pytest.mark.console
class TestLink:
    def test_url_creation(self):
        assert Url(temp_url)._uri == temp_url

    def test_get_domain_for_url(self):
        assert Url(temp_url).get_domain() == "plumbr.eu"

    def test_print_url(self):
        assert Url(temp_url).__str__() == temp_url


@pytest.mark.console
class TestLinkInfo:
    def test_link_info_get_tags(self):
        assert LinkInfo(temp_link).get_tags() == ["education", "imported"]

    def test_is_private(self):
        assert LinkInfo(temp_link).is_private is True
        assert LinkInfo(temp_link_public).is_private is False

    def test_href(self):
        assert LinkInfo(temp_link).href == "https://www.smartvideos.ru/"

    def test_text(self):
        assert LinkInfo({**temp_link, **{"text": "text2"}}).text == "text2"
        assert LinkInfo({**temp_link, **{"text": ""}, }).text == "www.smartvideos.ru"
        assert LinkInfo({**temp_link, **{"text": "None"}, }).text == "www.smartvideos.ru"

    def test_link_date_short(self):
        assert LinkInfo(temp_link).date == "2012"

    def test_link_date_long(self):
        assert LinkInfo(temp_link_long_date).date == "2017-02-21"

    def test_link_timestamp_short(self):
        assert LinkInfo(temp_link).timestamp == 0

    def test_link_timestamp_long(self):
        assert LinkInfo(temp_link_long_date).timestamp == 1487678923

    def test_link_str_public(self):
        assert LinkInfo(temp_link_public).__str__() == "LinkInfo: www.smartvideos.ru"

    def test_link_str_private(self):
        assert LinkInfo(temp_link).__str__() == "LinkInfo is private."

    def test_link_get_domaint(self):
        assert LinkInfo(temp_link).get_domain() == "www.smartvideos.ru"


@pytest.mark.console
class TestStats:
    def test_stats_privacy(self):
        s = Stats()
        assert s.privacy["private"] == 0
        assert s.privacy["public"] == 0
        s.update_stats(LinkInfo(temp_link))
        assert s.privacy["private"] == 1
        s.update_stats(LinkInfo(temp_link_public))
        assert s.privacy["private"] == 1
        assert s.privacy["public"] == 1

    def test_stats_tags(self):
        s = Stats()
        assert len(s.tags.keys()) == 0
        s.update_stats(LinkInfo(temp_link))
        assert len(s.tags.keys()) == 2
        assert s.tags["imported"] == 1
        assert s.tags["education"] == 1

        s.update_stats(LinkInfo(temp_link_empty_tags))

        assert s.tags["imported"] == 1
        assert s.tags["education"] == 1


@pytest.mark.console
class TestGetLInks:
    def test_private(self):
        f = get_links(delicious_links, private=True)
        assert not next(f).is_private is True
        assert next(f).is_private
        assert next(f).is_private
        with pytest.raises(StopIteration):
            next(f)

    def test_public(self):
        f = get_links(delicious_links)
        assert not next(f).is_private is True
        with pytest.raises(StopIteration):
            next(f)
