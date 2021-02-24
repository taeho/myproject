from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from .auth_views import login_required
from .. import db
from ..forms import AnswerForm
from ..models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')
# 답변모델 answer를 관리하는 블루프린트.

# create 함수의 매개변수 question_id는 URL 에서 전달된다.
# ocahost:5000/answer/create/2/ 페이지를 요청받으면 question_id에는 2가 넘어온다
# @bp.route의 methods 속성에는 'POST'를 지정
# @bp.route에 똑같은 폼 방식을 지정하지 않으면 다음과 같은 오류가 발생 - method not allowed
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        #answer = Answer(content=content, create_date=datetime.now())
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)