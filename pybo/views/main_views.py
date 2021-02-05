from flask import Blueprint, render_template

from pybo.models import Question

# 블루프린트를 이용하면 라우트 함수를 구조적으로 관리
# 플라스크에서는 URL과 호출되는 함수의 관계를 확인할 수 있는 Blueprint 클래스를 의미
bp = Blueprint('main', __name__, url_prefix='/')

# url_prefix : Blueprint 클래스로 객체를 생성할 때는 이름, 모듈명, URL 프리픽스(url_prefix)값을 전달해야
# 어노테이션이 app.route에서 bp로 변경됨. blueprint 클래스로 생성한 객체 의미
# @bp.route('/')
# def hello_pybo():
#     return 'Hello, Pybo!'

## localhost:5000/hello 접속시 라우터 /hello에 매핑된 hello_pybo 호출, 출력
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

# localhost:5000/ 접속시 라우터 / 에 매핑된 index 함수 호출, 출력
@bp.route('/')
def index():
    # 질문 목록은 Question.query.order_by로 얻을 수 있다
    # 작성일시 순서로 질문목록을 조회하려면 order_by(Question.create_date.asc()) 또는 asc()를 생략
    # order_by(Question.create_date)라고 작성
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

# 상세조회 함수 구현 localhost:5000/detail/2/
# 즉, localhost:5000/detail/2/ 페이지를 요청하면 main_views.py 파일의 detail 함수가 실행되고,
# 매개변수 question_id에는 2라는 값이 전달
# 매핑 규칙에 있는 int는 question_id에 숫자값이 매핑됨을 의미
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question)