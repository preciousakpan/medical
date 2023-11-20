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
    - Edit lines 14 and 15 to test new users creation (optional)
    - Replace lines 42 and 43 with existing users in your database
    - Replace line 70 with an existing name from your database 
    - Replace line 66 with the JWT token of the user on line 70 (Generate the JWT token from the login endpoint using postman)
    - Run the app using either python or docker
    - On another terminal, run "pytest test.py"

TO USE THE API DOCUMENTATION
    - download the json file
    - import it into postman