from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser

# used a form to customize the damin panel 
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "phone_number",)

        


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "phone_number",)