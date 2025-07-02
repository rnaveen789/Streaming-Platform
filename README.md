# Streaming Platform

A modern streaming platform built with Flask that allows users to upload, stream, and manage video content.

## Features

- User authentication and authorization
- Video upload and streaming
- Video categorization and search
- User profiles and watch history
- Responsive web interface
- We can Like and share videos 

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///streaming.db 
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## Project Structure

```
streaming_platform/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
└── run.py
```

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Login
- AWS S3 (for video storage)
- HTML5/CSS3/JavaScript 

## Pages & Sections

The platform includes the following main pages:

- **Login Page** (`auth/login.html`)
  - Allows users to log in with their username and password.
  - Provides a link to the registration page for new users.

- **Register Page** (`auth/register.html`)
  - New users can create an account by providing a username, email, and password.
  - Includes password confirmation and a link to the login page.

- **Home Page / Dashboard** (`main/index.html`)
  - Displays featured and recent videos in a card layout.
  - Shows video title, description, author, category, and view count.
  - Prompts unauthenticated users to register.

- **Profile Page** (`main/profile.html`)
  - Shows user information, watch history, and a list of uploaded videos.
  - Allows users to upload new videos, edit, or delete their own videos.

- **Search Page** (`main/search.html`)
  - Lets users search for videos by keyword.
  - Displays search results or a message if no results are found.

- **Upload Video Page** (`video/upload.html`)
  - Authenticated users can upload new videos with title, description, category, and file upload.
  - Supports MP4, WebM, and OGG formats.

- **Edit Video Page** (`video/edit.html`)
  - Allows users to edit the title, description, and category of their uploaded videos.

- **Watch Video Page** (`video/watch.html`)
  - Main video player with custom controls, quality selection, and playback speed.
  - Like and share buttons, video details, and related videos sidebar.
  - Edit/delete options for video owners.

## Snapshots

> **To add real snapshots:**
> 1. Create a folder named `snapshots/` in the project root.
> 2. Add PNG/JPG images named after each page (e.g., `login.png`, `register.png`, `index.png`, `profile.png`, `search.png`, `upload.png`, `edit.png`, `watch.png`).
> 3. Replace the placeholder image links below with your actual screenshots.

- ![Login Page](https://github.com/user-attachments/assets/67efecb6-7716-4b25-871f-b58e7498d6bd)
- ![Register Page](https://github.com/user-attachments/assets/c56da307-f4c9-4752-bc62-21ea6272e192)
- ![Home Page](https://github.com/user-attachments/assets/d4fc4fb0-2ea2-455c-81a8-f2b124bec367)
- ![Video Upload Page](https://github.com/user-attachments/assets/088d09e3-186a-4899-8e66-403b837bf1d2)
- ![Selecting Category](https://github.com/user-attachments/assets/9313711b-295b-4533-bcd9-40c07a3a5a1a)
- ![Edit Vedio](https://github.com/user-attachments/assets/b31d2cd8-aea8-4110-935f-de27cff8daab)
- ![Delete Video page](https://github.com/user-attachments/assets/942154eb-8bb3-41b5-899b-4d686efef113)
- ![Home after SuccessFully deleted Video](https://github.com/user-attachments/assets/cae8bc11-496a-4223-9735-6bad8035f480)
- ![Search page](https://github.com/user-attachments/assets/910dcccc-86f9-4844-b758-3c6fa587cb57)
- ![Search Page 2](https://github.com/user-attachments/assets/36ce894e-d9f7-430e-8054-3a2429b93a7c)
- ![Watch Video Screen recoding](https://github.com/user-attachments/assets/fdf6ca01-7f4c-4b38-b342-1b94ddf2e47c)
- ![Profile Page](https://github.com/user-attachments/assets/fef0fdcb-c42b-48a5-8c17-e679ec4f9470)


## Database Models

- **User**: Stores user credentials and profile info. Has a one-to-many relationship with Video and WatchHistory.
- **Video**: Stores video metadata, file info, and is linked to a user (author). Has a one-to-many relationship with WatchHistory. Deleting a video cascades and deletes its watch history.
- **WatchHistory**: Tracks which user watched which video, when, and for how long.

## API / Routes Overview

- **Authentication**
  - `/register` (GET, POST): Register a new user
  - `/login` (GET, POST): Login
  - `/logout` (GET): Logout
- **Main**
  - `/` (GET): Home page (featured/recent videos)
  - `/profile` (GET): User profile, uploaded videos, watch history
  - `/search` (GET): Search videos
- **Video**
  - `/upload` (GET, POST): Upload a new video
  - `/watch/<video_id>` (GET): Watch a video
  - `/edit/<video_id>` (GET, POST): Edit a video
  - `/delete/<video_id>` (GET): Delete a video (with cascade delete for watch history)
  - `/stream/<video_id>` (GET): Stream video file
  - `/update_watch_duration/<video_id>` (POST): Update watch duration (AJAX)
  - `/<video_id>/preview` (GET): Get a 10-second preview

## Configuration

- Uses `.env` file for secrets and environment variables.
- Main config in `config.py` and `app/config.py`.
- Key variables: `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`, `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_BUCKET_NAME`, `MAX_CONTENT_LENGTH`, `ALLOWED_EXTENSIONS`.

## Dependencies

All dependencies are listed in `requirements.txt`:
- flask==2.0.1
- flask-sqlalchemy==2.5.1
- flask-login==0.5.0
- flask-wtf==0.15.1
- python-dotenv==0.19.0
- werkzeug==2.0.1
- moviepy==1.0.3
- pillow==10.2.0
- boto3==1.26.137
- python-jose==3.3.0
- requests==2.26.0
- SQLAlchemy==1.4.49

## App Factory Pattern

- The app uses a factory pattern (`create_app` in `app/__init__.py`).
- Blueprints for `auth`, `main`, and `video` routes are registered.
- Database tables are created automatically on first run.

## Entry Point

- Run the app with:
  ```bash
  python streaming_platform/run.py
  ```
- Or use Flask CLI if preferred.

## Troubleshooting

- **Pillow/SQLAlchemy errors**: Use the versions in `requirements.txt`.
- **Cascade delete**: Deleting a video will also delete its watch history (see Video model).
- **Database migrations**: If you change models, use Flask-Migrate or recreate the database.
- **File upload issues**: Check `MAX_CONTENT_LENGTH` and `ALLOWED_EXTENSIONS` in config. 
