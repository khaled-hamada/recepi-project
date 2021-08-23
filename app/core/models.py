from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import validate_email
from django.conf import settings
import uuid, os


def recipe_img_file_path(instance , filename):
    """ Generate file path for new recipe image """
    ext = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipes/', unique_filename)
class UserManager(BaseUserManager):
    

    def create_user(self, email , password = None, **extra_args):
       
        if not email :
            raise ValueError('Users must have an email address')
        ## check correct email 
        try:
            validate_email(email)
        except Exception as ex:
            raise ValueError('Users must have a vaild email address')

        
        user = self.model(email = self.normalize_email(email), **extra_args)
        user.set_password(password) ## password must be encypted before being saved
        user.save(using = self._db) ## allow client to use and dbms

        return user 

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user




class User(AbstractBaseUser , PermissionsMixin):
    """ custom user model to use an email for auth. 
        instead of user name 
    
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()


    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
            on_delete= models.CASCADE )
    

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True , upload_to=recipe_img_file_path)
   
    def __str__(self):
        return self.title
