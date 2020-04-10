from analyze_delicious import Url, LinkInfo


class TestLink:
    def test_url_creation(self):
        l = Url("https://plumbr.eu/handbook/garbage-collection-algorithms-implementations/concurrent-mark-and-sweep")
        assert (
            l.url
            == "https://plumbr.eu/handbook/garbage-collection-algorithms-implementations/concurrent-mark-and-sweep"
        )

    def test_get_domain_for_url(self):
        assert Url("https://egghead.io/courses/getting-started-with-redux").get_domain() == "egghead.io"


class TestLinkInfo:
    def test_link_info_get_tags(self):
        assert LinkInfo(
            {"href": "http://www.smartvideos.ru/", "add_date": "2012", "private": "1", "tags": "education,imported"}
        ).get_tags() == ["education", "imported"]

    def test_is_private(self):
        assert (
            LinkInfo(
                {"href": "http://www.smartvideos.ru/", "add_date": "2012", "private": "1", "tags": "education,imported"}
            ).is_private
            is True
        )
        assert (
            LinkInfo(
                {"href": "http://www.smartvideos.ru/", "add_date": "2012", "private": "0", "tags": "education,imported"}
            ).is_private
            is False
        )

    def test_href(self):
        assert (
            LinkInfo(
                {"href": "http://www.smartvideos.ru/", "add_date": "2012", "private": "1", "tags": "education,imported"}
            ).href
            == "http://www.smartvideos.ru/"
        )

    def test_text(self):
        assert (
            LinkInfo(
                {
                    "href": "http://www.smartvideos.ru/",
                    "add_date": "2012",
                    "private": "1",
                    "tags": "education,imported",
                    "text": "text2",
                }
            ).text
            == "text2"
        )
        assert (
            LinkInfo(
                {
                    "href": "http://www.smartvideos.ru/",
                    "add_date": "2012",
                    "private": "1",
                    "tags": "education,imported",
                    "text": "",
                }
            ).text
            == "www.smartvideos.ru"
        )
        assert (
            LinkInfo(
                {
                    "href": "https://egghead.io/courses/getting-started-with-redux",
                    "add_date": "2012",
                    "private": "1",
                    "tags": "education,imported",
                    "text": "",
                }
            ).text
            == "egghead.io"
        )
        assert (
            LinkInfo(
                {
                    "href": "https://egghead.io/courses/getting-started-with-redux",
                    "add_date": "2012",
                    "private": "1",
                    "tags": "education,imported",
                    "text": None,
                }
            ).text
            == "egghead.io"
        )

