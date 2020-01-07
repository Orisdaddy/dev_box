from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import json


class ResponseMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        status = response.status_code
        if 200 <= status < 300:
            content = response.content.decode()
            try:
                content = json.loads(content)
            except:return response
            if isinstance(content, dict):
                if content.get('code') and content.get('msg'):
                    return response
                else:
                    res = {
                        'code': 1000,
                        'msg': '操作成功',
                        'data': content
                    }
                    response.content = json.dumps(res, ensure_ascii=False).encode()
                    return response
            else:
                res = {
                    'code': 1000,
                    'msg': '操作成功',
                    'data': content
                }
                response.content = json.dumps(res, ensure_ascii=False).encode()
                print(response.content)
                return response
        else:
            return response
