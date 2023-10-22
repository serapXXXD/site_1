from core.tests.base_test import BaseTest


class TestPostViewset(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url_post = '/api/v1/posts/'

    def test_create(self):
        create = self.test_user_1_api_client.post(self.url_post, data={"title": "111111",
                                                                       "body": "111111",
                                                                       "tags": [self.test_tag.id],
                                                                       "category": self.test_category.id})

        self.assertEquals(create.status_code, 201)
