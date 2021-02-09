from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

# 질문 등록을 할 때 사용할 QuestionForm 클래스를 작성
# QuestionForm 클래스는 Flask-WTF 모듈의 FlaskForm 클래스를 상속받으며 subject, content 속성을 포함
# 폼 클래스의 속성과 모델 클래스의 속성은 비슷
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])