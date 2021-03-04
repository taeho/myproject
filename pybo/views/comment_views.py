from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Question, Comment, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')

#  질문 상세 템플릿에서 ‘댓글추가..’ 링크에 해당하는 create_question 함수를 작성
#  한 가지 주의할 점은, 질문에 달린 댓글이므로 Comment 모델 객체를 생성할 때 question 필드에 값을 설정한 점
@bp.route('/create/question/<int:question_id>', methods=('GET', 'POST'))
@login_required
def create_question(question_id):
    form = CommentForm()
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), question=question)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('comment/comment_form.html', form=form)

# 이어서 댓글을 수정할 수 있도록 url_for('comment.modify_question', comment_id=comment.id)
# URL에 매핑되는 modify_question 함수를 작성
# 댓글 등록 함수와 구성은 크게 다르지 않다. GET 방식으로 요청할 경우 기존 댓글을 조회하여 반환
# POST 방식으로 요청할 경우 폼에서 받은 내용으로 댓글을 업데이트
@bp.route('/modify/question/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.question.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=comment.question.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)

#댓글을 삭제하는 url_for('comment.delete_question', comment_id=comment.id)
# URL에 매핑되는 delete_question 함수를 작성
@bp.route('/delete/question/<int:comment_id>')
@login_required
def delete_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.question.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

# 질문 댓글 함수들과 거의 차이가 없다. 다만 답변 댓글은 question_id 필드의 값을 알기 위해
# comment.answer.question.id와 같이 answer를 사용해서 question에 접근하고 있다.
@bp.route('/create/answer/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def create_answer(answer_id):
    form = CommentForm()
    answer = Answer.query.get_or_404(answer_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), answer=answer)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=answer.question.id))
    return render_template('comment/comment_form.html', form=form)


@bp.route('/modify/answer/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.answer.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=comment.answer.question.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/answer/<int:comment_id>')
@login_required
def delete_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.answer.question.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))