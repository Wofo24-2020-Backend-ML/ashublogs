from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import PhoneNumberUserManager
from django.utils import timezone

# Create your models here.

class User(AbstractBaseUser):
    phone_number = models.CharField(unique=True, max_length=13)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254)

    object = PhoneNumberUserManager()
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS =  ['name']


    def get_full_name(self):
        return self.phone_number

    def get_short_name(self):
        return self.phone_number

    def __str__(self):
        return str(self.name) + '(' + str(self.phone_number) + ')'

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class OTP(models.Model):
    receiver = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=False, blank=False)
    sent_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return "%s has received otps: %s" % (self.receiver.phone_number, self.otp)
