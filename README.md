# Homework 2

This is my submission of homework 2

- [x] Basic part: Implement authentication feature
  - [x] Listen on localhost:5000
  - [x] Render authentication form at <http://localhost:5000/>
  - [x] Redirect user to profile page if successfully authenticated
  - [x] Show profile page for authenticated user only at <http://localhost:5000/profile>
  - [x] User name and password are stored in Mongodb

- [x] Advanced part:
  - [x] Implement feature that allows users to create new account, profile will be shown with data respected to each account.
  - [x] Implement password hashing, logout and password change features
  - [x] Allow users to update profile picture (new user will have a default profile picture)
  - [x] Allow users to update profile information

- [ ] Challenging part:
  - [ ] Implement notification, an active user will receive notification when a new account is created.

## Prerequisites

* Running MongoDB on localhost:27017
  * Install docker
    - docker pull mongodb (pull mongodb image to local system)
    - docker run --name mongodb -d -p 27017:27017 mongo (start container)
  * Install docker-compass (GUI for mongodb)
    - Initialize connection with mongodb://localhost:27017
* requirements.txt

## Run

`python src/app.py`

## Credits

Ali Affaz (ISU 372795 / N4156c)
