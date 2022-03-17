from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Article, Category


def index_handler(request):
    last_articles = Article.objects.all().order_by("-pub_date")[:6].prefetch_related('categories')

    context = {'last_articles': last_articles}
    return render(request, "news/index.html", context)


def blog_handler(request, **kwargs):
    cat_slugs = kwargs.get('cat_slugs')
    page = int(kwargs.get('number', 1))
    count_pages = 7
    category = None
    if cat_slugs:
        category = Category.objects.get(slug=cat_slugs)
        last_articles = Article.objects.filter(categories__slug=cat_slugs).order_by("-pub_date")[:10].prefetch_related(
            'categories')
        articles_count = Article.objects.filter(categories__slug=cat_slugs).count()
        max_page = articles_count // count_pages + 1

    else:
        articles_count = Article.objects.all().count()
        max_page = articles_count // count_pages + 1
        last_articles = Article.objects.all().order_by("-pub_date")[
                        (page - 1) * count_pages:page * count_pages].prefetch_related('categories')

    context = {
        'last_articles': last_articles,
        'pages': range(2, max_page + 1),
        'current_page': page,
        'max_page': max_page,
        'category': category
    }
    return render(request, "news/blog.html", context)


def blog_details_handler(request, post_slug):
    article = Article.objects.get(slug=post_slug)
    try:
        prev_article = Article.objects.get(id=article.id - 1)
    except ObjectDoesNotExist:
        prev_article = None
    try:
        next_article = Article.objects.get(id=article.id + 1)
    except ObjectDoesNotExist:
        next_article = None
    context = {
        'article': article,
        'prev_article': prev_article,
        'next_article': next_article
    }
    return render(request, "news/blog_details.html", context)


def categories_handler(request):
    context = {}
    return render(request, "news/category.html", context)


def about_handler(request):
    context = {}
    return render(request, "news/about.html", context)


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
