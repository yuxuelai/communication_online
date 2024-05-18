import hashlib

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import User
import re


def custom_make_password(password):
    """
    自定义密码加密方法
    """
    # 去掉盐值
    # salt = "random_salt"
    # 将密码和 salt 拼接起来，然后计算其 SHA-256 散列值
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


def custom_check_password(raw_password, hashed_password):
    # 去掉盐值
    # salt = "random_salt"
    # 使用相同的哈希算法和盐值进行哈希
    # print("加密后的", hashlib.sha256(raw_password.encode('utf-8')).hexdigest())
    return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == hashed_password


# def check_password(raw_password, hashed_password):
#     return custom_check_password(raw_password, hashed_password)


class RegistrationSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repassword', "phone"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    """
    校验获取到的用户名是否符合验证规则
    """

    def validate_username(self, value):
        # 用户名必须是8-16位，支持中文、字母、下划线
        if not re.match(r'^[\w\u4e00-\u9fff]{8,16}$', value):
            raise serializers.ValidationError("用户名必须是8-16位，支持中文、字母、下划线")
        return value

    """
    校验获取到的密码是否符合验证规则
    """

    def validate_password(self, value):
        # 密码必须是8-16位，首字母大写，支持字母、数字、符号
        if not re.match(r'^[A-Z][A-Za-z0-9@#$%^&+=]{7,15}$', value):
            raise serializers.ValidationError("密码必须是8-16位，首字母大写，支持字母、数字、符号")
        return value

    """
    校验获取到的电话格式是否符合验证规则
    """

    def validate_phone(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("无效的手机号码")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号码已被注册")
        return value

    """
    校验二次确认密码是否一致
    """

    def validate(self, data):
        if data['password'] != data['repassword']:
            raise serializers.ValidationError("密码和确认密码不匹配")
        return data

    """
    验证没问题那么将获取的传入User中
    创建数据库对应的用户信息
    """

    def create(self, validated_data):
        validated_data.pop('repassword')
        user = User.objects.create_user(**validated_data)
        # print(user.password)
        return user


"""登录的验证器"""


class LoginSerializer(serializers.Serializer):
    username_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # print(username_or_phone)

    def validate(self, data):
        """
        先获取到前端表单传入的值
        """
        username_or_phone = data.get('username_or_phone')  # 从请求数据中获取 username_or_phone
        password = data.get('password')  # 从请求数据中获取 password
        """
        如果获取到的表单信息都不为空
        """
        if username_or_phone and password:
            # 那么检查输入的是否符合手机号的格式
            if re.match(r'^1[3-9]\d{9}$', username_or_phone):
                user = User.objects.filter(phone=username_or_phone).first()
                if user and check_password(password, user.password):
                    data['user'] = user
                else:
                    raise serializers.ValidationError("无效的手机号或密码")

            # 否则检查是否为用户名登录
            else:
                user = User.objects.filter(username=username_or_phone).first()

                # print(check_password(password, user.password), user.password, password)
                # 根据用户名查询如果user不为空 并且密码检查一致
                if user and check_password(password, user.password):
                    # 那么将用户放入data中
                    data['user'] = user
                else:
                    raise serializers.ValidationError("无效的用户名或密码")
        else:
            raise serializers.ValidationError("必须同时提供用户名或手机号和密码")
        # 最后返回数据data
        return data


"""
忘记密码的验证/判断器
"""


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        # 校验密码格式是否为 8-16位，首字母大写，可以包含中文，字符和字母
        if not re.match(r'^[A-Z][A-Za-z0-9@#$%^&+=]{7,15}$', value):
            raise serializers.ValidationError("密码格式错误 密码格式为 8-16位，首字母大写，可以包含中文，字符和字母")
        return value

    def validate(self, data):
        # print(bool(data.get('old_password')))
        if data.get('old_password'):
            # 如果有旧密码，则进行密码比对
            username = data.get('username')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            user = User.objects.filter(username=username).first()
            if user and check_password(old_password, user.password):
                if new_password != confirm_password:
                    raise serializers.ValidationError("两次输入的密码不一致")
                return data
            else:
                raise serializers.ValidationError("原密码错误或用户不存在")
        else:
            if data['new_password'] != data['confirm_password']:
                raise serializers.ValidationError("两次输入的密码不一致")
            return data

    def save(self, **kwargs):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']

        user = User.objects.get(username=username)
        # 重新设置密码
        user.set_password(new_password)
        user.save()
        return user


