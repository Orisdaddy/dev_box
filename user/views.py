
from common.view import ResView
from user.jwt.serializer import LoginSerializer

from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from Crypto.Cipher import AES
from binascii import b2a_hex
import random
import time
import json
import base64
import datetime

AES_KEY = 'as56hr1jko_saoqp'
AES_IV = 'asw56hxr8q1jfkoo'


def response_payload(token, user=None):
    return {
        'token': token,
        'user': user.username
    }


class Login(JSONWebTokenAPIView, ResView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = response_payload(token, user)
            response = self.success(msg='登录成功', data=response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        error = serializer.errors.get('non_field_errors')[0]
        return self.error(msg=error)


class Captcha(ResView):
    def get_chars_str(self):
        _letter_cases = "abcdefghjkmnpqrstuvwxy"
        _upper_cases = _letter_cases.upper()
        _numbers = ''.join(map(str, range(3, 10)))
        init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
        return init_chars

    def create_validate_code(self, size,
                             chars,
                             mode="RGB",
                             bg_color=(255, 255, 255),
                             fg_color=(0, 0, 255),
                             font_size=18,
                             font_type="C:\Windows\Fonts\Arial.ttf",
                             length=4,
                             draw_lines=True,
                             n_line=(1, 2),
                             draw_points=True,
                             point_chance=1):
        """
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        """

        width, height = size  # 宽高
        # 创建图形
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)  # 创建画笔

        def get_chars():
            """生成给定长度的字符串，返回列表格式"""
            return random.sample(chars, length)

        def create_lines():
            """绘制干扰线"""
            line_num = random.randint(*n_line)  # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                # 结束点
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            """绘制干扰点"""
            chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            """绘制验证码字符"""
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开
            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                      strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

        return img, strs

    def get(self, request):
        io = BytesIO()
        img, code = self.create_validate_code((120, 30), self.get_chars_str(), font_type=r"user\ttf\monaco.ttf")
        img.save(io, 'png')
        b64img = base64.b64encode(io.getvalue())

        t = time.time() + 300
        capt_res = json.dumps({
            'code': code,
            'time': t
        })
        if len(capt_res.encode('utf-8')) % 16:
            add = 16 - (len(capt_res.encode('utf-8')) % 16)
        else:
            add = 0
        capt_res = capt_res + ('\0' * add)
        key = AES_KEY.encode()
        iv = AES_IV.encode()
        cipher = AES.new(key, AES.MODE_CFB, iv)
        capt_code = b2a_hex(cipher.encrypt(capt_res.encode()))
        data = {
            'img': b64img,
            'captcha_code': capt_code
        }
        return self.success(data=data)

