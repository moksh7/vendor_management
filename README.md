# vendor_management

### Install project dependencies
`pip install -r requirements.txt`

### Perform database migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Create an admin user to manage the application and obtain an authentication token
`python manage.py createsuperuser`

### Generate Auth Token
`python manage.py drf_create_token {username}`

To refresh an existing token:
`python manage.py drf_create_token -r {username}`

### Start the development server
`python manage.py runserver`

### Explore Endpoints
Navigate to /swagger to explore and interact with the API endpoints. Use the "Authorize" tab to authenticate by entering the acquired token in the following format:
`Token <token>`

NOTE: **All UPDATE APIs support partial updates**

### Run Test cases
`python manage.py test`
