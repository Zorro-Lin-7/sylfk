from sylfk.view import View


class BaseView(View):
    # 定义支持的请求方法，默认支持 GET 和 POST 方法
    methods = ['GET', 'POST']

    # 处理 POST请求 的函数
    def post(self, request, *args, **options):
        pass

    # 处理 GET请求 的函数
    def get(self, request, *args, **options):
        pass

    def dispatch_request(self, request, *args, **options):
        # 定义请求方法与处理函数的映射
        methods_meta = {
                'GET': self.get,
                'POST': self.post,
                }

        # 判断该view 是否支持所请求的方法
        if request.method in methods_meta:
            return methods_meta[request.method](request, *args, **options)
        else:
            return '<h1>Unknown or unsupported require method</h1>'
