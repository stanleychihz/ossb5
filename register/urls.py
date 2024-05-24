from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('', views.lgn, name='lgn'),
    path('messages/', views.msg, name='msg'),
    path('messages2/', views.msg2, name='msg2'),
    path('i/', views.i, name='i')
]