from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.item_create, name="item_create"),
    path("search/", views.search_items, name="search"),
    path("statistics/", views.statistics, name="statistics"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("items/<int:item_id>/edit/", views.item_update, name="item_update"),
    path("items/<int:item_id>/delete/", views.item_delete, name="item_delete"),
]
