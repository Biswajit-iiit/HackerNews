from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import models
import utils

@csrf_exempt
def update_article(request):
    """Function to display top news from HackerNews"""

    try:
        article_id_arr = models.Article.objects.fetch_top_article_ids()
        article_dict = models.Article.objects.get_article_arr(article_id_arr)
        return HttpResponse(utils.render_result(request,article_dict))
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
    return HttpResponse(utils.render_result(request,article_dict))


@csrf_exempt
def display_news(request):
    """Display all stored articles."""

    article_dict = models.Article.objects.get_article_arr()
    return HttpResponse(utils.render_result(request,article_dict))
