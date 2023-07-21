from django.urls import path

from .views import *



urlpatterns = [
    path('',index,name='home'),
    path('about/',about,name='about'),
    path('add_comment/',add_comment,name='add_comment'),
    path('login/',login,name='login'),
    # path('post/<int:post_id>/',show_comment,name='post'),
    path('post/<slug:post_slug>/',show_comment,name='post'),
    path('category/<int:cat_id>/',show_category,name='category'),
]