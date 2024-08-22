from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from authentication.models import CustomUser




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user']={
            'userId':user.id,
            'first_name':user.first_name,
            'email':user.email, 
         
        }
        return token
    

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['email','mobile_number','first_name','last_name','password']

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


