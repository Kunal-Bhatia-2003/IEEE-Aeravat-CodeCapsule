from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('', views.Findex, name='Findex'),
    path('Fsignup', views.Fsignup, name='Fsignup'),
    path('Fsignin', views.Fsignin, name='Fsignin'),
    path('Flogout', views.Flogout, name='Flogout'),
    path('Fhomepage', views.Fhomepage, name='Fhomepage'),
    path('Fprofile', views.Fprofile, name='Fprofile'),
    path('Fdocuments', views.Fdocuments, name='Fdocuments'),
    path('Floan', views.Floan, name='Floan'),
    path('Floan', views.Floan, name='Floan'),
    path('Ftransaction', views.Ftransaction, name='Ftransaction'),
]