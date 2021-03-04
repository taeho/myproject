from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
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


# --------------------------------- [edit] ---------------------------------- #
# url_for('answer.modify', answer_id=answer.id) URL이 추가되었으므로
# answer_views.py 파일에 modify 함수를 추가
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)
# --------------------------------------------------------------------------- #

# url_for('answer.delete', answer_id=answer.id) URL이 추가되었으므로
# answer_views.py 파일에 delete 함수를 작성하자.
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))