from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users_app'

urlpatterns = [
    # include default auth urls
    path('', include('django.contrib.auth.urls')),
    path ('signup/', views.signupView, name= 'signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
