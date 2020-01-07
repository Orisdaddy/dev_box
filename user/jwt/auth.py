from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTTokenAuth(JSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        if request.method == 'GET':
            token = request.GET.get('token')
        else:
            token = request.data.get('token')
        if token:
            return token
        else:
            raise AuthenticationFailed('缺少认证token')

