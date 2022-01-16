import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from django.utils.timezone import make_aware
from requests_html import HTMLSession
from slugify import slugify

from bbc_news.models import Article, Author, Category

author = Author.objects.get(id=2)
print(author)


def crawl_one(url):
    with HTMLSession() as session:
        response = session.get(url)
    try:
        name = response.html.xpath(
            '//div[@class="ssrcss-1ocoo3l-Wrap e42f8511"]//h1/text()'
        )[0]

        content = response.html.xpath(
            '//div[@class="ssrcss-1ocoo3l-Wrap e42f8511"]//p')

        image_url = response.html.xpath(
            '//div[@class="ssrcss-1ocoo3l-Wrap e42f8511"]//img/@src'
        )[0]

        pub_date = response.html.xpath(
            '//div[@class="ssrcss-1ocoo3l-Wrap e42f8511"]//time/@datetime'
        )[0]

        print('pub_date', pub_date)

        cats = response.html.xpath(
            '//a[@class="ssrcss-1yno9a1-StyledLink ed0g1kj0"]')

        my_content = ""
        short_description = ""
        for element in content:
            my_content += f"<{element.tag}>" + element.text + f"<{element.tag}>"
            if len(short_description) < 200:
                short_description += element.text + " "

        image_name = slugify(name)

        pub_date = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%S.%fZ")

        print(pub_date)

        img_type = image_url.split(".")[-1]

        img_path = f"images/{image_name}.{img_type}"

        with open(f"media/{img_path}", "wb") as f:
            with HTMLSession() as session:
                response = session.get(image_url)
                f.write(response.content)

        categories = []

        for cat in cats:
            categories.append(
                {"name": cat.text.strip(), "slug": slugify(cat.text)})

        article = {
            "name": name,
            "slug": slugify(name),
            "content": my_content,
            "short_description": short_description.strip(),
            "main_image": img_path,
            "pub_date": make_aware(pub_date),
            "author": author,
        }

        article, created = Article.objects.get_or_create(**article)
        for category in categories:
            cat, created = Category.objects.get_or_create(**category)
            article.categories.add(cat)

    except Exception as ex:
        print(f"[{url}]", ex, type(ex), sys.exc_info()[-1].tb_lineno)


def get_fresh_news():
    """Отбирает статьи и возвращает ссылки на них"""
    base_url = "https://www.bbc.com/news/business"

    with HTMLSession() as session:
        response = session.get(base_url)

    links = response.html.absolute_links

    fresh_news = []

    for link in links:
        try:
            if link.split("-")[-1].isdigit():
                fresh_news.append(link)
        # create except class
        except Exception:
            pass

    return fresh_news


def run_parser():
    fresh_news = get_fresh_news()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawl_one, fresh_news)
