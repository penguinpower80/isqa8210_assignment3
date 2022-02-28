#Tech Tracker
This project will be a technical support dispatch and logging system.  Users will be able to visit the page, login, and submit a request for support.  A dispatcher will see the request and assign it to a particular technician for a particular time slot.  The user requesting support will be notified via email, and the technician will be notified via the mobile friendly interface. When the technician arrives on site, they will use the interface to start the job, make notes, and request any parts to be ordered.  They will then schedule a new time slot if they must return, or mark the job as finished.  The user will get an automatic invoice when the job is finished, and the dispatcher can pull a report of billed jobs, parts to order and other system information. 

## Setting up
- Clone the repo from GitHub
  - Make sure your product has a valid venv set up for python 3.8 or later.
- install requirements: `pip install -r requirements.txt`
- copy env.sample to .env
  - Add the appropriate settings values.j
  - If use S3, you can follow these steps to setup the AWS Bucket:
    - https://blog.theodo.com/2019/07/aws-s3-upload-django/

### Initial Setup
*DO THIS ONLY ONCE AT THE VERY BEGINNING OR TO START OVER!!*
- run `python manage setup` 
  - This will:
    1. Erase any migrations
    2. Make the migrations fresh
    3. Delete the mysql db if found
    4. Populate the WorkingDay, PayRate, Skills tables and add some dummy parts
    5. It will run db seeding operation to create techs and users.  Follow the on-screen prompts
    6. Prompt to create a new superuser
- `python manage.py runserver`


### Keep existing DB
- If you want to not seed the db and keep any existing data, you can just run:
  - `python manage.py makemigrations && python manage.py migrate`
  - `python manage.py initial_entities` (if you want the basic info populated)
  - `python manage.py createsuperuser` (if you want a superuser created)
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
- django-wigdet-tweak
  - Form Styling
  - Referenced this (a lot): https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
##Unsplash Image attribution
- Harddrive, Nick van der Ende
- Keyboard, Martin Garrido
- Mouse: Oscar Ivan Esquivel Arteaga
- Laptop: Erick Cerritos
- Computer: Luke Hodde
