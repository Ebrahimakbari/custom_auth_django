## Project Overview

This project is a Django authentication system with fully customizable options. It allows users to register, login, logout, update their profiles, and reset their passwords. The system is designed to be easily customizable and can be used as a starting point for building more complex authentication systems.

## Installation

To install this project, simply clone the repository and set the API key. You can then use the project as is or customize it to fit your needs.

## Features

- User registration with email and username
- User login and logout
- User profile update
- Password reset
- Customizable password validation
- Customizable username validation

## Requirements

- Django 4.2
- Pillow 11.0.0
- python-decouple 3.8

## Configuration

To configure the project, you need to set the following environment variables:

- `SECRET_KEY`: This is a secret key used by Django for security purposes.
- `EMAIL_HOST_USER`: This is the email address used to send emails for password reset.
- `EMAIL_HOST_PASSWORD`: This is the password for the email address used to send emails for password reset.

## Usage

To use this project, you need to include the `account` app in your `INSTALLED_APPS` setting in your Django project's `settings.py` file.

```python
INSTALLED_APPS = [
    ...
    'account',
    ...
]
```

You also need to include the `account` URLs in your Django project's `urls.py` file.

```python
urlpatterns = [
    ...
    path('account/', include('account.urls')),
    ...
]
```

## Contributing

If you want to contribute to this project, you can fork the repository and submit a pull request with your changes.