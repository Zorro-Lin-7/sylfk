import os

root_path = os.getwcd()

directory_list = [
        'dbconnector',
        'exceptions',
        'helper',
        'route',
        'session',
        'template_engine',
        'view',
        'wsgi_adapter',
        ]

children = {'name': '__init__.py',
            'children': None,
            'type': 'file',
            }

# 目录结构
dir_map = [{
    'name': 'sylfk', # 框架名
    'children': [{
        'name': directory,
        'type': 'dir',
        'children': [children], # 用于子目录的创建，
        } for directory in directory_list] + [children],
    'type': 'dir',
    }]

# 创建文件夹或目录
def create(path, kind):
    if kind == 'dir':
        os.mkdir(path)
    else:
        open(path, 'w').close()

# 递归创建目录
def gen_project(parent_path, map_obj):
    for line in map_obj:
        path = os.path.join(parent_path, line['name'])
        create(path, line['type'])
        if line['children']: # 目录里创建子目录
            gen_project(path, line['children']) # 递归执行

def main():
    gen_project(root_path, dir_map)


if __name__ == '__main__':
    main()

