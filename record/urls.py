from django.urls import path, include
from record import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

