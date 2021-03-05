from flask import Flask
# ORM 적용을 위한 import 추가
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

import config

# --------------------------------- [edit] ---------------------------------- #
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
# --------------------------------------------------------------------------- #
# 전역변수 선언
db = SQLAlchemy()
migrate = Migrate()

#######################################
# app = Flask(__name__)
#
# @app.route('/')
# def hello_pybo():
#     return 'Hello, Pybo!'
########################################
# create_app 함수가 app 객체를 생성해서 반환하도록 코드 수정
# app 객체가 함수 안에서 사용되므로 hello_pybo함수를 create_app함수안에 포함
# create_app 함수가 애플리케이션 팩토리. create_app 는 플라스크 내부 정의함수명이라 변경하면x
def create_app():
    app = Flask(__name__)

    # config.py 파일에 작성한 항목을 app.config 환경변수 호출을 위한 추가
    app.config.from_object(config)

    # ORM, 전역 변수로 셋팅초기화
    db.init_app(app)
    # --------------------------------- [edit] ---------------------------------- #
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    # --------------------------------------------------------------------------- #
    # #생성한 모델들을 플라스크의 Migrate 기능이 인식할 수 있도록
    from . import models

    # @app.route('/') #라우트함수
    # def hello_pybo():
    #     return 'Hellow, Pybo!'

    # views 폴더의 블루프린트 적용
    # 블루프린트를 사용하려면 main_views.py파일에서 생성한 블루프린트 객체인 bp를 등록
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    # 생성한 블루프린터 객체를 등록.
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # --------------------------------- [edit] ---------------------------------- #
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime
    # --------------------------------------------------------------------------- #

    return app