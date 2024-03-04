from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.utils import timezone
from django.core.validators import validate_email
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


# class ArtistProfile(AbstractUser):
#     bio = models.TextField()
#     groups = models.ManyToManyField(Group, related_name='artist_profiles')
#     user_permissions = models.ManyToManyField(Permission, related_name='artist_profiles')

#     def __str__(self):
#         return self.username

class YourModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class UserProfile(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255, default='default_password')
#     email = models.EmailField(unique=True)
#     # user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.CharField(max_length=10, choices=[('member', 'Member'), ('artist', 'Artist')], default='member')

#     def __str__(self):
#         return self.username

# class Artwork(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to='artwork_images/')
#     is_for_sale = models.BooleanField(default=False)
#     price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     is_for_auction = models.BooleanField(default=False)
#     artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

# class AuctionItem(models.Model):
#     artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='auctions')
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     current_bid = models.DecimalField(max_digits=10, decimal_places=2)
#     current_bid_user = models.ForeignKey(ArtistProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
#     def __str__(self):
#         return f"{self.artwork.title} - {self.current_bid}"

#     @property
#     def is_active(self):
#         return self.end_time > timezone.now()

#     @property
#     def time_remaining(self):
#         return (self.end_time - timezone.now()).total_seconds()

# class UserProfile(models.Model):
    # username = models.CharField(max_length=255, unique=True)
    # email = models.EmailField(unique=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # user_type = models.CharField(max_length=10, choices=[('member', 'Member'), ('artist', 'Artist')], default='member')

    # def __str__(self):
    #     return self.user.username
    
from django.contrib.auth.models import AbstractUser
from django.db import models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=[('member', 'Member'), ('artist', 'Artist')], default='member')
    groups = models.ManyToManyField(Group, related_name='user_profiles_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles_permissions')

    def __str__(self):
        return self.user.username
# class UserProfile(models.Model):
#     user_type = models.CharField(max_length=10, choices=[('member', 'Member'), ('artist', 'Artist')], default='member')
#     member_groups = models.ManyToManyField(Group, related_name='member_profiles')
#     member_permissions = models.ManyToManyField(Permission, related_name='member_profiles')

#     def __str__(self):
#         return self.username

class UserProfileGroup(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='groups')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserProfilePermission(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_artist = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'email', 'is_artist']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        user.is_artist = self.cleaned_data['is_artist']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, username=user.username, password=user.password, email=user.email, user_type=user.is_artist)

        return user


#neww
    
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django import forms
from django.contrib.auth.hashers import make_password

class ArtistProfile(AbstractUser):
    bio = models.TextField()
    groups = models.ManyToManyField(Group, related_name='artist_profiles_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='artist_profiles_permissions')

    def __str__(self):
        return self.username


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='artwork_images/')
    is_for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_for_auction = models.BooleanField(default=False)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class AuctionItem(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='auctions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid_user = models.ForeignKey(ArtistProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.artwork.title} - {self.current_bid}"

    @property
    def is_active(self):
        return self.end_time > timezone.now()

    @property
    def time_remaining(self):
        return (self.end_time - timezone.now()).total_seconds()