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


- ![LoginPage](https://github.com/user-attachments/assets/aeca0acc-1ff0-4c22-a0b6-17228739d3cd)
- ![Register Page](https://github.com/user-attachments/assets/8a1b1c17-10d5-4d5c-b360-f6c7e4126044)
- ![HomePage](https://github.com/user-attachments/assets/d8f02907-f5a6-453b-9601-78f4691108ba)
- ![Upload Page](https://github.com/user-attachments/assets/0b735ff3-c9ae-4945-bcb4-6de4d048c020)
- ![Selecting Category](https://github.com/user-attachments/assets/ba573416-8aee-4e6d-8e87-586e946dbabe)
- ![Edit video](https://github.com/user-attachments/assets/c0150d2c-e50d-4f9c-9c4a-31b1e78d21ac)
- ![Search page](https://github.com/user-attachments/assets/8c326032-dc20-469e-825a-d2d872a6db83)
- ![Search Page 2](https://github.com/user-attachments/assets/a6c757ca-cd22-43f0-b65e-c9ec1713986c)
- ![Delete Video page](https://github.com/user-attachments/assets/23b065ed-b96e-4307-b1a2-250ef7a18132)
- ![Home after SuccessFully deleted](https://github.com/user-attachments/assets/4bf4a4d5-c047-4a2d-9418-1601097634b9)
- [Watch Video Screen Recording](https://github.com/user-attachments/assets/4186eeb5-71b4-4567-975c-f270d9375fce)
- ![Profile Page](https://github.com/user-attachments/assets/936fda98-417e-4555-8da0-7b42ee5c17cb)



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
