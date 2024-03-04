from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Artwork

class CustomLoginForm(forms.Form):
    # Add your custom login form fields if needed
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    # Add your custom signup form fields if needed
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

from django.contrib.auth.hashers import make_password

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_artist = forms.BooleanField(required=False, initial=False)
    user_type = forms.ChoiceField(choices=[('artist', 'Artist'), ('member', 'Member')], widget=forms.RadioSelect)

    class Meta:
        model = UserProfile
        fields = ['user_type', 'password', 'is_artist']

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        user_profile.user = user
        user_profile.user_type = self.cleaned_data['user_type']
        
        if commit:
            user_profile.save()

        return user_profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     is_artist = forms.BooleanField(required=False, initial=False)

#     class Meta:
#         model = UserProfile
#         fields = ['username', 'password', 'email', 'is_artist']

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if UserProfile.objects.filter(email=email).exists():
#             raise ValidationError("This email is already in use.")
#         return email

#     def save(self, commit=True):
#         user = User.objects.create_user(
#             username=self.cleaned_data['username'],
#             password=self.cleaned_data['password'],
#             email=self.cleaned_data['email']
#         )
#         user.is_artist = self.cleaned_data['is_artist']
#         user.save()

#         # Now link the UserProfile to the User
#         user_profile = UserProfile.objects.create(
#             user=user,
#             username=user.username,
#             password=user.password,
#             email=user.email,
#             user_type='artist' if user.is_artist else 'member'
#         )

#         return user


from .models import ArtistProfile


class ArtistProfileForm(forms.ModelForm):
    # Add your custom artist profile form fields if needed
    class Meta:
        model = ArtistProfile
        fields = ['bio', 'groups', 'user_permissions']

    widgets = {
        'bio': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    }

class LoginForm(forms.Form):
    # Add your custom login form fields if needed
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from .models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image', 'is_for_sale', 'price', 'is_for_auction']

    def __init__(self, *args, **kwargs):
        super(ArtworkForm, self).__init__(*args, **kwargs)
        # Customize the form if needed, for example, set specific attributes for fields
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 15})


from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']