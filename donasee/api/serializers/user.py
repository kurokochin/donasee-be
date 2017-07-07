from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from donasee.apps.accounts.models import UserProfile


def field_length(fieldname):
    field = next(field for field in User._meta.fields if field.name == fieldname)
    return field.max_length


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=field_length('email'), required=True)
    password = serializers.CharField(max_length=field_length('password'), required=True)
    community_name = serializers.CharField(max_length=256, required=True)
    admin_name = serializers.CharField(max_length=256, required=True)
    docs_link = serializers.URLField()

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        community_name = attrs['community_name']
        admin_name = attrs['admin_name']
        docs_link = attrs['docs_link']

        email = self.normalize_email(email)
        if not email:
            raise serializers.ValidationError(
                'Invalid email provided')

        if not community_name:
            raise serializers.ValidationError(
                'Invalid community/church name provided')

        if not admin_name:
            raise serializers.ValidationError(
                'Invalid admin name provided')

        if not docs_link:
            raise serializers.ValidationError(
                'Invalid docs link provided')

        try:
            if User.objects.get(email=email):
                raise serializers.ValidationError(
                    'A user with that email address already exists')
        except User.DoesNotExist:
            pass

        try:
            password_validation.validate_password(password)
        except serializers.ValidationError:
            raise serializers.ValidationError(
                'Invalid password provided')

        return attrs

    def create(self, validated_data):
        email = validated_data['email'].lower()  # set to lower
        username = email.lower()
        password = validated_data['password']

        user, created = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)

        user.save()

        # create userprofile
        try:
            community_name = validated_data['community_name']
            admin_name = validated_data['admin_name']
            docs_link = validated_data['docs_link']
            UserProfile.objects.create(user=user, community_name=community_name, admin_name=admin_name,
                                       docs_link=docs_link)
        except User.DoesNotExist:
            print 'User not found'
        except Exception as e:
            print 'User registered, UserProfile failed to save', e

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=field_length('email'), required=True)
    password = serializers.CharField(max_length=field_length('password'), required=True)

    def authenticate(self, email=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                username = user.get_username()
                return authenticate(username=username, password=password)
        except User.DoesNotExist:
            return None

    def validate(self, attrs):
        email = attrs['email'].lower()  # force lowercase email
        user = self.authenticate(email=email,
                                 password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Wrong email or password')
        elif not user.is_active:
            raise serializers.ValidationError(
                'Can not log in as inactive user')
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'userprofile')
