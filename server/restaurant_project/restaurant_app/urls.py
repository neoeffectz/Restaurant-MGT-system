from django.urls import path
from .views import *
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # used djangrestframework-simplejwt to add auth urls
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),

    #urls for crud action on product
    path('product/', CreateProductView.as_view(), name='create-product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),



    path('restaurant/', views.restaurant, name='restaurant'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('processOrder/', views.processOrder, name='processOrder'),

]
