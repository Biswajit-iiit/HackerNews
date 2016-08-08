from __future__ import unicode_literals
from django.db import models
import requests
from bulk_update.helper import bulk_update
import config
from HackerNews.server_config import MAX_RESULT


class ArticleManager(models.Manager):
    """Model Manager for Article class."""

    def fetch_top_article_ids(self):
        """ This function returns ids of top articles."""

        end_point = "https://community-hacker-news-v1.p.mashape.com/topstories.json?print=pretty"
        headers = {"X-Mashape-Key": config.API_KEY}
        article_id_arr_fetched = eval(
            requests.get(
                end_point,
                headers=headers).text)
        article_id_arr_existing = list(
            Article.objects.all().values_list(
                'article_id', flat=True))
        article_id_arr_new = list(
            set(article_id_arr_fetched) -
            set(article_id_arr_existing))
        article_id_arr_common = list(
            set(article_id_arr_fetched).intersection(
                set(article_id_arr_existing)))
        self.save_article(article_id_arr_new)
        self.update_article(article_id_arr_common)
        return article_id_arr_new

    def fetch_article(self, article_id):
        """This function fetch the article details."""

        end_point = "https://community-hacker-news-v1.p.mashape.com/item/{}.json?print=pretty".format(
            article_id)
        headers = {"X-Mashape-Key": config.API_KEY}
        article = eval(requests.get(end_point, headers=headers).text)
        return article

    def get_article_arr(self, article_id_arr):
        """This function returns array of articles."""

        article_arr = Article.objects.filter(
            article_id__in=article_id_arr).values()
        for article in article_arr:
            article['article_id'] = str(article['article_id'])
            article['upvote_count'] = str(article['upvote_count'])
        article_dict = {"article_arr": article_arr}
        return article_dict

    def get_article_sentiment(self, article_title):
        """This function fetches the sentiment of an article."""

        end_point = "https://community-sentiment.p.mashape.com/text/"
        headers = {"X-Mashape-Key": config.API_KEY}
        payload = {"txt": article_title}
        res = eval(
            requests.post(
                end_point,
                data=payload,
                headers=headers).text)
        return res['result']['sentiment']

    def save_article(self, article_id_arr):
        """This function stores the articles in database."""

        article_obj_arr = []
        count = 0
        for article_id in article_id_arr:
            try:
                print article_id
                article = self.fetch_article(article_id)
                sentiment = self.get_article_sentiment(article['title'])
                article_obj = Article(
                    article_id=article['id'],
                    title=article['title'],
                    url=article['url'],
                    user=article['by'],
                    sentiment=sentiment,
                    upvote_count=article['score'])
                article_obj_arr.append(article_obj)
                count += 1
                if count == MAX_RESULT:
                    break
            except KeyError:
                continue
            except Exception:
                import traceback
                print traceback.format_exc()
        Article.objects.bulk_create(article_obj_arr)
        print 'Saved'

    def update_article(self, article_id_arr):
        """This function updates the score of the already stored articles."""
        try:
            article_qs = Article.objects.filter(article_id__in=article_id_arr)
            for article in article_qs:
                article.upvote_count = self.fetch_article(
                    article.article_id)['score']
            bulk_update(article_qs)
        except Exception:
            pass

    def search_article(self, key):
        """This function searches for a keyword in article titles."""

        article_arr = Article.objects.filter(title__icontains=key).values()
        if len(article_arr) > 0:
            for article in article_arr:
                article['article_id'] = str(article['article_id'])
                article['upvote_count'] = str(article['upvote_count'])
            article_dict = {"article_arr": article_arr}
            return article_dict
        else:
            return {}


class Article(models.Model):
    """Article model stores info related to each article."""

    article_id = models.PositiveIntegerField(primary_key=True)
    title = models.TextField()
    url = models.URLField(max_length=1024, null=True, blank=True)
    user = models.CharField(max_length=30)
    upvote_count = models.PositiveIntegerField()
    sentiment = models.CharField(max_length=30)
    objects = ArticleManager()

    def __unicode__(self):
        return str(self.article_id) + "----" + self.title
