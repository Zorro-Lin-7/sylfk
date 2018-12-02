from sylfk import SYLFk


app = SYLFk()

'''
@app.route('/index', methods=['GET'])
def index():
    return '这是一个路由测试页面'
'''
# 等价于:

def index():
    return '这是一个路由测试页面'

index = app.route('/index', methods=['GET'])(index)
    # 等价于调用: .add_url_rule(url='index', f=index, 'route', methods=['GET'])

#          ⬇等价于
#       decorator(index)
#             ⬇
    # def decorator(f):
        # # 调用应用内部的 add_url_rule 添加规则
        # self.app.add_url_rule(url, f, 'route', **options) # [self.app] 已在上面定义，即应用本身
        # return f


@app.route('/test/js')
def test_js():
    return '<script src="/static/test.js"></script>'

# 等价于
'''
def test_js():
    return '<script src="/static/test.js"></script>'

test_js = app.route('/test/js')(test_js)
'''

app.run()


