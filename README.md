# recepi-project

this project  is a complete recipes API mainly consists of recipes and their tags, ingredients. 
This project is built using Django, Django rest framework, Travis ci, Docker and Postgres SQL.

------------------------------------------------------------------

To test the project:
 1. clone the project to your local pc.
  2.  run from cmd ->   docker-compose  build    and wait unit it completes building the image
  3. run ->  docker-compose run --rm app sh -c "python manage.py makemigrations"
 4.   run ->  docker-compose run --rm app sh -c "python manage.py test"

## to test the project in the browser:
1. complete the above step first then, 
 2. run ->   docker-compose up
 3. go to the browser and type   http://localhost:8000/api/accounts/create  and have fun !
    you can go to the urls file in the project to see a  complete list of all available APIs URLs.

