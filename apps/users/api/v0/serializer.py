from rest_framework import serializers
from apps.users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'phone_number', 'email', 'image', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Parollar mos emas!"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # confirm saqlash shart emas
        user = User.objects.create_user(
            fullname=validated_data['fullname'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email manzilingizni kiriting")
    password = serializers.CharField(write_only=True, help_text="Parolingizni kiriting")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh tokenni kiriting", default="")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'phone_number', 'image']
        extra_kwargs = {
            'image': { 'help_text':'image kiriting', 'required': False, 'default': ''},
            'fullname': { 'help_text':'fullname kiriting','required': False, 'default': ''},
            'phone_number': { 'help_text':'phone_number kiriting','required': False, 'default': ''}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullname", "email", "phone_number", "image"]