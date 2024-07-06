from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from .exceptions import (
    AccountDisabledException,
    InvalidCredentialsException,
)
from .models import Address, Profile
from dj_rest_auth.serializers import LoginSerializer


User = get_user_model()

class UserRegistrationSerializer(RegisterSerializer):
    """
    Serializer for registering new users using email or phone number.
    """

    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='customer', write_only=True)

    def validate(self, data):
        email = data.get("email", None)

        if not (email):
            raise serializers.ValidationError(_("Enter an email ."))

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))

        return data

    def get_cleaned_data_extra(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "email": self.validated_data.get("email", ""),
            "role": self.validated_data.get("role", "customer"),
        }

    def create_extra(self, user, validated_data):
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.email = validated_data.get("email")
        user.role = validated_data.get("role", "customer")
        user.save()

    def custom_signup(self, request, user):
        self.create_extra(user, self.get_cleaned_data_extra())


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to login users with email or phone number.
    """

    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_email(self, email, password):
        user = None

        if email:
            user = authenticate(email=email, password=password)
        
        else:
            raise serializers.ValidationError(
                _("Enter  an email and password.")
            )

        return user

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = None

        user = self.validate_email( email=email, password=password)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        if email:
            email_address = user.emailaddress_set.filter(
                email=user.email, verified=True
            ).exists()
            if not email_address:
                raise serializers.ValidationError(_("E-mail is not verified."))

        

        validated_data["user"] = user
        return validated_data



class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        )


class AddressReadOnlySerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize Address model
    """

    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize User model
    """

    profile = ProfileSerializer(read_only=True)
    addresses = AddressReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "user_id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "profile",
            "addresses",
        )


class ShippingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type shipping

    For shipping address, automatically set address type to shipping
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "S"

        return representation


class BillingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type billing

    For billing address, automatically set address type to billing
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "B"

        return representation
    
