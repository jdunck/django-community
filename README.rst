Overview
========

This is a branch/clone of the actual django website. Github just makes for easier collaboration.

To visit the canonical repository, visit http://code.djangoproject.com/browser/djangoproject.com/django_website



Installation Instructions
=========================

Checkout code:
::

    git clone git://github.com/justinlilly/django-community.git
    cd django-community

Install virtualenv:
::

    # either..
    apt-get install python-virtualenv
    # or..
    easy_install -U virtualenv

Create & Activate virtualenv:
::

    virtualenv env
    . env/bin/activate

Install pip & requirements:
::

    easy_install -U pip
    pip install -r requirements.txt

Create database:
::

    createuser -U postgres `whoami`
    createdb -U `whoami` djangoproject

Create Schema:
::

    cd django_website
    python manage.py syncdb
    # fill out user info

Run the Server:
::

    python manage.py runserver

Visit http://localhost:8000/community/
