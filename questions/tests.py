# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.client import Client

from likes.models import Like
from questions.models import Question


class QuestionAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', password='123456test_user')
        self.question = Question.objects.create(name="test question 1",
                                                content="test content",
                                                author=self.user)
        self.question_model_type = ContentType.objects.get_for_model(self.question)

        self.response_map = {
            'name': "test category 1"
        }

        self.request_data = {
            "jsonrpc": "2.0",
            "method": "",
            "id": 1,
            "params": {}
        }

    def test_question_views(self):
        request = self.request_data
        request["method"] = "question.views"
        response = self.client.post('/api/',
                                    data=str(json.dumps(request)),
                                    content_type="application/json")
        self.assertTrue(response.status_code == 200, "success")

    def check_likes(self):
        like = Like.objects.create(content_type=self.question_model_type, object_id=self.question.id, user=self.user)
        print(str(like.objects.count()))
        self.assertTrue(like.objects.count() == 1, "success")

    def tearDown(self):
        print("Done")
