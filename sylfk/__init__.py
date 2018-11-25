from werkzeug.serving import run_simple


class SYLFk:

    # 实例化方法
    def __init__(self):
        self.host = '127.0.0.1' # 默认主机
        self.port = 8086 # 默认端口

    # 路由
    def dispatch_request(self):
        pass

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
    def __call__(self):
        pass


