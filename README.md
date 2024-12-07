# Startup
First, set up a virtual environment:
```
root> python -m venv env
```
Activate it. In powershell, for example, run:
```
root> ./env/Scripts/Activate
```
Install dependencies:
```
(env) root> pip install -r requirements.txt
```
Then create a database:
```
(env) root> python manage.py migrate
```
Create a superuser if you need to:
```
(env) root> python manage.py createsuperuser --username admin --email admin@example.com
```
Run a server:
```
(env) root> python manage.py runserver
```
# Api Description
Project is done using Django Rest Framework and all endpoints are represented by `ApiView`s, so you can navigate through API in the browser using buttons and objects' `"url"` fields.
## Resources
### `User`
- `url`
- `id`
- `username`
- `email`
### `Movie`
- `url`
- `id`
- `title`
- `description`

## Key Endpoints
### Auth
Server allows Session and Token-based authentication
- `api-auth/` - Provides `login/` and `logout/` endpoints for Session-based authentication.
- `api-token-auth/` - endpoint for token-based authentication, recieves `"username"` and `"password"` and returns token. For authentication recieved token should be provided in `Authorization` header in form `Token {your_token}`.
### Users
All user-related endpoints are on the `users/` prefix. This endpoints are for admin users only, apart from those that related to the currently authenticated user.
- `GET users/` - returns a list of all users. 
- `POST users/` - creates a new user.
- `GET users/{user_id}/` - returns the user with the given `user_id`.
- `PUT users/{user_id}/` - updates the user with the given `user_id`.
- `DELETE users/{user_id}/` - deletes the user with the given `user_id`.
### Movies
All movie-related endpoints are on the `movies/` prefix. Only admin users can create, update or delete movies.
- `GET movies/` - returns a list of all movies. 
- `POST movies/` - creates a new movie.
- `GET movies/{movie_id}/` - returns the movie with the given `movie_id`.
- `PUT movies/{movie_id}/` - updates the movie with the given `movie_id`.
- `DELETE movies/{movie_id}/` - deletes the movie with the given `movie_id`.
- `POST movies/{movie_id}/make-favorite/` - adds the movie with the given `movie_id` to your favorite list.
- `DELETE movies/{movie_id}/make-favorite/` - removes the movie with the given `movie_id` from your favorite list.
- `GET movies/favorites/` - return a list of your favorite movies.