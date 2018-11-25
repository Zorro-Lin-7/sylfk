from werkzeug.serving import run_simple
from werkzeug.wrappers import Response

from sylfk.wsgi_adapter import wsgi_app

# 指定URL下，处理请求的函数，将其封装为一个有type标识的数据结构
class ExecFunc:
    def __init__(self, func,func_type, **options):
        self.func = func           # 处理请求的函数
        self.options = options     # 附带参数
        self.func_type = func_type # 函数类型

class SYLFk:

    # 实例化方法
    def __init__(self):
        self.host = '127.0.0.1' # 默认主机
        self.port = 8086 # 默认端口

    # 路由
    def dispatch_request(self, request):
        status = 200 # HTTP 状态码，200表示请求成功

        # 定义响应报头的 Server属性
        headers = {
                'Server': 'Shiyanlou Framework'
                }

        # 回传实现 WSGI 规范的响应体给 WSGI 模块
        return Response('<h1>Hello, Framework</h1>', content_type='text/html', headers=headers, status=status)

    # 启动入口，这是使用框架实现应用后，应用启动的入口
    def run(self, host=None, port=None, **options):
        # 关键字参数的使用。 如果有参数进来且值不为空，则赋值
        for key, value in options.items():
            if value is not None:
                self.__setattr__(key, value)

        # 如果 host 不为 None，替换 self.host
        if host is not None:
            self.host = host

        if port is not None:
            self.port = port

        # 把框架本身，也就是应用本身和其它几个配置参数传给 werkzeug 的 run_simple
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    # WSGI调用框架入口的方法
    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)



