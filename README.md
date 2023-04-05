
<h1>Welcome to Restaurant Website</h1>



## Functionality




## Flow Chart 



## Design


### Reservation Form

- Radio Tags, targeted by Javascript to stay coloured when selected
- Custom error message using "inspect" to match Validation error if time selected is on the day of booking but earlier than the current time. Tested by adding time to Time_choices and ensuring error displayed.
### Models

### Forms
- Used min max numbers on forms party size so that users can not select unser 1 or over 6, this is also on the models validator but it adds an ease of use to the user having arrows to select party size

## Initial Setup

For this Project a Template provided by CodeInstitute was used -[Template](https://github.com/Code-Institute-Org/gitpod-full-template)

- Click "Use this Template" then "Create a new repository"
- Give the repository a name then click "Create repository from template"
### DJANGO AND LIBRARIES
- Install Django and Libraries:
 - pip3 install 'django<4' gunicorn (This installs the LTS (Long Term Support) version of Django and is therefore preferable to use over a beta version)

- Set up the project to use Cloudinary and PostgreSQL:
    - Install Django and PostgreSQL libraries:
        - pip3 install dj_database_url==0.5.0 psycopg2 (Returns a Django database connection dictionary & 
          PostgreSQL database adapter)
    - Install Cloudinary Libraries:
        pip3 install dj3-cloudinary-storage

- Create local requirements:
    - pip3 freeze --local > requirements.txt

- Created Project:
    - django-admin startproject __PROJ_NAME__ . 

- Created Required Apps:
    - python3 manage.py startapp __APP_NAME__
    - Each APP is then added to INSTALLED_APPS in settings.py

- Changes are Migrated as needed, but initially as:
    - python3 manage.py migrate

- The server is then tested:
    - python3 manage.py runserver

### ElephantSQL
- Create an External Database:
    - Log in to ElephantSQL
    - Create New Instance
        - Name the project
        - select "Tiny Turtle" (free version)
        - Click Select Region and choose the nearest Data Center
        - Click "Review", then click "Create instance"
    - Click on the newly created project in the dashboard
    - Copy the URL - "postgres://...."

### HEROKU APP 
- Login to the Heroku App:
    - Click "New", then "Create new app"
    - Under App name - name the app, with a unique name
    - Choose your region
    - Click Create app
    - On your new app, click "Settings"
    - Click Reveal Config Vars
    - Add a Config Var called DATABASE_URL and give it the value from ElephantSQL ("postgres://....") and 
      click Add

### Cloudinary
- Login to Cloudinary
- On the Dashboard under API Environment variable, copy the CLOUDINARY_URL (copy from after the "=" symbol) 
### Link Databases and Hide KEYS
- Create an env.py in the top-level directory (This is for the SECRET_KEY in Django and also the URL's for ElephantSQL and Cloudinary, so they are not pushed to Git and visible to others)
- At the top of the env.py file import os
- Create Environment Variables for DATABASE_URL(ElephantSQL URL), SECRET_KEY(Django Secret Key) and CLOUDINARY_URL (Cloudinary URL)
- Set these equal to their corresponding values with - os.environ["VARIABLE_NAME"] = "Corresponding Variable"
- Do the same in Config Vars on Heroku, so the config vars on Heroku should be DATABASE_URL, SECRET_KEY, CLOUDINARY_URL
- Add DISABLE_COLLECTSTATIC = 1 on HEROKU also, for the development period, this is removed at project completion.
- In Heroku Config VARS add PORT = 8000
- Check .gitignore 
    - add *.sqlite3 to hide your database

    -   core.Microsoft*
        core.mongo*
        core.python*
        env.py
        __pycache__/
        *.py[cod]
        node_modules/
        .github/
        cloudinary_python.txt
        *.sqlite3

### Settings.py Setup
- Before Deployment make sure Debug = False as if not, secret information could be displayed to users 
  unwittingly
- In settings.py import os, import dj_database_url and import env
    - import os
      import dj_database_url

      if os.path.isfile("env.py"):
        import env

- Hide the SECRET_KEY variable
    - SECRET_KEY = os.environ.get('SECRET_KEY')

- Comment out the DATABASES Section and Add:
    DATABASES = {
   'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

- Add Cloudinary Libraries to INSTALLED_APPS:
    - INSTALLED_APPS = [
    …,
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    …,
    ] - The order is important

- Instruct DJANGO to use Cloudinary to Store Media and Static Files
    - STATIC_URL = '/static/'

      STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
      STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
      STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

      MEDIA_URL = '/media/'
      DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

- Link file to templates directory in Heroku (Under BASE_DIR)
    - TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

- Set the TEMPLATES DIR in TEMPLATES [...]
    - TEMPLATES = [
            {
                …,
                'DIRS': [TEMPLATES_DIR],
            …,
                    ],
                },
            },
        ]

- Add the App name to ALLOWED_HOSTS
    - ALLOWED_HOSTS = ["forgottenit-restaurant.herokuapp.com", "localhost"]

### Top-level directories

- Create media, static and templates folders in the top-level directory

- Create a Procfile
    - In Procfile add web: gunicorn restaurant.wsgi

- Migrate changes
    - python3 manage.py migrate

- Push Changes to Git
    - git add .
      git commit -m “Commit Comment”
      git push

### Heroku Deployment
- In Heroku, on the app go to the Deploy section
- Click GitHub  in the "Deployment method" section
- Under the "Connect to GitHub" section, type in the repository name in the "repo-name" field then click 
  "Search"
- Once your repository name comes up underneath, click "Connect"
- Scroll down to the Manual deploy section and click "Deploy Branch"
- Then at the top of the page click "Open app"

## Crispy Forms
- pip install django-crispy-forms

- Add to settings.py:
    - INSTALLED_APPS = [
    ...
    'crispy_forms',
    'crispy_bootstrap5',
    '...
]   
   -  Add TEMPLATE packs:
      CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
      CRISPY_TEMPLATE_PACK = "bootstrap5"

- Insert {% load crispy_forms_tags %} at top of HTML page

## Alert Messages

- Imported constants as messages to display Login/ Sign up/ Log Out success messages using:
from django.contrib.messages import constants as messages
then amending the settings.py to add the message tags and styling:
MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }
The message div was then targeted to close after 2.5 Seconds using the set Timeout function. 
- This method was learned from the CodeInstitute classes.





## Technology used

1. GitPod for writing the code
2. Python as the programming language
3. Heroku for deployment
4. Code Instistute Terminal for displaying finished product
5. https://pep8ci.herokuapp.com/ CI Python Linter for testing code
6. # DJANGO, CLOUDINARY, ElephantSQL....

## Imports used from Python Library


## Testing


## Constraints



# Learning and Future Improvements

## Learning



## Future improvements  




## Deployment
<h3>GitPod<h3>


<h3>Heroku</h3>


## Acknowledgements 

