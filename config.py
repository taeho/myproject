# 파이보에 ORM을 적용하려면 config.py라는 설정 파일이 필요
import os

BASE_DIR = os.path.dirname(__file__)

#SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션, 필요치 않아서 false처리
SQLALCHEMY_TRACK_MODIFICATIONS = False
