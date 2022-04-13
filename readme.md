#Tech Tracker
This project will be a technical support dispatch and logging system.  Users will be able to visit the page, login, and submit a request for support.  A dispatcher will see the request and assign it to a particular technician for a particular time slot.  The user requesting support will be notified via email, and the technician will be notified via the mobile friendly interface. When the technician arrives on site, they will use the interface to start the job, make notes, and request any parts to be ordered.  They will then schedule a new time slot if they must return, or mark the job as finished.  The user will get an automatic invoice when the job is finished, and the dispatcher can pull a report of billed jobs, parts to order and other system information. 

## Setting up
- Clone the repo from GitHub
  - Make sure your product has a valid venv set up for python 3.8 or later.
- install requirements: `pip install -r requirements.txt`
- copy or rename the file called `env.sample` to `.env`
  - DO NOT INCLUDE THIS FILE IN YOUR COMMIT (it is in the gitignore file already)
  - Add the appropriate settings values:
    - SECRET_KEY
      - You can leave as is for testing, but if deploying, you can generate a new key here: https://miniwebtool.com/django-secret-key-generator/
    - DB
      - The database type you want to use.  Leave at `sqlite` for testing, but can change to `MYSQL` if you want to connect to a mysql database.
    - DB_NAME
      - Name of the database.  Leave at `db.sqlite3` for testing
    - DB_HOST
      - Hostname of the database server.  Leave blank for your local machine (127.0.0.1)
    - DB_USER
      - Username with read/write permission to the database
    - DB_PASSWORD
      - Password to use when connecting to the database
    - DB_PORT
      - TCP/IP Port to use to connect to the server.  Default MYSQL port is 3306
    - AWS_ACCESS_KEY_ID
      - The access key id for your AWS S3 bucket
    - AWS_SECRET_ACCESS_KEY
      - The access key secret for your AWS S3 bucket
    - AWS_STORAGE_BUCKET_NAME
      - The AWS S3 bucket name
    - HEROKU
      - Is this system running in a Heroku environment.
      - Mostly prepares the settings file for including Heroku specific items.

  - If use S3, you can follow these steps to setup the AWS Bucket:
    - https://blog.theodo.com/2019/07/aws-s3-upload-django/
  - These environment files typically have a way to be provided by a hosting system.
    - In Heroku, open your app dashboard and then navigate to Settings and add an entry for each item necessary under Config Vars
    - Make sure the "HEROKU" config var is set to "True"
- 

### Initial Setup
*DO THIS ONLY ONCE AT THE VERY BEGINNING OR TO START OVER!!*
- In the terminal, run `python manage setup` 
  - This will:
    1. Erase any migrations
    2. Make the migrations fresh
    3. Delete the SQLITE db if found (it will NOT delete a MYSQL database.  You must reset this manually if you want to start over and are using a MySQL database)
    4. Populate the WorkingDay, PayRate, Skills tables and add some dummy parts
    5. It will run db seeding operation to create techs and users.  Follow the on-screen prompts
    6. Prompt to create a new superuser



### Keep existing DB
- If you want to not seed the db and keep any existing data, you can just run:
  - `python manage.py makemigrations && python manage.py migrate`
  - `python manage.py initial_entities` (if you want the basic info (WorkingDay, PayRate, Skills, and dummy parts) populated)
  - `python manage.py createsuperuser` (if you want a superuser created)

### Run Server
- After running either the initial setup or other setup routines run:
  - `python manage.py runserver`

## Styling
- Bulma.io
  - https://bulma.io/
- Bulmaswatch
  - https://jenil.github.io/bulmaswatch/spacelab/
- Bulma Quick View
  - https://wikiki.github.io/components/quickview/

## Toasts, Dialogs
- Sweet Alert 2
  - https://sweetalert2.github.io/

## Jquery Date/Time Picker
- https://flatpickr.js.org/

## Icons
- Fontawesome
  - https://fontawesome.com/

## Special Packages Used:
- django-admin-list-filter-dropdown
  - Better dropdown filters in admin
- django-seed
  - Create seeding functions
- python-decouple
  - Use env variables to not commit sensitive info
- django-widget-tweak
  - Form Styling
  - Referenced this (a lot): https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
##Unsplash Image attribution
- Harddrive, Nick van der Ende
- Keyboard, Martin Garrido
- Mouse: Oscar Ivan Esquivel Arteaga
- Laptop: Erick Cerritos
- Computer: Luke Hodde
