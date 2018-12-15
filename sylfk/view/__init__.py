# 视图基类
class View:
    # 支持的请求方法
    methods = None

    # request-handler func 映射
    methods_meta = None

    # 视图处理函数调度入口
    def dispatch_request(self, request, *args, **option):
        raise NotImplementedError

    # 生成视图处理函数，参数 name 其实就是节点名
    @classmethod
    def get_func(cls, name):

        # 定义处理函数
        def func(*args, **kwargs):
            # 在处理函数内部实例化视图对象
            obj = func.view_class()

            # 通过视图对象调用【handler func 调度入口】，返回视图处理结果
            return obj.dispatch_request(*args, **kwargs)

        # 为handler func 绑定属性
        func.view_class = cls
        func.__name__ = name # 把外部的 name 参数作为自身的 __name__ 属性值，实现函数名与节点名的绑定
        func.__doc__ = cls.__doc__
        func.__module__ = cls.__module__
        func.methods = cls.methods

        # 返回这个处理函数
        return func

# 控制器类
class Controller:
    def __init__(self, name, url_map):
        self.url_map = url_map # 存放映射关系，一个元素为 Dict 的 List
        self.name = name

    def __name__(self):
        # 返回控制器名字
        return self.name


