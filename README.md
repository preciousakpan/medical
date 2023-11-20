TO RUN THE APP USING PYTHON:
    - python3 -m virtualenv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - python3 manage.py makemigrations records
    - python3 manage.py migrate
    - python3 manage.py runserver

OR

TO RUN THE APP USING DOCKER
    - docker build -t medical .
    - docker run -p8000:8000 medical

TO RUN THE UNIT TESTS
    - Make sure the app is running
    -