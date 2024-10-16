from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User
from allauth.account.adapter import DefaultAccountAdapter

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    def validate(self, data):
        # Validate first_name and last_name
        print('validate ->', data)
        # Validate email field
        email = data.get('email')
        if not email:
            raise serializers.ValidationError({"email": "Email is required."})
        
        # Use Django's built-in validator to check if email is valid
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({"email": "Please enter a valid email address."})
        
         # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        
        return data

    def get_cleaned_data(self):
        print('print cleaned data',self.validated_data)
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data

    def save(self, request):
        print('serializer',request)
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        return user

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        print(data,'--adapter')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.save()
        return user

