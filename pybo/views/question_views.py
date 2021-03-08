from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from sqlalchemy import func
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question, Answer, User, question_voter
from ..views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

# 질문 목록과 상세기능 적용
# 관리 유지보수 용이를 위해 분리
@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    # 우선 추천순으로 정렬하는 코드
    # question_voter.c.question_id는 Question 모델과 조인하기 위한 것
    # func.count('*').label('num_voter')는 질문별 추천 수를 위한 것
    # group_by(question_voter.c.question_id)는 ‘같은 질문으로 그룹을 만든다’는 의미
    # func.count('*')는 ‘같은 질문 그룹의 추천 수’를 의미
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:  # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    # 조회한 데이터 question_list에 paginate 함수로 페이징을 적용
    #  1번째 인자로 전달된 page는 현재 조회할 페이지의 번호를 의미하고,
    #  2번째 인자 per_page로 전달된 10은 페이지마다 보여 줄 게시물이 10건임을 의미
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)

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

# --------------------------------- [edit] ---------------------------------- #
# modify 함수가 GET 방식으로 요청되는 경우는 <질문수정> 버튼을 눌렀을 때이다(question/question_form.html 템플릿 렌더링
# 수정할 질문에 해당하는 ‘제목’, ‘내용’ 등의 데이터가 보여야 한다
# 데이터베이스에서 조회한 데이터를 템 플릿에 적용하는 가장 간단한 방법은 QuestionForm(obj=question)과 같이
# 조회한 데이터를 obj 매개변수에 전달하여 폼을 생성하는 것
# QuestionForm의 subject, content 필드에 question 객체의 subject, content의 값이 적용
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        # flash 함수는 강제로 오류를 발생시키는 함수로, 로직에 오류가 있을 경우 사용
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)
# --------------------------------------------------------------------------- #

# delete 함수 역시 로그인이 필요하므로 @login_required 애너테이션을 적용하고,
# 로그인한 사용자와 글쓴이가 같은 경우에만 질문을 삭제할 수 있도록
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))