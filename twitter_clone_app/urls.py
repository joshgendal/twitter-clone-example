from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('tweet', views.tweet),
    path('logout', views.logout),
    path('add-tweet', views.add_tweet),
    path('feed', views.feed),
    path('edit-tweet/<int:tweet_id>', views.edit_tweet_template),
    path('edit-tweet', views.edit_tweet),
    path('add-comment', views.add_comment)
]

