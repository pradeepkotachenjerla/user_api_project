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

This documentation was generated with GenAI assistance and covers the schema, endpoints, and validation logic for your Flask-based user API project.
