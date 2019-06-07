# Otus Django Courses

Simple website for Django REST API demonstration. Supports: user register, user login, registration on selected course.
Authorization and login were made by JSON requests for using in rich frontends.

[== DEMO ==](https://oc.space-coding.com/api)

**<Attention!>** This module was made by mad-skilled student. Never use it in production. I said "NEVER". :) **</Attention!>**
**<Disclaimer!>** I know about Django Filter. Bicycle invention in the name of learning! **</Disclaimer!>**

## Install
```commandline
git clone https://github.com/ravique/otus-courses-website.git
cd otus-django-shop
pip install -r requirements.txt
```
To perform migrations:
```commandline
python manage.py migrate
```

## API Reference

## Registration and login

**<Attention!>** For all POST requests CSRF Token in Headers required!

Passing unhached passwords in JSON? May be, not a very good idea, but we use CSRF protection and HTTPS.  

### Registration: `/api/register/` – POST
**Example**
```json
{
"username": "sammy",
"password": 1234
}
```

### Login `/api/login/` – POST
**Example**
```json
{
"username": "sammy",
"password": 1234
}
```

### Account `/api/account/` – GET
Returns user account details.

### Logout `/api/logout/` – POST

## Entities

All list-view endpoints return JSON with `links` (HATEOAS meta) and `objects` keys. 

### Courses list `/api/course/` – GET
Returns list of courses.

### Course detail `/api/<id>/` – GET
Returns detailed information about course.

### Register on course `/api/<id>/register/` – POST
Return 201 on success, 304 if you are already registered on this course.

### Lecturers list `/api/lecturer/` – GET
Returns list of lecturer.

### Lecturer detail `/api/lecturer/<id>/` – GET
Returns detailed information about lecturer.

### Lessons list `/api/lesson/` – GET, params available!
Returns list of lessons.
Supports filtration by:
- id
- name
- date (`/api/lesson/?date=2019-06-06`)
- course__name 

Multiple values of the same parameter supported (`/api/lesson/?course__name=Django&course__name=Python`)

### Lesson detail `/api/lesson/<id>/` – GET
Returns detailed information about lesson.

## Authors

* **Andrei Etmanov** - *Student of OTUS :)*

## License

This project is licensed under the MIT License – see the [LICENSE.md](LICENSE.md) file for details
