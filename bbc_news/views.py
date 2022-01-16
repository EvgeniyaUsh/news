from django.shortcuts import render
from django.db.models import Count

from .models import Article, Category


def index_handler(request):
    last_articles = Article.objects.all().order_by("-pub_date")[:6]
    menu_categories = Category.objects.annotate(
        count=Count("article__id")).order_by("count")[:6]

    context = {'last_articles': last_articles,
               "menu_categories": menu_categories}
    return render(request, "news/index.html", context)


def categories_handler(request):
    context = {}
    return render(request, "news/category.html", context)


def category_handler(request, slug):
    context = {}
    return render(request, "news/category.html", context)


def blog_handler(request):
    context = {}
    return render(request, "news/blog.html", context)


def about_handler(request):
    context = {}
    return render(request, "news/about.html", context)


def blog_details_handler(request, slug):
    context = {}
    return render(request, "news/blog_details.html", context)


def contact_handler(request):
    context = {}
    return render(request, "news/contact.html", context)


def latest_news_handler(request):
    context = {}
    return render(request, "news/latest_news.html", context)


def robots_handler(request):
    context = {}
    return render(request, "news/robots.txt", context,
                  content_type="text/plain")
