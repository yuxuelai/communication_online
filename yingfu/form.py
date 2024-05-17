from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from pylint.checkers.typecheck import _

"""判断首字母是否大写"""


def validate_capital_initial(value):
    if not value or not value[0].isupper():
        raise ValidationError(_('密码设置必须以大写字母开始'))


"""使用django的forms编写 校验注册时的表单"""


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=8, max_length=16,
                               error_messages={'min_length': '用户名长度不能小于8字符',
                                               'max_length': '用户名长度不能大于16个字符'})

    password = forms.CharField(label='密码', widget=forms.PasswordInput(), min_length=8, max_length=16,
                               validators=[validate_capital_initial],
                               error_messages={'min_length': '密码长度不能小于8字符',
                                               'max_length': '密码长度不能大于16个字符'})

    repassword = forms.CharField(label='确认密码', widget=forms.PasswordInput(), min_length=8, max_length=16,
                                 error_messages={'min_length': '密码长度不能小于8个字符',
                                                 'max_length': '密码长度不能大于16个字符'})

    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')])
