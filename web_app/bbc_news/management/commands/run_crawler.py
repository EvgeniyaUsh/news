from django.core.management.base import BaseCommand

from web_app.bbc_news.crawlers.bbc_crawler import run_parser


class Command(BaseCommand):
    help = "Run BBC news parser from site - https://www.bbc.com/news/business"

    def handle(self, *args, **options):
        run_parser()
