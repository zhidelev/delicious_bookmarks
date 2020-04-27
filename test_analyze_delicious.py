from analyze_delicious import Url, LinkInfo, Stats
import copy

temp_url = "https://plumbr.eu/handbook/garbage-collection-algorithms-implementations/concurrent-mark-and-sweep"
temp_link = {"href": "https://www.smartvideos.ru/", "add_date": "2012", "private": "1", "tags": "education,imported"}

temp_link_public = copy.deepcopy(temp_link)
temp_link_public["private"] = "0"

temp_link_long_date = copy.deepcopy(temp_link)
temp_link_long_date["add_date"] = "1487678923"

temp_link_empty_tags = copy.deepcopy(temp_link)
temp_link_empty_tags["tags"] = ""


class TestLink:
    def test_url_creation(self):
        assert Url(temp_url).url == temp_url

    def test_get_domain_for_url(self):
        assert Url(temp_url).get_domain() == "plumbr.eu"


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
        assert LinkInfo({**temp_link, **{"text": ""},}).text == "www.smartvideos.ru"
        assert LinkInfo({**temp_link, **{"text": "None"},}).text == "www.smartvideos.ru"

    def test_link_date_short(self):
        assert LinkInfo(temp_link).date == "2012"

    def test_link_date_long(self):
        assert LinkInfo(temp_link_long_date).date == "2017-02-21"


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
