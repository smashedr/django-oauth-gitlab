# Django Twitch

[![build status](https://git.cssnr.com/shane/django-twitch/badges/master/build.svg)](https://git.cssnr.com/shane/django-twitch/commits/master) [![coverage report](https://git.cssnr.com/shane/django-twitch/badges/master/coverage.svg)](https://git.cssnr.com/shane/django-twitch/commits/master)

This is a Django Framework for a Twitch site.

# Features

### Site Settings

Fully customizable settings including title, meta tags, favicon, twitch user, and more...

### Social Settings

Fully customizable social links.

### Twitch Oauth

Twitch Oauth managed from Django admin.

### Frameworks

- Django (2.1.2) https://www.djangoproject.com/
- Bootstrap (4.1.3) http://getbootstrap.com/
- Font Awesome (5.4.2) http://fontawesome.io/

# Development

### Deployment

To deploy this project on the development server:

```
git clone https://git.cssnr.com/shane/django-twitch.git
cd django-twitch
pyvenv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp settings.ini.example settings.ini
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata site-fixtures.json
python manage.py loaddata social-fixtures.json
python manage.py runserver 0.0.0.0:8000
```

*Note: Make sure to update the `settings.ini` with the necessary details...*

### Copying This Project

To clone a clean copy of this project int your repository:

```
git clone https://git.cssnr.com/shane/django-twitch.git
cd django-twitch
rm -rf .git
git init
git remote add origin https://github.com/your-org/your-repo.git
git push -u origin master
```

*Note: make sure to replace `your-org/your-repo.git` with your actual repository location...*
