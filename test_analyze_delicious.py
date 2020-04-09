from analyze_delicious import Link


class TestLink:
    def test_link_creation(self):
        l = Link("https://plumbr.eu/handbook/garbage-collection-algorithms-implementations/concurrent-mark-and-sweep")
        assert l.url == "https://plumbr.eu/handbook/garbage-collection-algorithms-implementations/concurrent-mark-and-sweep"

    def test_get_domain_for_link(self):
        assert Link("https://egghead.io/courses/getting-started-with-redux").get_domain() == "egghead.io"