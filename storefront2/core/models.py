from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# a model that extends abstract user:
class User(AbstractUser): #creating this model is the 1st step to extend the user model
    email=models.EmailField(unique=True)
    