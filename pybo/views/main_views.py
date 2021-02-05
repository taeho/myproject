from flask import Blueprint

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
    return 'Pybo index'