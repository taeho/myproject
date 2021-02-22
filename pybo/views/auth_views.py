from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm
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