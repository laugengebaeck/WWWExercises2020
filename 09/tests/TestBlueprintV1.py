import hashlib
import random

from flask_testing import TestCase

from flask_common.test.util import base_app

from app.views_v1 import V1


class V1Test(TestCase):
    def create_app(self):
        app = base_app()
        app.register_blueprint(V1, url_prefix="")
        return app

    def test_status(self):
        health_response = self.client.get('/health', content_type="application/json")
        self.assert200(health_response, {"status": "up"})

    def fetch_data(self):
        fetch_response = self.client.post('/images/fetch')
        self.assert200(fetch_response)

    def test_double_fetch(self):
        self.fetch_data()
        count_response_01 = self.client.get('/images')
        self.assert200(count_response_01)
        self.fetch_data()
        count_response_02 = self.client.get('/images')
        self.assert200(count_response_02)
        self.assertEqual(count_response_01.json['count'], count_response_02.json['count'])

    def test_fetch_some_images(self):
        self.fetch_data()
        count_response = self.client.get('/images')
        self.assert200(count_response)

        image_list = []
        seen_images = {}

        for i in range(0, count_response.json['count'], 500):
            image_list_response = self.client.get('/images?limit=500&offset={}'.format(i))
            self.assert200(image_list_response)

            self.assertEqual(500, len(image_list_response.json['images']))

            image_list += image_list_response.json['images']

        random.shuffle(image_list)

        for image in image_list[:33]:
            image_metadata_response = self.client.get('/images/{}'.format(image['id']))
            self.assert200(image_metadata_response)

            self.assertDictEqual(image, image_metadata_response.json['image'])

            image_bitmap_response = self.client.get('/images/{}/bitmap'.format(image['id']))
            self.assert200(image_bitmap_response)

            hash_value = hashlib.sha256(image_bitmap_response.data)
            self.assertFalse(hash_value in seen_images)
            seen_images[hash_value] = True

    def test_content_type_bitmap(self):
        self.fetch_data()
        image_list_response = self.client.get('/images?limit=1')
        self.assert200(image_list_response)
        self.assertEqual(len(image_list_response.json['images']), 1)

        image_bitmap_response = self.client.get('/images/{}/bitmap'.format(image_list_response.json['images'][0]['id']))
        self.assert200(image_bitmap_response)
        self.assertEqual('image/jpeg', image_bitmap_response.content_type)
        self.assertGreater(len(image_bitmap_response.data), 100)

    def test_invalid_images_limit_text(self):
        image_list_response = self.client.get('/images?limit=bla')
        self.assert400(image_list_response)

    def test_invalid_images_limit_negative(self):
        image_list_response = self.client.get('/images?limit=-123')
        self.assert400(image_list_response)

    def test_invalid_images_limit_large(self):
        image_list_response = self.client.get('/images?limit=501')
        self.assert400(image_list_response)

    def test_invalid_images_offset_text(self):
        image_list_response = self.client.get('/images?offset=fds')
        self.assert400(image_list_response)

    def test_invalid_images_offset_negative(self):
        image_list_response = self.client.get('/images?offset=-3')
        self.assert400(image_list_response)

    def test_images_offset_large(self):
        image_list_response = self.client.get('/images?offset=10000')
        self.assert200(image_list_response)
        self.assertEqual(len(image_list_response.json['images']), 0)

    def test_unknown_image_metadata(self):
        image_bitmap_response = self.client.get('/images/9999')
        self.assert404(image_bitmap_response)

        self.assertGreater(len(image_bitmap_response.json['message']), 8)

    def test_unknown_image_bitmap(self):
        image_bitmap_response = self.client.get('/images/9999/bitmap')
        self.assert404(image_bitmap_response)

    def test_get_answers(self):
        answers_response = self.client.get('/answers')
        self.assert200(answers_response)

    def test_get_task_list(self):
        task_response = self.client.get('/tasks')
        self.assert200(task_response)
