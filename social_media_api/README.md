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