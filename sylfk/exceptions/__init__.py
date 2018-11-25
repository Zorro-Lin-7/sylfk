# 框架异常基类
class SYLFkException(Exception):
    def __init__(self, code='', message='Error'):
        self.code = code        # 异常编号
        self.message = message  # 异常信息

    def __str__(self):
        return self.message     # 当作为字符串使用时，返回异常信息


# “节点已存在”异常
class EndpointExistsError(SYLFkException):
    def __init__(self, message='Endpoint exists'):
        super(EndpointExistsError, self).__init__(message) # 此处的异常处理很简单，只是抛出一个消息


# “URL 已存在”异常
class URLExistsError（SYLEkException):
    def __init__(self, message='URL exists'):
        super(URLExistsError, self).__init__(message)
