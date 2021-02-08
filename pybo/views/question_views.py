from flask import Blueprint, render_template

from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

# 질문 목록과 상세기능 적용
# 관리 유지보수 용이를 위해 분리
@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)