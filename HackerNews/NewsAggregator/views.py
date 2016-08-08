from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context
import models
import json


@csrf_exempt
def display_news(request):
    """Function to display top news from HackerNews"""

    try:
        article_id_arr = models.Article.objects.fetch_top_article_ids()
        article_dict = models.Article.objects.get_article_arr(article_id_arr)
        s = str(
            render(
                request,
                'news.html',
                article_dict,
                content_type='text/html'))
        x = s.replace("u&#39;", "'")  # removing unicode issues in JS
        y = x.replace("&#39;", "'")
        z = y.replace("Content-Type: text/html", "")
        p = z.replace("u&quot;","'")
        q = p.replace("&quot;","'")
        return HttpResponse(q)
    except Exception:
        return HttpResponse('Error')


@csrf_exempt
def search_article(request):
    """Search for an article"""

    try:
        key = request.GET['key']
    except KeyError:
        return HttpResponse('Please supply key')
    article_dict = models.Article.objects.search_article(key)
    s = str(
        render(
            request,
            'news.html',
            article_dict,
            content_type='text/html'))
    x = s.replace("u&#39;", "'")  # removing unicode issues in JS
    y = x.replace("&#39;", "'")
    z = y.replace("Content-Type: text/html", "")
    p = z.replace("u&quot;","'")
    q = p.replace("&quot;","'")
    return HttpResponse(q)
