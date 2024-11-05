from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('homepage/', views.homepage, name="homepage"),
    path('logout/', views.logout_view, name='logout'),
    path('adduser/', views.adduser, name="adduser"),
    path('updateuser/<int:user_id>/', views.updateuser, name='updateuser'),
    path('deleteuser/<int:user_id>/', views.deleteuser, name='deleteuser'),
]

