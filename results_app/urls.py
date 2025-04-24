''' Defines url patterns for the results app. '''
from django.urls import path
from . import views

app_name = 'results_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('get_all_results/', views.get_all_results, name='get_all_results'),
    path('check_result/', views.checkResult, name='check_result'),
    path('make-card/', views.makeCard, name='make_card'),
]
