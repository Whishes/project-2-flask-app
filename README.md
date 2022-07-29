# _Project-2_ Nice-ities

<img src="/static/images/github_img_1.jpg" alt="project-img" width="900" height="600">

## Can be found at:

[Link to Project](https://immense-chamber-64350.herokuapp.com/)

## Installation Instructions:

1.  `git clone` with the specific **HTTPS** or **SSH** for this repo.
2.  In the code's folder run the following commands in this order:
    1.  `pip install venv`
    2.  `source venv/bin/activate`
    3.  If in the venv environment, run `pip install -r requirements.txt` to install required packages
3.  If postgreSQL is already installed on your machine, run `psql` then `CREATE DATABASE niceities` to create the required database.
    1.  if postgreSQL isn't already installed, follow the appropriate instructions from [here](https://www.postgresql.org/download/) and repeat step 3 when installed.
4.  To create the appropriate tables in the db, run `psql niceities < db/schema.sql` in the venv terminal
5.  To then seed some data to each table, run `python3 db/seed.py` in the venv terminal
6.  If everything is successful, run `python3 app.py` in the venv terminal

## Technologies Used:

During this project the technologies that had been used were;

- VS Code
- HTML (Jinja for templating)
- CSS (Bootstrap for carousel functionality)
- JavaScript
- Python (Flask, psycopg2, gunicorn, bcrypt)
- PostgreSQL for database management
- Google Chrome & Firefox for testing/dev tools
- Github for storing/managing code
- Heroku for hosting the website/db

## Main Features

- Login/Register
- Create sentences
- If logged in, users can like/unlike each displayed sentence
- All users (logged in or not) are able to share individual sentence links with each other/social media
- User profile so individual users can monitor/delete their own sentences

## Ideal/Planned Features:

- [ ] An admin control panel to help manage all sentences/users without necessarily needing to go inside heroku psql

## Database Design

<img src="/static/images/github_img_2.jpg" alt="db-design" width="900" height="600">

## Acknowledgements

- Staff at GA -
  - Instructors: Ken & Ge
  - Instructors Assistants: Lucy & Sam
- GA friends for being my rubber duck -
  - Particularly: Elise and Rob
