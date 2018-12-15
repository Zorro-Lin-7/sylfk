from sylfk import SYLFk
from sylfk.view import Controller

from core.base_view import BaseView


class Index(BaseView):
    def get(self, request):
        return '你好，实验楼'


class Test(Index):
    def post(self, request):
        return '这是一个 POST请求'


app = SYLFk()

syl_url_map = [
        {
            'url': '/shiyanlou',
            'view': Index,
            'endpoint': 'index',
            },
        {
            'url': '/test',
            'view': Test,
            'endpoint': 'test',
            }
        ]

index_controller = Controller('index', syl_url_map)
app.load_controller(index_controller)

#'''
#@app.route('/index', methods=['GET'])
#def index():
#    return '这是一个路由测试页面'
#'''
## 等价于:
#
#def index():
#    return '这是一个路由测试页面'
#
#index = app.route('/index', methods=['GET'])(index)
#    # 等价于调用: .add_url_rule(url='index', f=index, 'route', methods=['GET'])
#
##          ⬇等价于
##       decorator(index)
##             ⬇
#    # def decorator(f):
#        # # 调用应用内部的 add_url_rule 添加规则
#        # self.app.add_url_rule(url, f, 'route', **options) # [self.app] 已在上面定义，即应用本身
#        # return f
#
#
#@app.route('/test/js')
#def test_js():
#    return '<script src="/static/test.js"></script>'
#
## 等价于
#'''
#def test_js():
#    return '<script src="/static/test.js"></script>'
#
#test_js = app.route('/test/js')(test_js)
#'''

app.run()


