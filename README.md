# Role-based-Access-Control
Only users with specific roles can create users and peform certain operations on the server

# Functionality
For the projects to work, first install the dependencies in the requirements.txt file.
Create superuser: python manage.py createsuperuser


### Login: http://127.0.0.1:8000/api/login
	
	If the user is authenticated the server returns a web token with the format
	{
    	"username": "username",
   	 	"token": "c020ec3c4a6d5a99e5b6f587afece979b68f267c"
	}
	Response is a status code 200. 
	Incase of invalid credentials, then the server will return a status 401 with a message "Invalid credentials"
	Post body should have:
		* Username
		* Password
		
	For first time login the user will receive a message asking for password change.
	{
    	"username": "username",
   	 	"token": "c020ec3c4a6d5a99e5b6f587afece979b68f267c",
		"message": "Consider changing your first time login password"
	}
	
### Request headers
	The Authorization in the request headers should have a value with the format "Token c020ec3c4a6d5a99e5b6f587afece979b68f267c" for authentication. 		Unauthenticated requests are rejected except for login.
	
	
### Only a user with an admin role can add a user
	Add User body: http://127.0.0.1:8000/api/add-user
		* Username
		* Password
		* Email
		* Role
	Response is a status 200 with a success message. The post request header needs to have authorization token of a user with an admin role.
	Other users will receive a status 403 Forbidden
	
### Get Request to view all users according to role
	List of Users in the database
	Url Format: http://127.0.0.1:8000/api/users?role=admin
				http://127.0.0.1:8000/api/users?role=staff
				http://127.0.0.1:8000/api/users?role=basic
	
	Each of the urls will return distinct users based on the role specified in the query params
	
### Change password
	Url: http://127.0.0.1:8000/api/change-password
	Request body Format: 
	{
		"password": "new_password"
	}
	
	If the password is provided the server will respond with a status code 200 with message 
	{
		"message": "Password Updated"
	}
	
	If no password in provided then the server will respond with a status code 400 with message 
	{
		"message": "Provide password"
	}

### Run with docker 
	docker build -t app .
	docker run -d -p 80:8000 app

