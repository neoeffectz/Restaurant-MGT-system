from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(    
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    
# added a serializer for staff registration
    
class StaffRegistrationSerializer(serializers.ModelSerializer):

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





# model serializers starts here...




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


class UpdateItemSerializer(serializers.Serializer):
   
   productId = serializers.CharField()
   action = serializers.CharField()