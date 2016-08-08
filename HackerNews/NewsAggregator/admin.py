from django.contrib import admin
from models import Article


class NewsAggregatorAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ['article_id', 'title']

admin.site.register(Article, NewsAggregatorAdmin)
