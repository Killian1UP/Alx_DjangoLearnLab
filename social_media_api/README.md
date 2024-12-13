Setup Process: User Registration and Authentication
Install Required Packages
Ensure Django and djangorestframework are installed in your environment:
bash:
pip install django djangorestframework

Configure Settings
Update your settings.py to use the custom user model:
AUTH_USER_MODEL = 'accounts.CustomUser'
Run Migrations
Generate and apply migrations for the custom user model:
bash
python manage.py makemigrations
python manage.py migrate

Static and Media Files
Ensure your project is configured to handle static and media files properly, especially for profile pictures:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

Create Superuser
Use the custom manager to create a superuser:
bash
python manage.py createsuperuser

User Registration
URL: /accounts/register/
Functionality:
Users can create accounts by providing a username and password.
Template: accounts/register.html
Code Reference:
RegisterView in views.py uses the CustomUserCreationForm to register users.

Authentication
Login
URL: /accounts/login/
Template: accounts/login.html
Default Django login view.

Logout
URL: /accounts/logout/
Default Django logout view.

User Profile
View Profile
URL: /accounts/profile/
Permissions: IsAuthenticated
Response:
HTML: Render accounts/profile.html with user details.
JSON: Return user data as JSON.

Update Profile
HTTP Method: PUT
Functionality: Update user bio or profile picture.
Validation: Handled by CustomUserSerializer.

Overview of CustomUser Model
Base: Inherits from AbstractUser.

Fields:
bio: Text field for user biography.
profile_picture: Image field with default and upload functionality.
followers: Many-to-many relationship for following functionality.

Custom Manager:
create_user: Validates and creates standard users.
create_superuser: Adds staff and superuser privileges.
String Representation:
The username is returned for each user.

Detailed descriptions of each endpoint, including usage examples:
1. /api/posts/ (POST, GET)
POST: Create a new post.

Usage: Create a post by sending a JSON request with title, content, and author (or automatically set via the authenticated user).
Example Request:
{
    "title": "New Post",
    "content": "This is a new post.",
    "author": 1
}

Example Response (201 Created):
{
    "id": 1,
    "title": "New Post",
    "content": "This is a new post.",
    "author": 1
}

GET: List all posts.
Usage: Retrieve a list of all posts.

Example Response (200 OK):
[
    {
        "id": 1,
        "title": "New Post",
        "content": "This is a new post.",
        "author": 1
    },
    {
        "id": 2,
        "title": "Another Post",
        "content": "This is another post.",
        "author": 1
    }
]


Here's a concise description of each endpoint, including usage examples:

1. /api/posts/ (POST, GET)
POST: Create a new post.

Usage: Create a post by sending a JSON request with title, content, and author (or automatically set via the authenticated user).
Example Request:
json
Copy code
{
    "title": "New Post",
    "content": "This is a new post.",
    "author": 1
}
Example Response (201 Created):
json
Copy code
{
    "id": 1,
    "title": "New Post",
    "content": "This is a new post.",
    "author": 1
}
GET: List all posts.

Usage: Retrieve a list of all posts.
Example Response (200 OK):
json
Copy code
[
    {
        "id": 1,
        "title": "New Post",
        "content": "This is a new post.",
        "author": 1
    },
    {
        "id": 2,
        "title": "Another Post",
        "content": "This is another post.",
        "author": 1
    }
]

2. /api/posts/{id}/ (GET, PUT, DELETE)
GET: Retrieve a single post by ID.
Usage: Fetch details of a specific post using its ID.

Example Request:
/api/posts/1/
Example Response (200 OK):
{
    "id": 1,
    "title": "New Post",
    "content": "This is a new post.",
    "author": 1
}

PUT: Update a post by ID.
Usage: Update the details of an existing post.
Example Request:
{
    "title": "Updated Post Title",
    "content": "Updated content for the post."
}
Example Response (200 OK):
{
    "id": 1,
    "title": "Updated Post Title",
    "content": "Updated content for the post.",
    "author": 1
}
DELETE: Delete a post by ID.
Usage: Remove a specific post from the system.

Example Response (204 No Content): No content is returned, but the post is deleted.

3. /api/comments/ (POST, GET)
POST: Create a new comment on a post.
Usage: Create a comment by specifying the post (referencing the post ID) and content. The author is automatically set via the authenticated user.
Example Request:
{
    "post": 1,
    "content": "This is a comment on post 1."
}
Example Response (201 Created):
{
    "id": 1,
    "post": 1,
    "content": "This is a comment on post 1.",
    "author": 1,
    "created_at": "2024-12-13T12:34:56.789Z"
}

GET: List all comments.
Usage: Retrieve a list of all comments.

Example Response (200 OK):
[
    {
        "id": 1,
        "post": 1,
        "content": "This is a comment on post 1.",
        "author": 1
    },
    {
        "id": 2,
        "post": 1,
        "content": "Another comment on post 1.",
        "author": 2
    }
]

4. /api/comments/{id}/ (GET, PUT, DELETE)
GET: Retrieve a single comment by ID.
Usage: Fetch details of a specific comment using its ID.
Example Request:
/api/comments/1/
Example Response (200 OK):
{
    "id": 1,
    "post": 1,
    "content": "This is a comment on post 1.",
    "author": 1,
    "created_at": "2024-12-13T12:34:56.789Z"
}

PUT: Update a comment by ID.
Usage: Update the content of a specific comment.
Example Request:
{
    "content": "Updated comment content."
}
Example Response (200 OK):
{
    "id": 1,
    "post": 1,
    "content": "Updated comment content.",
    "author": 1
}
DELETE: Delete a comment by ID.
Usage: Remove a specific comment.

Example Response (204 No Content): No content is returned, but the comment is deleted.

5. /api-token-auth/ (POST)
POST: Obtain an authentication token for an existing user.
Usage: Send a POST request with the user's username and password to obtain a token.
Example Request:
{
    "username": "your_username",
    "password": "your_password"
}
Example Response (200 OK):
{
    "token": "your_token_here"
}

This token should then be included in the Authorization header (as Token your_token_here) for subsequent API requests that require authentication.

Authentication: All POST, PUT, and DELETE endpoints for posts and comments require the user to be authenticated. You'll need to include the token in the Authorization header as Token <your_token_here>.
Permissions: Only the author of a post or comment can modify or delete it. For others, these actions are restricted.