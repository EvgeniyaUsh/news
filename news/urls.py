import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from bbc_news import views

urlpatterns = [
    path("", views.index_handler),
    path("blog/", views.blog_handler),
    path("about/", views.about_handler),
    path("blog_details/", views.blog_details_handler),
    path("category/", views.category_handler),
    path("contact/", views.contact_handler),
    path("latest_news/", views.latest_news_handler),
    path("robots.txt/", views.robots_handler),
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)