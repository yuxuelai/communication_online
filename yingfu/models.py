from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import hashlib


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # 使用自定义的密码设置方法
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.CharField(max_length=50, verbose_name='邮箱')
    phone = models.CharField(verbose_name='手机号', max_length=20, blank=False)
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    age = models.IntegerField(default=0, verbose_name="年龄")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # def set_password(self, password):
    #     self.password = custom_make_password(password)

    def __str__(self):
        return self.username


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
    salt = "random_salt"
    return hashlib.sha256((raw_password + salt).encode('utf-8')).hexdigest() == hashed_password
