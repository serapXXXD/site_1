from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', IndexSearchView.as_view(), name='index'),
]
