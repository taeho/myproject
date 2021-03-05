from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')

# 질문 추천 함수 만들기
# 추천 등록을 할 때 url_for('vote.question', question_id=question.id)
# URL을(1단계에서 HTML에 작성) 2단계 코드에서 호출할 수 있도록 만들었다 이 URL에 해당하는 라우트 함수를 추가
# Question 모델의 vorter는 여러 사람을 추가할 수 있는 다대다 관계이므로
# _question.voter.append(g.user)와 같이 append 함수로 추천인을 추가해야 한다
@bp.route('/question/<int:question_id>/')
@login_required
def question(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

# 답변 추천 함수 만들기
# url_for('vote.answer', answer_id=answer.id)
# URL을 추가했으므로 vote_views.py 파일에 answer 함수를 추가
@bp.route('/answer/<int:answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=_answer.question.id))