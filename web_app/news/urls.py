import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from bbc_news import views

urlpatterns = [
                  path("", views.IndexView.as_view(), name="homepage"),
                  path("about/", views.AboutView.as_view(), name="about"),

                  path("blog/", views.BlogListView.as_view(), name="blog"),

                  path("blog_details/<post_slug>", views.ArticleDetailView.as_view(), name="article"),

                  # path("blog/", views.CategoryDeleteView.as_view(), name="categories"),
                  path("category/<cat_slug>", views.CategoryListView.as_view(), name="category"),

                  path("contact/", views.ContactView.as_view(), name="contact"),
                  path("latest_news/", views.LatestNewsView.as_view(), name="latest_news"),
                  path("robots.txt/", views.RobotsView.as_view()),
                  path("admin/", admin.site.urls),
                  path("summernote/", include("django_summernote.urls")),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
