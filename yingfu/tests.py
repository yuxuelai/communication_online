from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase

# Create your tests here.


import hashlib


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
    return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == hashed_password

list1 = []
# 示例用法
password = "Absdgjh@"
hashed_password = custom_make_password(password)
print("Hashed Password:", hashed_password)
list1.append(hashed_password)

print(list1[0])
# 验证密码
is_valid = custom_check_password(password, list1[0])
print("Is Valid:", is_valid)




encode_password = make_password(password)

result = check_password(password,encode_password)
print("asdiasgbdiua",result)
