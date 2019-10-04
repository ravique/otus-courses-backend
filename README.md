[![Travis build result](https://travis-ci.com/ravique/otus-courses-website.svg?branch=master)](https://travis-ci.com/ravique/otus-courses-website/) [![codecov](https://codecov.io/gh/ravique/otus-courses-website/branch/master/graph/badge.svg)](https://codecov.io/gh/ravique/otus-courses-website)

# Otus Django Courses

Simple website for Django REST API demonstration. Supports: user register, user login, registration on selected course.
Authorization and login were made by JSON requests for using in rich frontends.

[== DEMO ==](https://oc.space-coding.com/api)

**<Attention!>** This module was made by mad-skilled student. Never use it in production. I said "NEVER". :) **</Attention!>**
**<Disclaimer!>** I know about Django Filter. Bicycle invention in the name of learning! **</Disclaimer!>**

## Install
```commandline
git clone https://github.com/ravique/otus-courses-website.git
cd otus-courses-website
pip install -r requirements.txt
```

then add `.env` to the `otus_django_courses` folder.

example:
```
EMAIL_HOST=<ip>
EMAIL_HOST_USER=<host_user>
EMAIL_HOST_PASSWORD=<password>
```

To perform migrations:
```commandline
python manage.py migrate
```

## Tests

```commandline
pytest
```

## API Reference

## Registration and login

**<Attention!>** For all POST requests CSRF Token in Headers required!

Passing unhached passwords in JSON? May be, not a very good idea, but we use CSRF protection and HTTPS.  

### Registration: `/api/register/` – POST
Required fields: `username, password, email`  
Optional fields: `first_name, last_name`

User must me verified by email. After registration you need to visit your mailbox for account activation.

**Example**
```json
{
"username": "sammy",
"password": 1234,
"email": "example@example.com"
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

### Course detail `/api/course/<id>/` – GET
Returns detailed information about course.

### Register on course `/api/course/<id>/register/` – POST
Return 201 on success, json with error on fail.

### Register on course `/api/course/<id>/unregister/` – POST
Return 201 on success, json with error on fail.

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
