import os
from flask import Blueprint, render_template, request, send_file, current_app, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.video import Video, WatchHistory
from app import db
from moviepy.editor import VideoFileClip
import subprocess

bp = Blueprint('video', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_video_qualities(video_path):
    """Get available video qualities using ffprobe"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'json',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            if 'streams' in data and len(data['streams']) > 0:
                width = data['streams'][0].get('width', 0)
                height = data['streams'][0].get('height', 0)
                return {
                    'original': f"{height}p",
                    '1080p': '1080p',
                    '720p': '720p',
                    '480p': '480p'
                }
    except Exception as e:
        print(f"Error getting video qualities: {e}")
    return {'original': 'Original'}

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No video file')
            return redirect(request.url)
            
        file = request.files['video']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create uploads directory if it doesn't exist
            upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save to local storage
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # Get video duration
            video = VideoFileClip(file_path)
            duration = int(video.duration)
            video.close()
            
            # Create video record
            video = Video(
                title=request.form.get('title'),
                description=request.form.get('description'),
                filename=filename,
                duration=duration,
                category=request.form.get('category'),
                user_id=current_user.id
            )
            
            db.session.add(video)
            db.session.commit()
            
            flash('Video uploaded successfully!')
            return redirect(url_for('video.watch', video_id=video.id))
            
    return render_template('video/upload.html')

@bp.route('/watch/<int:video_id>')
def watch(video_id):
    video = Video.query.get_or_404(video_id)
    video.views += 1
    db.session.commit()
    
    if current_user.is_authenticated:
        history = WatchHistory(user_id=current_user.id, video_id=video_id)
        db.session.add(history)
        db.session.commit()
    
    # Get available qualities
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
    video_path = os.path.join(upload_folder, video.filename)
    qualities = get_video_qualities(video_path)
        
    return render_template('video/watch.html', video=video, qualities=qualities)

@bp.route('/stream/<int:video_id>')
def stream(video_id):
    video = Video.query.get_or_404(video_id)
    quality = request.args.get('quality', 'original')
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
    video_path = os.path.join(upload_folder, video.filename)
    
    # If quality is not original, transcode the video
    if quality != 'original':
        try:
            output_path = os.path.join(upload_folder, f"{video.filename.rsplit('.', 1)[0]}_{quality}.mp4")
            if not os.path.exists(output_path):
                height = int(quality.replace('p', ''))
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vf', f'scale=-2:{height}',
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-y',
                    output_path
                ]
                subprocess.run(cmd, check=True)
            video_path = output_path
        except Exception as e:
            print(f"Error transcoding video: {e}")
    
    return send_file(
        video_path,
        mimetype='video/mp4'
    )

@bp.route('/update_watch_duration/<int:video_id>', methods=['POST'])
@login_required
def update_watch_duration(video_id):
    video = Video.query.get_or_404(video_id)
    watch_duration = request.json.get('duration', 0)
    
    history = WatchHistory.query.filter_by(
        user_id=current_user.id,
        video_id=video_id
    ).first()
    
    if history:
        history.watch_duration = watch_duration
    else:
        history = WatchHistory(
            user_id=current_user.id,
            video_id=video_id,
            watch_duration=watch_duration
        )
        db.session.add(history)
    
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/edit/<int:video_id>', methods=['GET', 'POST'])
@login_required
def edit(video_id):
    video = Video.query.get_or_404(video_id)
    
    if video.author.id != current_user.id:
        flash('You do not have permission to edit this video')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        video.title = request.form.get('title')
        video.description = request.form.get('description')
        video.category = request.form.get('category')
        
        db.session.commit()
        flash('Video updated successfully!')
        return redirect(url_for('video.watch', video_id=video.id))
        
    return render_template('video/edit.html', video=video)

@bp.route('/delete/<int:video_id>')
@login_required
def delete(video_id):
    video = Video.query.get_or_404(video_id)
    
    if video.author.id != current_user.id:
        flash('You do not have permission to delete this video')
        return redirect(url_for('main.index'))
        
    # Delete from local storage
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads')
    file_path = os.path.join(upload_folder, video.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete transcoded versions
    for quality in ['1080p', '720p', '480p']:
        transcoded_path = os.path.join(upload_folder, f"{video.filename.rsplit('.', 1)[0]}_{quality}.mp4")
        if os.path.exists(transcoded_path):
            os.remove(transcoded_path)
    
    db.session.delete(video)
    db.session.commit()
    
    flash('Video deleted successfully')
    return redirect(url_for('main.profile'))

@bp.route('/<int:video_id>/preview')
def preview(video_id):
    video = Video.query.get_or_404(video_id)
    video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], video.filename)
    
    # Generate a 10-second preview
    preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'preview_{video.filename}')
    
    if not os.path.exists(preview_path):
        clip = VideoFileClip(video_path)
        preview = clip.subclip(0, min(10, clip.duration))
        preview.write_videofile(preview_path, codec='libx264', audio_codec='aac')
        clip.close()
        preview.close()
    
    return send_file(preview_path, mimetype='video/mp4') 