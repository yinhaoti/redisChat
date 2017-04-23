from models.user import User
from routes import *
from utillity import random_string, xfrs_dict
main = Blueprint('user', __name__)

Model = User



@main.route('/')
def index():
    ms = Model.query.all()
    xfrs = random_string()
    xfrs_dict[xfrs] = 0
    if 'username' in session:
        return render_template('user/index.html', xfrs=xfrs, username=session['username'], user_list=ms)
    return redirect(url_for('.login'))


@main.route('/login', methods=['POST', 'GET'])
def login():
    error = ""

    if request.method == 'POST':
        form = request.form
        u = User(form)
        # print(form)
        if u.valid_login():
            print('login success')
            # 把id写入session
            # 这个session是flask自带的
            session['username'] = u.username
            return redirect(url_for('message.index'))
        else:
            error = 'login fail'

    return render_template('user/login.html', result=error)


@main.route('/logout/<int:id>')
def logout(id):
    ms = User.find_by_ID(id)
    # session清空
    if ms.username == session['username']:
        session.pop('username', None)

    return redirect(url_for('message.index'))


@main.route('/register', methods=['POST', 'GET'])
def register():
    error = " "

    if request.method == 'POST':
        form = request.form
        u = User(form)
        # print(form)
        valid, msgs = u.valid_register()
        if valid:
            print('register success')
            u.save()
            return redirect(url_for('.login'))
        else:
            print('register fail:', msgs)
            error = msgs

    return render_template('user/register.html', error=error)


@main.route('/edit/<int:id>')
def edit(id):
    m = Model.query.get(id)
    return render_template('user/edit.html', user=m)


# 处理数据返回重定向
@main.route('/add', methods=['POST'])
def add():
    form = request.form
    xfrs = form.get('xfrs')

    if xfrs in xfrs_dict:
        xfrs_dict.pop(xfrs)
        Model.new(form)
        return redirect(url_for('.index'))
    else:
        return 'ERROR 非法链接'


@main.route('/update/<id>', methods=['POST'])
def update(id):
    form = request.form
    Model.update(id, form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
def delete(id):
    r = request.args
    xfrs = r.get('code')
    if xfrs in xfrs_dict:
        xfrs_dict.pop(xfrs)
        ms = User.find_by_ID(id)
        # session清空
        if ms.username == session['username']:
            session.pop('username', None)

        Model.delete_by_ID(id)

        return redirect(url_for('.index'))
    else:
        return 'ERROR 非法链接'
