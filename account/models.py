from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        
        if not email:
            raise ValueError('User must have email address')
        
        user = self.model(
            email = self.normalize_email(email),
            name=name
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email,name,password=None):
        
       
        user = self.create_user(
            email = email,
            password=password,
            name=name
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user
        
    


# Create your models here.

class User(AbstractBaseUser):
    email= models.EmailField(unique=True)
    name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    
    def get_full_name(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        "All admins are staff."
        return self.is_admin
