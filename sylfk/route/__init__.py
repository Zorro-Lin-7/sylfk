class Route:
    def __init__(self, app):
        # 传入应用（框架）实例
        self.app = app

    # 实现 call 方法
    def __call__(self, url, **options):
        # 如果 methods 参数没有定义，则初始化为“仅支持 GET 方法”
        if 'methods' not in options:
            options['methods'] = ['GET']

        def decorator(f):
            # 调用应用内部的 add_url_rule 添加规则
            self.app.add_url_rule(url, f, 'route', **options) # [self.app] 已在上面定义，即应用本身
            return f

        return decorator
