from pybo import db

# id : 질문 데이터 고유번호
# subject : 질문 제목
# content: 질문 내용
# create_date : 질문 작성일시

# Question 클래스는 모든 모델의 기본 클래스인 db.Model을 상속
# db는 __init__.py 파일에서 생성한 SQLAlchemy 객체
#  db.Column() 괄호 안의 첫 번째 인수는 데이터 타입을 의미
class Question(db.Model):
    # 고유 번호 id에 지정한 primary_key는 id 속성을 기본 키로 지정
    id = db.Column(db.Integer, primary_key=True)
    #  nullable은 속성에 빈값을 허용할 것인지를 결정
    # 빈값을 허용하지 않으려면 nullable=False를 지정
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

# id: 답변 데이터 고유번호
# question_id : 질문 데이터 고유 번호(어떤질문의 대한 답변인지위해)
# content : 답변 내용
# create_date : 답변 작성일시
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 어떤 속성을 기존 모델과 연결하려면 db.ForeignKey를 사용
    # 데이터베이스에서는 기존 모델과 연결된 속성을 외부 키(foreign key)
    #  답변 모델의 question_id 속성은 질문 모델의 id 속성과 연결되며
    #  #ondelete='CASCADE'에 의해 데이터베이스에서 쿼리를 이용하여 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    # db.relationship에 지정한 첫 번째 값은 참조할 모델명이고 두 번째 backref에 지정한 값은 역참조 설정이다.
    # 역참조란 쉽게 말해 질문에서 답변을 참조하는 것을 의미
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)