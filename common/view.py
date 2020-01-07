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


class DataViews(APIView):
    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)
            request = self.change_data(request)
            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def change_data(self, request):
        if request.method == 'GET':
            data = request.GET.get('data')
        else:
            data = request.data.pop('data', None)
            request.data.pop('token')
        if data:
            for k, v in data.items():
                request.data[k] = v

        return request


