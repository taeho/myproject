from flask import Blueprint, url_for
from werkzeug.utils import redirect

# 블루프린트를 이용하면 라우트 함수를 구조적으로 관리
# 플라스크에서는 URL과 호출되는 함수의 관계를 확인할 수 있는 Blueprint 클래스를 의미
bp = Blueprint('main', __name__, url_prefix='/')

## localhost:5000/hello 접속시 라우터 /hello에 매핑된 hello_pybo 호출, 출력
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

# localhost:5000/ 접속시 라우터 / 에 매핑된 index 함수 호출, 출력
@bp.route('/')
def index():
    return redirect(url_for('question._list'))

# @bp.route('/detail/<int:question_id>/')
# def detail(question_id):
#     question = Question.query.get(question_id)
#     return render_template('question/question_detail.html', question=question)