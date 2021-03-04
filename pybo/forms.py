from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# 질문 등록을 할 때 사용할 QuestionForm 클래스를 작성
# QuestionForm 클래스는 Flask-WTF 모듈의 FlaskForm 클래스를 상속받으며 subject, content 속성을 포함
# 폼 클래스의 속성과 모델 클래스의 속성은 비슷
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


# --------------------------------- [edit] ---------------------------------- #
# username은 필수 항목이면서 길이를 제한해야 하므로 validators 옵션에 필수 항목으로 DataRequired()와
# 길이 조건 Length(min=3, max=25)를 추가.
# ‘비밀번호’, ‘비밀번호확인’ 필드 password1, password2를 PasswordField로 추가
# 두 값은 일치해야 하므로 password1의 validators 옵션에 EqualTo 검증을 추가
class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
# --------------------------------------------------------------------------- #

# FlaskForm 클래스를 상속받아 UserLoginForm을 만들었다. username, password 필드를 추가
class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

#댓글을 등록할 때 사용할 CommentForm 클래스 추가
class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])