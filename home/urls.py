from django.urls import path

import home.views as home

urlpatterns = [
    path('', home.home_view, name='home.index'),
]
