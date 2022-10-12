from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import News
from django.urls import reverse

default_news_list_html_template_path = 'news/list.html'
default_news_detail_html_template_path = 'news/detail.html'


def news_feed(request, tmp_path=None):
    if tmp_path is None:
        tmp_path = default_news_list_html_template_path
    latest_news = News.objects.order_by('-pub_date')
    return render(request, tmp_path, {'latest_news': latest_news})


def news_detail(request, news_id, tmp_path=None):
    try:
        n = News.objects.get(id=news_id)
    except:
        raise Http404('Не найдено')

    comments = n.comment_set.order_by('id')

    if tmp_path is None:
        tmp_path = default_news_detail_html_template_path

    return render(request, tmp_path, {'data': n, 'comments': comments})


def add_comment(request, news_id):
    try:
        n = News.objects.get(id=news_id)
    except:
        raise Http404('Не найдено')

    n.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['comment'])

    return HttpResponseRedirect(reverse('news_detail', args=(n.id,)))
