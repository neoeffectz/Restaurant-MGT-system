from rest_framework import serializers
from .models import *
from Menu.models import MenuProducts, Categories
from django.contrib.auth import authenticate
from users.models import CustomUser

# serializer for user registration 
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ( 'password', 'email', 'first_name', 'last_name', 'phone_number')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(    
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number = validated_data.get('phone_number', ''),
        )
        return user
    
# added a serializer for staff registration

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


<<<<<<< Updated upstream
=======
# class HotelSerializer(serializers.ModelSerializer):

#     class Meta: 
#         model = Hotel 
#         fields = "__all__"


# custom serializers 
>>>>>>> Stashed changes
class UpdateItemSerializer(serializers.Serializer):
   
   productId = serializers.CharField()
   action = serializers.CharField()