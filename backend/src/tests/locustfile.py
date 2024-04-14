from locust import HttpUser, task


class BasicBookmarksUser(HttpUser):
    @task
    def list_all_bookmarks(self):
        self.client.get("/bookmarks")

    @task
    def create_bookmark(self):
        self.client.post(
            "/bookmarks/",
            json={
                "uri": "https://example.com",
                "title": "Example Domain",
                "description": "An example domain for use in illustrative examples in documents. You may use!",
            },
        )
