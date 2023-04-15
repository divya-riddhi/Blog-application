import logging
from django.shortcuts import render
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,logout
from rest_framework import permissions

logger = logging.getLogger(__name__)


#============================================#
#       User registeration starts            #                
#============================================#

class register(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    
    def post(self,request,format=None):
        try:
            data={}
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user_register = serializer.save()
                token,create=Token.objects.get_or_create(user=user_register)

                data={"username":user_register.username,
                      "email":user_register.email,
                      "token":token.key,
                      "status":"success",
                      "message":"Registration successfully completed"}
            else:
                data=serializer.errors
            return Response(data)
        except Exception as e:
            logger.error(f"User registration failed: {str(e)}")
            return Response({'status': 'error', 'message': 'User registration failed.'})

    
#============================================#
#       User registeration ends              #                
#============================================#

#============================================#
#          User login starts                 #                
#============================================#
    
class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'username': user.username,
                    'email': user.email,
                    'token': token.key,
                    'status': 'success',
                    'message': 'User login successfully.'
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid login credentials'
                })
        except Exception as e:
            logger.error(f"User login failed: {str(e)}")
            return Response({'status': 'error', 'message': 'User login failed.'})

#============================================#
#          User login ends                   #                
#============================================#


#============================================#
#          User logout starts                 #                
#============================================#

class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({'status': 'success', 'message': 'User logged out successfully.'})
        except Exception as e:
            logger.error(f"User logout failed: {str(e)}")
            return Response({'status': 'error', 'message': 'User logout failed.'})
    
#============================================#
#          User logout ends                  #                
#============================================#
    



    





            


