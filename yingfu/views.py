# Create your views here.
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, ResetPasswordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

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


"""
忘记密码的编写
"""


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '密码重置成功'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
验证token是否有效
同时验证AccessToken和RefreshToken
"""


class TokenVerifyView(APIView):
    def post(self, request, *args, **kwargs):

        token = request.data.get("token", None)
        token_type = request.data.get('token_type', 'access')

        if token is None:
            return Response({"detail": "请传入需要验证的token"})

        try:
            if token_type == "access":
                # print(AccessToken(token).lifetime)
                AccessToken(token)
                return Response({"detail": "AccessToken 有效"}, status=status.HTTP_200_OK)
            elif token_type == "refresh":
                # print(RefreshToken(token).lifetime)
                RefreshToken(token)
                return Response({"detail": "RefreshToken 有效"}, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "无效token"}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({"detail": "无效token或者token已经过期了"}, status=status.HTTP_400_BAD_REQUEST)


