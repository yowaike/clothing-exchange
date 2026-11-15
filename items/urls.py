from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.home, name="home"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("search/", views.search_items, name="search"),
    path("statistics/", views.statistics, name="statistics"),
]
