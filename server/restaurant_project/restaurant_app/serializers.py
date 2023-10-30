from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        return user

# model serializers starts here...

class CustomerSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Customer 
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Categories 
        fields = "__all__"


class MenuProductsSerializer(serializers.ModelSerializer):

    class Meta: 
        model = MenuProducts 
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Order 
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta: 
        model = OrderItem 
        fields = "__all__"


# class HotelSerializer(serializers.ModelSerializer):

#     class Meta: 
#         model = OrderItem 
#         fields = "__all__"


# custom serializers 
class UpdateItemSerializer(serializers.Serializer):
   
   productId = serializers.CharField()
   action = serializers.CharField()