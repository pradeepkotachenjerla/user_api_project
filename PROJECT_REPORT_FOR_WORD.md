# User API Project: Full Report

## 1. Project Documentation

---

# User API Project Documentation

## Database Schema

- **users**
  - `id` (int, primary key, auto-increment): Unique user identifier
  - `name` (string, required): User's name
  - `email` (string, required, unique): User's email address
  - `age` (int, optional): User's age
  - `createdAt` (datetime): Timestamp when the user was created
  - `updatedAt` (datetime): Timestamp when the user was last updated

- **profiles**
  - `id` (int, primary key, auto-increment): Unique profile identifier
  - `user_id` (int, foreign key): References `users.id`
  - `bio` (text, optional): User's biography
  - `profile_picture_url` (string, optional): URL to profile picture
  - `social_links` (text, optional): Social media links

## API Endpoints

### Users
- `POST /users` — Create a new user
  - Request JSON: `{ "name": "Alice", "email": "alice@example.com", "age": 30 }`
  - Validates name, email, and age. Returns new user ID.
- `GET /users` — List all users
- `GET /users/<id>` — Get user by ID
- `PUT /users/<id>` — Update user by ID
  - Request JSON: `{ "name": "New Name", "email": "new@example.com", "age": 31 }`
  - Validates name, email, and age. Checks for unique email.
- `DELETE /users/<id>` — Delete user by ID

### Profiles
- `POST /profiles` — Create a new profile
  - Request JSON: `{ "user_id": 1, "bio": "Bio", "profile_picture_url": "url", "social_links": "links" }`
  - Validates that user exists.
- `GET /profiles` — List all profiles
- `GET /profiles/<id>` — Get profile by ID
- `PUT /profiles/<id>` — Update profile by ID
- `DELETE /profiles/<id>` — Delete profile by ID

## Data Validation Logic

- **Name**: Must be a non-empty string.
- **Email**: Must match a standard email format (regex: `^[\w\.-]+@[\w\.-]+\.\w+$`).
- **Age**: Must be an integer between 1 and 120 (inclusive).
- **Email Uniqueness**: No two users can have the same email.
- **Profile user_id**: Must reference an existing user.

Validation is performed in the API endpoints before any database operation. If validation fails, a clear error message and HTTP 400 status code are returned.

---

## 2. Example Code: routes.py

```python
import re
from flask import request, jsonify
from app import app, db
from app.models import User, Profile

def is_valid_name(name):
    return isinstance(name, str) and name.strip() != ''

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return isinstance(email, str) and re.match(pattern, email)

def is_valid_age(age):
    try:
        age = int(age)
        return 1 <= age <= 120
    except (TypeError, ValueError):
        return False

# ...existing code...
```

---

## 3. ChatGPT Conversation Summary

- Used GenAI to generate SQL schema, Flask app structure, models, and CRUD endpoints.
- Implemented and validated API endpoints for users and profiles.
- Added data validation for name, email, and age.
- Documented the entire process in Markdown and explained how to use and test the API.
- Provided instructions for pushing code to GitHub and exporting documentation.

---

**To create a .docx file:**
1. Open this file in VS Code or any Markdown viewer.
2. Copy all contents.
3. Paste into a new Microsoft Word document.
4. Save as .docx.

You can also add more code, screenshots, or conversation details as needed.
