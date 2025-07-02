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

- ![Login Page](snapshots/login.png)
- ![Register Page](snapshots/register.png)
- ![Home Page](snapshots/index.png)
- ![Profile Page](snapshots/profile.png)
- ![Search Page](snapshots/search.png)
- ![Upload Video Page](snapshots/upload.png)
- ![Edit Video Page](snapshots/edit.png)
- ![Watch Video Page](snapshots/watch.png) 