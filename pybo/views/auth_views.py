import functools

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

# /auth/라는 URL 접두어로 시작하는 URL이 호출되면 auth_views.py 파일의 함수들이 호출될 수 있도록 블루프린트 auth를 추가
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 회원가입을 위한 /signup/ URL과 연결된 signup 함수를 생성
# signup 함수는 POST 방식 요청에는 계정 등록을, GET 방식 요청에는 계정 등록을 하는 템플릿을 렌더링하도록 구현
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 계정 등록을 할 때 username으로 데이터를 조회해서 ‘이미 등록된 사용자’인지를 확인
        # 동명이인 처리를 위해 이게 맞나.. 이메일이 맞지 않나.
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        # generate_password_hash 함수로 암호화하여 저장
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

# --------------------------------- [edit] ---------------------------------- #
# 라우트 URL인 /login/에 매핑되는 login 함수를 생성
# login 함수는 signup 함수와 비슷한 패턴
# POST 방식 요청에는 로그인을 수행하고, GET 방식 요청에는 로그인 템플릿을 렌더링한다.
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        # 사용자도 존재하고 비밀번호도 올바르다면 플라스크 세션(session)에 키와 키값을 저장한다.
        # 키에는 'user_id'라는 문자열을 저장하고 키값은 데이터베이스에서 조회된 사용자의 id값을 저장한다.
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)
# --------------------------------------------------------------------------- #

# --------------------------------- [edit] ---------------------------------- #
# 로그인한 사용자 정보를 조회하는 load_logged_in_user 함수 구현
# @bp.before_app_request 애너테이션을 사용했다. 이 애너테이션이 적용된 함수는 라우트 함수보다 먼저 실행
# load_logged_in_user 함수는 모든 라우트 함수보다 먼저 실행
@bp.before_app_request
def load_logged_in_user():
    # g.user에는 User 객체가 저장
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
# --------------------------------------------------------------------------- #

# --------------------------------- [edit] ---------------------------------- #
# 로그아웃 함수 구현하기
@bp.route('/logout/')
def logout():
    # logout 함수에는 세션의 모든 값을 삭제할 수 있도록 session.clear()를 추가
    session.clear()
    return redirect(url_for('main.index'))
# --------------------------------------------------------------------------- #

# 데코레이터 함수를 생성
#  @login_required 애너테이션을 지정하면 login_required 데코레이터 함수가 먼저 실행
# login_required 함수는 g.user가 있는지를 조사하여 없으면 로그인 URL로 리다이렉트 하고 g.user가 있으면 원래 함수를 그대로 실행
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view