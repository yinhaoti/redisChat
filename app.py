from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.todo import Todo
from models.user import User


app = Flask(__name__)
manager = Manager(app)

# 自定义过滤器
# 过滤器的名字是参数 xcxx
# str | xcxx
@app.template_filter('format_time')
def format_time(t):
    import time
    format = '%Y-%m-%d %l:%M %p'
    # print(type(t), t)
    value = time.localtime(int(t))
    dt = time.strftime(format, value)
    return dt

def configured_app():
    # 这一句是套路, 不加会有 warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # secret key 和 数据库配置都放在 config.py 里面
    import config
    app.secret_key = config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    # 初始化 db
    db.init_app(app)
    # 注册路由
    register_routes(app)
    # 配置日志
    configure_log(app)
    # 返回配置好的 app 实例
    return app


def configure_log(app):
    # 设置 log, 否则输出会被 gunicorn 吃掉
    # 但是如果 app 是 debug 模式的话, 则不用这么搞
    if not app.debug:
        import logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def register_routes(app):
    """
    在这个函数里面 import 并注册蓝图
    """
    from routes.todo import main as routes_todo
    app.register_blueprint(routes_todo, url_prefix='/todo')

    from routes.redisChat import main as routes_redisChat
    app.register_blueprint(routes_redisChat, url_prefix='')


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


if __name__ == '__main__':
    configure_manager()
    configured_app()
    manager.run()
