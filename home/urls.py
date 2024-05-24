from django.urls import path
from . import views

urlpatterns = [
    
    path('lgn', views.logout_user, name='logout_user'),
    path('suggestion/', views.suggestion, name='suggestion'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox_admin/', views.inbox_admin, name='inbox_admin'),
    path('outbox/', views.outbox, name='outbox'),
    path('view_message/<pk>', views.view_message, name='view_message'),
    path('reply/<pk>', views.reply, name='reply'),
    path('inprivate/', views.inprivate, name='inprivate'),
    path('outbox/<pk>', views.delete_outbox, name='delete_outbox'),
    #path('edit/<pk>', views.delete_image, name='delete_image'),
    #path('edit/<pk>', views.delete_audio, name='delete_audio'),
    #path('edit/<pk>', views.delete_video, name='delete_video'),
    path("delete_comment/<pk>", views.delete_comment, name="delete_comment"),
    path('analysis/', views.analysis, name='analysis'),
    path('edit/<pk>', views.edit, name='edit'),
    path('mycomments/', views.mycomments, name='mycomments'),
    path("view_message", views.like, name="like")
]
