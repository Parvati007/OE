from django.db import models
from django.contrib.auth.models import User

# Create your models here.

BODY_TYPE_CHOICES = [
    ('Slim', 'Slim'),
    ('Fit', 'Fit'),
    ('Fat', 'Fat'),
]

SKIN_TONE_CHOICES = [
    ('Fair/Light', 'Fair/Light'),
    ('Wheatish', 'Wheatish'),
    ('Dark', 'Dark'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

COLOR_CHOICES = [
    ('Black', 'Black'),
    ('White', 'White'),
    ('Blue', 'Blue'),
    ('Red', 'Red'),
    ('Green', 'Green'),
    ('Brown', 'Brown'),
    ('Navy', 'Navy'),
    ('Olive', 'Olive'),
    ('Maroon', 'Maroon'),
    ('Beige', 'Beige'),
    ('Yellow', 'Yellow'),
    ('Mustard', 'Mustard'),
    ('Teal', 'Teal'),
    ('Pastel', 'Pastel'),
]

CLOTHING_TYPE_CHOICES = [
    ('T-Shirts', 'T-Shirts'),
    ('Shirts', 'Shirts'),
    ('Jeans', 'Jeans'),
    ('Pants', 'Pants'),
    ('Jackets', 'Jackets'),
    ('Hoodies', 'Hoodies'),
    ('Sweaters', 'Sweaters'),
    ('Shorts', 'Shorts'),
    ('Dresses', 'Dresses'),
    ('Skirts', 'Skirts'),
]


class UserStyleProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='style_profile')
    height = models.CharField(max_length=10, help_text="Height in cm or ft/in")
    skin_tone = models.CharField(max_length=20, choices=SKIN_TONE_CHOICES)
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES)
    favourite_colors = models.JSONField(default=list, help_text="List of favorite colors")
    preferred_clothing_types = models.JSONField(default=list, help_text="List of preferred clothing types")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Style Profile"
        verbose_name_plural = "User Style Profiles"

    def __str__(self):
        return f"{self.user.username}'s Style Profile"
