from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import BlogPost,Comment

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=["username","password","email","confirm_password"]

    def save(self):
        user_reg=User(email=self.validated_data['email'],
                      username=self.validated_data['username'])
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password!=confirm_password:
            raise serializers.ValidationError({'password':"Password does not match"})
        
        user_reg.set_password(password)
        user_reg.save()
        return user_reg


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'created_at','updated_at')
        read_only_fields = ('id', 'created_at','updated_at')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'user', 'blog_post')


 
