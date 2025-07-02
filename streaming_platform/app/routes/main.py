from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.video import Video, WatchHistory

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    featured_videos = Video.query.order_by(Video.views.desc()).limit(6).all()
    recent_videos = Video.query.order_by(Video.created_at.desc()).limit(6).all()
    return render_template('main/index.html',
                         featured_videos=featured_videos,
                         recent_videos=recent_videos)

@bp.route('/profile')
@login_required
def profile():
    user_videos = Video.query.filter_by(user_id=current_user.id).all()
    watch_history = WatchHistory.query.filter_by(user_id=current_user.id).order_by(WatchHistory.watched_at.desc()).limit(10).all()
    return render_template('main/profile.html',
                         user_videos=user_videos,
                         watch_history=watch_history)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        videos = Video.query.filter(
            (Video.title.ilike(f'%{query}%')) |
            (Video.description.ilike(f'%{query}%'))
        ).all()
    else:
        videos = []
    return render_template('main/search.html', videos=videos, query=query) 