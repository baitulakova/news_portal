from django.http import HttpRequest
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from .views import *
from os import remove


news_list_content = '''{% if latest_news %}{% for n in latest_news %}{{ n.pub_date|date:"r" }} 
<a href="{% url 'news_detail' n.id %}">{{n.title}}</a>
{% if n.was_published_recently %} NEW {% endif %}{% endfor %}
{% else %}No news{% endif %}'''


news_details_content = """Title: {{ data.title }} Text: {{ data.text }} Author{{ data.author }} Pub_date{{ data.pub_date|date:"r" }}"""


class NewsTest(TestCase):
    def setUp(self):
        News.objects.create(title='test-1', pub_date=timezone.now() + timedelta(minutes=2))
        News.objects.create(title='test-2', pub_date=timezone.now() - timedelta(minutes=1))

    def test_was_published_recently(self):
        n = News.objects.get(title='test-1')
        assert n.was_published_recently() is True

        n = News.objects.get(title='test-2')
        assert n.was_published_recently() is False


class ViewsTestNoNewsCase(TestCase):
    def setUp(self):
        News.objects.all().delete()

        f = open("templates/test_html_tmp.html", "x")
        f.write(news_list_content)

    def tearDown(self):
        remove("templates/test_html_tmp.html")

    def test_news_feed(self):
        req = HttpRequest()
        resp = news_feed(req, "test_html_tmp.html")
        assert "b'No news'" == str(resp.content)

    def test_get_news_by_id(self):
        req = HttpRequest()
        self.assertRaises(Http404, news_detail, req, 1)

    def test_add_comment(self):
        req = HttpRequest()
        self.assertRaises(Http404, add_comment, req, 1)


class ViewsTest(TestCase):
    def setUp(self):
        f = open("templates/test_html_tmp.html", "x")
        f.write(news_list_content)

        f = open("templates/test_html_tmp_detail.html", "x")
        f.write(news_details_content)

    def tearDown(self):
        remove("templates/test_html_tmp.html")
        remove("templates/test_html_tmp_detail.html")

    def update_data(self):
        n = News.objects.get(id=1)
        n.pub_date = timezone.datetime(2022, 10, 11, 18, 7, 21)
        n.save()

        n = News.objects.get(id=2)
        n.pub_date = timezone.datetime(2022, 10, 11, 18, 7, 21)
        n.save()

    def test_news_feed(self):
        self.update_data()

        req = HttpRequest()
        resp = news_feed(req, "test_html_tmp.html")
        # we create 2 news in 0002_insert_test_data.py migration
        expected = """b'Tue, 11 Oct 2022 18:07:21 +0600 \\n<a href="/news/1/">Lorem Ipsum</a>\\nTue, 11 Oct 2022 18:07:21 +0600 \\n<a href="/news/2/">Suspendisse potenti.</a>\\n\\n'"""
        assert expected == str(resp.content)

    def test_news_detail(self):
        self.update_data()

        req = HttpRequest()
        # we create 2 news in 0002_insert_test_data.py migration
        resp = news_detail(req, 1, "test_html_tmp_detail.html")
        expected = """b'Title: Lorem Ipsum Text: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ultricies dictum nibh. Aenean eget elit elit. Integer sit amet tellus quis eros pellentesque semper vitae at risus. Aliquam eget odio nunc. Nunc bibendum tincidunt elementum. Suspendisse a mauris suscipit, laoreet enim vel, hendrerit nulla. Pellentesque tristique quam non semper semper.Donec a posuere nisl. Sed sapien massa, blandit sed dignissim tristique, egestas non nisl. Proin non nunc id quam sagittis imperdiet sed sed urna. Suspendisse pulvinar vel orci nec condimentum. Proin volutpat fermentum dictum. In posuere at elit tristique pretium. Sed eget lectus sit amet risus commodo congue. Vivamus vehicula semper libero quis sagittis. Pellentesque ut ultrices odio, ut commodo urna. Quisque varius suscipit luctus. Cras commodo vehicula dapibus. In in tempor mi, non feugiat eros. In a diam urna. Duis at felis lectus. Nam auctor viverra nisl quis faucibus. AuthorJohn Doe Pub_dateTue, 11 Oct 2022 18:07:21 +0600'"""
        assert expected == str(resp.content)

    def test_add_comment(self):
        dct = {'name': "John", "comment": "test"}
        resp = self.client.post(path="/news/1/add_comment", data=dct)
        self.assertRedirects(resp, '/news/1/', 302, 200)

