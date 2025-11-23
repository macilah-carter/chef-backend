from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number']

class UserSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_role'] = self.user.role
        return data