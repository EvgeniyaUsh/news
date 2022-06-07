from threading import Thread

from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from .crawlers.bbc_crawler import run_parser

from .models import Article, Category, Comment, Newsletter, Tag


@admin.action(description="Count words in article")
def words_counter(modeladmin, request, queryset):
    for obj in queryset:
        text = obj.content.replace("<p>", "").replace("</p>", "")
        words = text.split()
        obj.content_words_count = len(words)
        obj.save()


@admin.action(description="Get new articles")
def get_new_articles(modeladmin, request, queryset):
    for obj in queryset:
        if obj.name == "BBC news":
            thread = Thread(target=run_parser, args=())
            thread.start()


# собирает все статьи одного автора
class CommentsArticleInLine(admin.TabularInline):
    model = Comment


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = (
        "content",
        "short_description",
    )
    list_display = (
        "name",
        "image_code",
        "pub_date",
        "author",
        "content_words_count",
        "unique_words_counter",
    )
    list_filter = (
        "author",
        "pub_date",
    )
    search_fields = (
        "name",
        "author__name",
    )
    actions = (words_counter,)
    inlines = (CommentsArticleInLine,)

    # добавление кастомного поля, которое будет отображать фото статьи
    def image_code(self, object):
        return format_html(
            '<img src="{}" style="max-width: 100px" />', object.main_image.url
        )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "in_menu", "order", "articles_count")
    list_filter = ("in_menu",)
    search_fields = ("name",)
    list_editable = (
        "order",
        "in_menu",
    )
    readonly_fields = ("order",)

    # оптимизация запросов в базу
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("article_set")

    # поле которое считает кол-во статей в категории
    def articles_count(self, object):
        return object.article_set.all().count()



# class AuthorArticleInLine(admin.TabularInline):
#     model = Article
#     exclude = ("content", "short_description")
#
#
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ("name", "ava")
#     search_fields = ("name",)
#     inlines = (AuthorArticleInLine,)
#     actions = (get_new_articles,)
#
#     def ava(self, object):
#         return format_html(
#             '<img src="{}" style="max-width: 70px" />', object.avatar.url
#         )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Newsletter)
