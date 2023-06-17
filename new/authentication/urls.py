from django.urls import path
from .views import LoginUserView, RegisterUser, ProfileView, SubscribeView, unsubscribe_view, subscribe_post_view
from django.contrib.auth.views import LogoutView 

app_name = 'authentication'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),w
    path('subscibe/<int:author_id>/', SubscribeView.as_view(), name='subscibe'),
    path('unsubscribe/<int:author_id>/', unsubscribe_view, name='unsubscribe'),
    path('subscibe_list/', subscribe_post_view, name='subscibe_list'),
]

