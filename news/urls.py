from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_feed),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('<int:news_id>/add_comment', views.add_comment, name='add_comment')
]
