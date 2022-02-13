from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path("", views.index, name="index"),
    path("read/<str:headlines>", views.read_news, name="read_news"),
    path("tag/<str:tagtitle>", views.tag_news, name="tag_news"),
    path("choose/<str:categorytitle>", views.category, name="category"),
    path("search", views.search, name="search"),
    path("aboutus", views.aboutus, name="aboutus")
]