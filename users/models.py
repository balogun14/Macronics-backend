from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, role="customer"):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password, role="admin")
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_ADMIN = "admin"
    ROLE_VENDOR = "vendor"
    ROLE_CUSTOMER = "customer"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_VENDOR, "Vendor"),
        (ROLE_CUSTOMER, "Customer"),
    )

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    @property
    def is_vendor(self):
        return self.role == self.ROLE_VENDOR

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.role == self.ROLE_ADMIN
    
    def get_full_name(self):
        return self.first_name + " "+self.last_name



class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", blank=True)
    bio = models.CharField(max_length=250, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()


class Address(models.Model):
    # Address options
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, "billing"), (SHIPPING, "shipping"))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()

