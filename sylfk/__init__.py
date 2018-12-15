from werkzeug.serving import run_simple
from werkzeug.wrappers import Response

from sylfk.wsgi_adapter import wsgi_app
import sylfk.exceptions as exceptions
from sylfk.helper import parse_static_key
from sylfk.route import Route
import os


# 定义常见服务异常的响应体
ERROR_MAP = {
        '401': Response('<h1>401 Unknown or unsupported method</h1>', content_type='text/html; charset=UTF-8', status=401),
        '404': Response('<h1>404 Source Not Found</h1>', content_type='text/html; charset=UTF-8', status=404),
        '503': Response('<h1>503 Unknown Function Type</h1>', content_type='text/html; charset=UTF-8', status=503),
        }

# 定义文件类型
TYPE_MAP = {
        'css': 'text/css',
        'js': 'text/js',
        'png': 'image/png',
        'jpg': 'image/jpg',
        'jpeg': 'image/jpeg',
        }

# 指定URL下，处理请求的函数，将其封装为一个有type标识的数据结构
class ExecFunc:
    def __init__(self, func, func_type, **options):
        self.func = func           # 处理请求的函数
        self.options = options     # 附带参数
        self.func_type = func_type # 函数类型

class SYLFk:

    # 实例化方法
    def __init__(self, static_folder='static'):
        self.host = '127.0.0.1' # 默认主机
        self.port = 8086 # 默认端口
        self.url_map = {} # 存放 URL 与 Endpoint的映射
        self.static_map = {} # 存放 URL 与 静态资源的映射
        self.function_map = {} # 存放 Endpoint 与请求处理函数的映射
        self.static_folder = static_folder # 静态资源本地存放路径，默认放在app所在目录的 static 文件夹
        self.route = Route(self) # 路由装饰器

    # 静态资源的路由，用来寻找匹配的URL 并返回对应类型和文件内容封装成的响应体，找不到就返回404页
    def dispatch_static(self, static_path):
        # 判断资源文件是否在静态资源规则中，如果不存在，返回 404 状态页
        if os.path.exists(static_path):
            # 获取资源文件后缀
            key = parse_static_key(static_path)

            # 获取文件类型
            doc_type = TYPE_MAP.get(key, 'text/plain')

            # 获取文件内容
            with open(static_path, 'rb') as f:
                rep = f.read()

            # 封装并返回响应体
            return Response(rep, content_type=doc_type)
        else:
            # 返回的响应体为 404 页面
            return ERROR_MAP['404']


    # 路由
    def dispatch_request(self, request):
        # 去掉 URl 中域名部分，即从 http://xxx.com/path/file?xx=xx 中提取 path/file 部分
        url = "/" + "/".join(request.url.split("/")[3:]).split("?")[0]

        # 通过URL 寻找节点名
        if url.find(self.static_folder) == 1 and url.index(self.static_folder) == 1:
            # 如果 URL 以静态资源文件夹名为首目录，则资源为静态资源
            endpoint = 'static'
            url = url[1:]
        else:
            # 若不以static 为首，则从 URL 与节点的映射表中获取节点
            endpoint = self.url_map.get(url, None)

        # 定义响应报头的, Server 参数的值表示运行的服务名，通常有 IIS, Apache, Tomact, Nginx等，这里自定义为SYL Web 0.1
        headers = {
                'Server': 'SYL Web 0.1'
                }

        # 如果节点为空 返回404
        if endpoint is None:
            return ERROR_MAP['404']

        # 获取节点对应的执行函数
        exec_function = self.function_map[endpoint]

        # 判断执行函数类型
        if exec_function.func_type == 'route':
            """路由处理"""

            # 判断请求方法是否支持
            if request.method in exec_function.options.get('methods'):
                """路由处理结果"""

                # 判断路由的执行函数是否需要请求体进行内部处理
                argcount = exec_function.func.__code__.co_argcount

                if argcount > 0:
                    # 需要附带请求体进行结果处理
                    rep = exec_function.func(request)
                else:
                    # 不需要附带请求体进行结果处理
                    rep = exec_function.func()

            else:
                """未知请求方法"""

                # 返回401 错钱响应体
                return ERROR_MAP['401']

        elif exec_function.func_type == 'view':
            """ 视图处理结果 """

            # 所有视图处理函数都需要附带请求体来获取处理结果
            rep = exec_function.func(request)

        elif exec_function.func_type == 'static':
            """ 静态逻辑处理 """

            # 静态资源返回的是一个预先封装好的响应体，所以直接返回
            return exec_function.func(url)
        else:
            """ 未知类型处理  """

            # 返回 503错误响应体
            return ERROR_MAP['503']

        # 定义 200 状态码表示成功
        status = 200

        # 定义响应体类型
        content_type = 'text/html'

        # 返回响应体
        return Response(rep, content_type='%s; charset=UTF-8' % content_type, headers=headers, status=status)
#        # 回传实现 WSGI 规范的响应体给 WSGI 模块
#        return Response('<h1>Hello, Framework</h1>', content_type='text/html', headers=headers, status=status)

    # 添加视图规则
    def bind_view(self, url, view_class, endpoint): # view_class是类，作为参数传入
        self.add_url_rule(url, func=view_class.get_func(endpoint), func_type='view') # func参数需要一个get_view方法，它是类方法，不是实例方法；且会把节点名作为参数传进去作为函数名——调用add_url_rule时是没有为endpoint参数赋值的，默认为None，此时节点名即函数名。那么，get_view 返回的应该是一个动态生成的函数

    # 控制器加载
    def load_controller(self, controller):

        # 获取控制器名字
        name = controller.__name__()

        # 遍历控制器的 `url_map`成员
        for rule in controller.url_map:
            # 绑定 URL 与试图对象，最后的节点名称格式为 `控制器名` + “.” + 定义的节点名
            self.bind_view(rule['url'], rule['view'], name + '.' + rule['endpoint'])
    # 添加路由规则
    def add_url_rule(self, url, func, func_type, endpoint=None, **options):

        # 如果节点未命名，使用处理函数的名字
        if endpoint is None:
            endpoint = func.__name__

        # 如果 URL 已存在，抛出异常
        if url in self.url_map:
            raise exceptions.URLExistsError

        # 如果类型不是静态资源，并且节点已存在，则抛出“节点已存在”异常
        if endpoint in self.function_map and func_type != 'static':
            raise exceptions.EndpointExistsError

        # 添加 URL 与 节点的映射
        self.url_map[url] = endpoint

        # 添加 节点 与 request处理函数 的映射
        self.function_map[endpoint] = ExecFunc(func, func_type, **options)

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

        # 映射static resouce handler，所有静态资源相关的节点函数都命名为static，并且绑定处理方法dispatch_static
        self.function_map['static'] = ExecFunc(func=self.dispatch_static, func_type='static')

        # 把框架本身，也就是应用本身和其它几个配置参数传给 werkzeug 的 run_simple
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    # WSGI调用框架入口的方法
    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)



