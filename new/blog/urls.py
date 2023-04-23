from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('result/', ResultSearchIndexView.as_view(), name='index'),
]
