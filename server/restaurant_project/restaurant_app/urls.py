from django.urls import path
from .views import UserRegistrationView, UserAuthenticationView
from . import views


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserAuthenticationView.as_view(), name='user-login'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('processOrder/', views.processOrder, name='processOrder'),

]
