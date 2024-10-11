from rest_framework import serializers
from . models import Employee, Team
from  django.contrib.auth.models import User
from django.contrib.auth import authenticate
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name']
class EmployeeSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 1
        
    def validate(self, data):
        spl_char = '[@_{!#$%^&*()<>?/\|}{~:}]'
        if any(c in spl_char for c in data['name']):
            raise serializers.ValidationError('name should not contain special characters')
        if data['age'] < 18:
            raise serializers.ValidationError('age should be greater than 18')
        
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User    
        fields = ['username', 'email', 'password']
    
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                return serializers.ValidationError('username already exists')
        
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                return serializers.ValidationError('email already exists')
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        
        def validate(self, data):
            user = authenticate(**data) 
            return user
       