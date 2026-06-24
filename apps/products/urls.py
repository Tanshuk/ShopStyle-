from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',                    views.product_list_view,   name='list'),
    path('search/',             views.product_search_view, name='search'),
    path('categories/',         views.categories_view,     name='categories'),
    path('<slug:slug>/',        views.product_detail_view, name='detail'),
]