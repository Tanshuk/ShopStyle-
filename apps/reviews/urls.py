from django.urls import path
from . import views
app_name = 'reviews'
urlpatterns = [
    path('', views.review_list_view, name='list'),
]