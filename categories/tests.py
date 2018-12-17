# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client

from categories.models import Category


class CategoryAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='123456test_user')
        self.category = Category.objects.create(name="test category 1", author=self.user)
        self.response_map = {
            'name': "test category 1"
        }

        self.request_data = {
            "jsonrpc": "2.0",
            "method": "",
            "id": 1,
            "params": {}
        }

    def test_category_views(self):
        request = self.request_data
        request["method"] = "category.views"
        response = self.client.post('/api/',
                                    data=str(json.dumps(request)),
                                    content_type="application/json")
        self.assertTrue(response.status_code == 200, "success")

    def test_category_details(self):
        request = self.request_data
        request["method"] = "category.details"
        request["params"] = {
            "category_id": 1
        }
        response = self.client.post('/api/',
                                    data=str(json.dumps(request)),
                                    content_type="application/json")
        self.assertTrue(response.status_code == 200, "success")

    def tearDown(self):
        print("Done")
