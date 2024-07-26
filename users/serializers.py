from django.contrib.auth.hashers import make_password
from users.models import Owner, AdminStaff, RetailStaff
from rest_framework import serializers
import logging
import bleach

log = logging.getLogger('main')

class OwnerSerializer(serializers.ModelSerializer):
    """
    This class defines the serializer for the Owner model.
    """
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = Owner
        fields = '__all__'
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        """
        Validates request data.
        """
        log.info(f'validating owner data from request')
        if data['password'] != data['confirm_password']:
            log.error(f'validation of owner data from request failed because password and confirm_passwords dont match')
            raise serializers.ValidationError("Passwords do not match.")
        
        username = data.get('username', None)
        if username is not None:
            username = bleach.clean(username, strip=True)
            if len(username) > 50:
                log.error(f'validation of owner data from request failed because username exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        first_name = data.get('first_name', None)
        if first_name is not None:
            first_name = bleach.clean(first_name, strip=True)
            if len(first_name) > 50:
                log.error(f'validation of owner data from request failed because first_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        last_name = data.get('last_name', None)
        if last_name is not None:
            last_name = bleach.clean(last_name, strip=True)
            if len(last_name) > 50:
                log.error(f'validation of owner data from request failed because last_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        middle_name = data.get('middle_name', None)
        if middle_name is not None:    
            middle_name = bleach.clean(middle_name, strip=True)
            if len(middle_name) > 50:
                log.error(f'validation of owner data from request failed because middle_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        phone = data.get('phone', None)
        if phone is not None:
            phone = bleach.clean(phone, strip=True)
            if len(phone) > 14:
                log.error(f'validation of owner data from request failed because phone exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        gender = data.get('gender', None)
        if gender is not None:
            gender = bleach.clean(gender, strip=True)
            if len(gender) > 50:
                log.error(f'validation of owner data from request failed because gender exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        email = data.get('email', None)
        if email is not None:
            email = bleach.clean(email, strip=True)
        
        password = data.get('password', None)
        if password is not None:
            password = bleach.clean(password, strip=True)

        if username != data.get('username', None) or first_name != data.get('first_name', None) or last_name != data.get('last_name', None) or middle_name != data.get('middle_name', None) or phone != data.get('phone', None) or email != data.get('email', None) or gender != data.get('gender', None) or password != data.get('password', None):
            log.error(f'validation of owner data from request failed because a field is missing')
            raise serializers.ValidationError("You have entered invalid characters.")
        
        log.info(f'owner data has been validated')
        return data

    def create(self, validated_data):
        """
        creates a new owner and hashes the password.
        """
        log.info(f'creating a new owner using the request data via the owner_serializer class')
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data.get('password'))
        log.info(f'new owner has been created successfully via the owner_serializer class')
        return super(OwnerSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing owner and hashes the password.
        """
        log.info(f'updating an existing owner using the request data via the owner_serializer class')
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        log.info(f'existing owner has been updated successfully via the owner_serializer class')
        return super(OwnerSerializer, self).update(instance, validated_data)

class AdminSerializer(serializers.ModelSerializer):
    """
    This class defines the serializer for the admin_staff model.
    """
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = AdminStaff
        fields = '__all__'
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        """
        Validates request data.
        """
        log.info(f'validating admin_staff data from request')
        if data['password'] != data['confirm_password']:
            log.error(f'validation of admin_staff data from request failed because password and confirm_passwords dont match')
            raise serializers.ValidationError("Passwords do not match.")
        
        username = data.get('username', None)
        if username is not None:
            username = bleach.clean(username, strip=True)
            if len(username) > 50:
                log.error(f'validation of admin_staff data from request failed because username exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        first_name = data.get('first_name', None)
        if first_name is not None:
            first_name = bleach.clean(first_name, strip=True)
            if len(first_name) > 50:
                log.error(f'validation of admin_staff data from request failed because first_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        last_name = data.get('last_name', None)
        if last_name is not None:
            last_name = bleach.clean(last_name, strip=True)
            if len(last_name) > 50:
                log.error(f'validation of admin_staff data from request failed because last_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        middle_name = data.get('middle_name', None)
        if middle_name is not None:    
            middle_name = bleach.clean(middle_name, strip=True)
            if len(middle_name) > 50:
                log.error(f'validation of admin_staff data from request failed because middle_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        phone = data.get('phone', None)
        if phone is not None:
            phone = bleach.clean(phone, strip=True)
            if len(phone) > 14:
                log.error(f'validation of admin_staff data from request failed because phone exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        gender = data.get('gender', None)
        if gender is not None:
            gender = bleach.clean(gender, strip=True)
            if len(gender) > 50:
                log.error(f'validation of admin_staff data from request failed because gender exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        email = data.get('email', None)
        if email is not None:
            email = bleach.clean(email, strip=True)
        
        password = data.get('password', None)
        if password is not None:
            password = bleach.clean(password, strip=True)

        if username != data.get('username', None) or first_name != data.get('first_name', None) or last_name != data.get('last_name', None) or middle_name != data.get('middle_name', None) or phone != data.get('phone', None) or email != data.get('email', None) or gender != data.get('gender', None) or password != data.get('password', None):
            log.error(f'validation of admin_staff data from request failed because a field is missing')
            raise serializers.ValidationError("You have entered invalid characters.")
        
        log.info(f'admin_staff data has been validated')
        return data

    def create(self, validated_data):
        """
        creates a new admin_staff and hashes the password.
        """
        log.info(f'creating a new admin_staff using the request data via the admin_serializer class')
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data.get('password'))
        log.info(f'new admin_staff has been created successfully via the admin_serializer class')
        return super(AdminSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing admin and hashes the password.
        """
        log.info(f'updating an existing admin_staff using the request data via the admin_serializer class')
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        log.info(f'existing admin_staff has been updated successfully via the admin_serializer class')
        return super(AdminSerializer, self).update(instance, validated_data)

class RetailSerializer(serializers.ModelSerializer):
    """
    This class defines the serializer for the retail_staff model.
    """
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = RetailStaff
        fields = '__all__'
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        """
        Validates request data.
        """
        log.info(f'validating retail_staff data from request')
        if data['password'] != data['confirm_password']:
            log.error(f'validation of retail_staff data from request failed because password and confirm_passwords dont match')
            raise serializers.ValidationError("Passwords do not match.")
        
        username = data.get('username', None)
        if username is not None:
            username = bleach.clean(username, strip=True)
            if len(username) > 50:
                log.error(f'validation of retail_staff data from request failed because username exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        first_name = data.get('first_name', None)
        if first_name is not None:
            first_name = bleach.clean(first_name, strip=True)
            if len(first_name) > 50:
                log.error(f'validation of retail_staff data from request failed because first_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        last_name = data.get('last_name', None)
        if last_name is not None:
            last_name = bleach.clean(last_name, strip=True)
            if len(last_name) > 50:
                log.error(f'validation of retail_staff data from request failed because last_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        middle_name = data.get('middle_name', None)
        if middle_name is not None:    
            middle_name = bleach.clean(middle_name, strip=True)
            if len(middle_name) > 50:
                log.error(f'validation of retail_staff data from request failed because middle_name exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        phone = data.get('phone', None)
        if phone is not None:
            phone = bleach.clean(phone, strip=True)
            if len(phone) > 14:
                log.error(f'validation of retail_staff data from request failed because phone exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        gender = data.get('gender', None)
        if gender is not None:
            gender = bleach.clean(gender, strip=True)
            if len(gender) > 50:
                log.error(f'validation of retail_staff data from request failed because gender exceeded the limit')
                raise serializers.ValidationError("You have exceeded the allowed characters")   

        email = data.get('email', None)
        if email is not None:
            email = bleach.clean(email, strip=True)
        
        password = data.get('password', None)
        if password is not None:
            password = bleach.clean(password, strip=True)

        if username != data.get('username', None) or first_name != data.get('first_name', None) or last_name != data.get('last_name', None) or middle_name != data.get('middle_name', None) or phone != data.get('phone', None) or email != data.get('email', None) or gender != data.get('gender', None) or password != data.get('password', None):
            log.error(f'validation of retail_staff data from request failed because a field is missing')
            raise serializers.ValidationError("You have entered invalid characters.")
        
        log.info(f'retail_staff data has been validated')
        return data

    def create(self, validated_data):
        """
        creates a new retail_staff and hashes the password.
        """
        log.info(f'creating a new retail_staff using the request data via the retail_serializer class')
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data.get('password'))
        log.info(f'new retail_staff has been created successfully via the retail_serializer class')
        return super(RetailSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        """
        updates an existing reatail_staff and hashes the password.
        """
        log.info(f'updating an existing retail_staff using the request data via the retail_serializer class')
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        log.info(f'existing retail_staff has been updated successfully via the retail_serializer class')
        return super(RetailSerializer, self).update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    This class handles the serialization for user login
    """
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = [
            'email',
            'password'
        ]
    
    def validate(self, data):
        """
        Validates the username and password fields.
        """
        log.info(f'validating login request data within the user_login_serializer class')
        email = data.get('email', None)
        password = data.get('password', None)

        log.info(f'validating login request data (email)')
        if email is None:
            log.error(f'validation of login request data failed because there was no email input')
            raise serializers.ValidationError("An Email is required to login.")

        log.info(f'validating login request data (password)')
        if password is None:
            log.error(f'validation of login request data failed because there was no password input')
            raise serializers.ValidationError("A Password is required to login.")

        log.info(f'login request data has been validated successfully')
        return data
    

