import jwt
from datetime import datetime, timedelta
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.')




class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, phone_number,  email, password=None, ):
        
        if first_name is None:
            raise TypeError('Users must have a first_name')

        if last_name is None:
            raise TypeError('Users must have a first_name')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(first_name=first_name, last_name=last_name, phone_number=phone_number, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, first_name, last_name, phone_number, email, password, ):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(first_name, last_name, phone_number, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField(max_length=200, validators=[alpha])
    last_name = models.CharField(max_length=200, validators=[alpha])
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=254, unique=True,)
    password = models.CharField(max_length=10,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return "%s %s" %(self.first_name, self.last_name)
        

    def get_short_name(self):
        return "%s %s" %(self.first_name, self.last_name)

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')



class Notifications(models.Model):
    user_sender = models.ForeignKey(User,null=True, blank=True, related_name='user_sender', on_delete=models.CASCADE)
    user_revoker = models.ForeignKey(User,null=True, blank=True, related_name='user_revoker', on_delete=models.CASCADE)
    status = models.CharField(max_length=264, null=True, blank=True, default="unread")
    type_of_notification = models.CharField(max_length=264, null=True, blank=True)