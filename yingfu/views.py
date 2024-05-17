from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import JsonResponse, response, request
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from yingfu import models
from yingfu.form import UserForm

# Create your views here.

from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

"""
用户注册逻辑的编写
输入长度控制在8-16位 可以是中文,字母,下划线组成
如果后端校验与上述不符合的话 那么抛出信息给用户
请输入由中文,字母,下划线组成的 8-16位用户名/密码

"""


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取表单传递过来的数据
        registration_data = request.data
        # 对相关字段名的值进行校验
        serializer = RegistrationSerializer(data=registration_data)
        # 如果验证都成功
        if serializer.is_valid():
            # 使用save方法保存到数据库中
            serializer.save()
            # 返回提示信息给用户 提示注册成功
            return Response({'message': '注册成功！'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""

用户登录逻辑的编写
使用rest_framework中的serializer进行后端校验与上述不符合的话 
那么抛出提示信息给用户

"""


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取数据进行验证
        serializer = LoginSerializer(data=request.data)
        # 判断传递的相关字段是否有验证成功
        if serializer.is_valid():
            # 都成功的的话将user名取出来
            user = serializer.validated_data['user']
            print("user:", user)
            # 传入user名生成token返会给用户端
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
