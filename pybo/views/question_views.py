from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question
from ..views.auth_views import login_required


bp = Blueprint('question', __name__, url_prefix='/question')

# 질문 목록과 상세기능 적용
# 관리 유지보수 용이를 위해 분리
@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지,  type=int는 page 파라미터가 정수임
    question_list = Question.query.order_by(Question.create_date.desc())
    # 조회한 데이터 question_list에 paginate 함수로 페이징을 적용
    #  1번째 인자로 전달된 page는 현재 조회할 페이지의 번호를 의미하고,
    #  2번째 인자 per_page로 전달된 10은 페이지마다 보여 줄 게시물이 10건임을 의미
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

#질문 목록 화면에 질문 등록 URL을 추가했으므로 question_views.py 파일에 라우트 함수 create를 추가
@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    # QuestionForm 클래스의 객체 form을 생성하고 return 문에서 render_template 함수가 템플릿을 렌더링할 때 form 객체를 전달
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 폼으로 전송받은 ‘ 제목’ 데이터는 form.subject.data로 얻고 있다
        #question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        # --------------------------------- [edit] ---------------------------------- #
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        # --------------------------------------------------------------------------- #
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)