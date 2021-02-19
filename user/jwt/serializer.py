import time
import json

from user import views
from Crypto.Cipher import AES
from binascii import a2b_hex

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.exceptions import ValidationError


class LoginSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        captcha = self.initial_data.get('captcha')
        captcha_text = self.initial_data.get('captcha_code')

        key = views.AES_KEY.encode()
        iv = views.AES_IV.encode()
        cryptos = AES.new(key, AES.MODE_CFB, iv)
        text = cryptos.decrypt(a2b_hex(captcha_text))
        res = json.loads(text.strip(b'\x00'))

        if captcha.upper() != res.get('code').upper():
            raise ValidationError('验证码错误')
        elif time.time() > res.get('time'):
            raise ValidationError('验证码已失效')
        return super().validate(attrs)
