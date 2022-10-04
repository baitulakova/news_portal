from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import News
from django.urls import reverse


def news_feed(request):
    latest_news = News.objects.order_by('-pub_date')
    return render(request, 'news/list.html', {'latest_news': latest_news})


def news_detail(request, news_id):
    try:
        n = News.objects.get(id=news_id)
    except:
        raise Http404('Не найдено')

    comments = n.comment_set.order_by('id')

    return render(request, 'news/detail.html', {'data': n, 'comments': comments})


def add_comment(request, news_id):
    try:
        n = News.objects.get(id=news_id)
    except:
        raise Http404('Не найдено')

    n.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['comment'])

    return HttpResponseRedirect(reverse('news_detail', args=(n.id,)))
