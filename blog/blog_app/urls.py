from django.urls import path
from . import blog_crud,user_mgmnt


urlpatterns = [

    #======================User Management===========================#
  
    path('register/',user_mgmnt.register.as_view(),name='register'),
    path('login/',user_mgmnt.Login.as_view(),name='login'),
    path('logout/',user_mgmnt.Logout.as_view(),name='Logout'),
 
    #======================Blog post===========================#
    
    path('blogpost/',blog_crud.BlogPostAPIView.as_view(),name='blogpost'),
    path('blogpost/<int:pk>/', blog_crud.BlogPostAPIView.as_view(),name='blogpost_update_delete'),
    path('blogpost/comments/', blog_crud.CommentCreateAPIView.as_view(),name='blogpost_commemt'),
    path('blogpost/search/', blog_crud.BlogPostSearchAPIView.as_view(),name='blog_post_serach')

    
]
