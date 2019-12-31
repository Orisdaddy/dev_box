from rest_framework.views import APIView
from rest_framework.response import Response


class ResView(APIView):
    @staticmethod
    def error(code=1001, msg='error', data=None, **kwargs):
        res = {
            'code': code,
            'msg': msg,
        }
        if data:
            res['data'] = data
        return Response(res, **kwargs)

    @staticmethod
    def success(msg='success', data=None, **kwargs):
        res = {
            'code': 1000,
            'msg': msg,
        }
        if data:
            res['data'] = data
        return Response(res, **kwargs)

