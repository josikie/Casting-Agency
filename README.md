## Casting Agency API ##
A back end application contains API for Casting Agency. It is used to help manage between artists and movies on casting agency. There are 15 endpoints for Movie, Actor, and movie_items. Credentials {token} in setup.sh file for assistant, director, and executive. Note: If there is server error, that means I haven't update the new credentials on setup.sh. I will always generate new credentials so you can try this app.

### How to run ###
1. Test 

    - Install dependencies:
    `pip3 install -r requirements.txt`

    - Add env variables to terminal:
    `chmod +x setup.sh`
    `source setup.sh`

    - Comment all test in test_app.py first, so there are only setUp, tearDown, and if __name__=="__main__": unittest.main()

    - Try run the test_app.py so the database made:
    `python3 test_app.py`

    - Stop application from running, you can use ctrl + c, or just cancel the terminal and you can reopen terminal again.

    - Uncomment all test in test_app.py.

    - Go to psql, login, and add this data to postgres locally:

	    Table movie (title and release date are string)
	    id  title       release_date
	    1   Frozen      11-29-2013
	    2   Frozen 2    11-20-2019
	    3   Aquaman     12-21-2018
	    4   Aquaman 2   12-25-2023
	    6   Aquaman 4   11-29-2013

	    Table actor (name and gender are string)
	    id  name            age     gender
	    1   Jason Momoa     43      Male
	    2   Emilia Clarke   36      Female
	    3   Idina Menzel    51      Female
	    4   Kristen Bell    42      Female
	    6   Angelina        26      female

	    Table movie_items
	    movie_id   actor_id
	    1           3
	    2           3
	    1           4
	    2           4
	    3           1
	    3           4

    - and run the test_app.py :
    `python3 test_app.py`

    Don't need migrations for only test in test_app.py. After run the test_app.py once, and you want to run it again, please drop the database in psql first, then loop the step above.

2. curl:
    - Migrate database,
    - Go to psql, login, and add this data to postgres locally:

	    Table movie (title and release date are string)
	    id  title       release_date
	    1   Frozen      11-29-2013
	    2   Frozen 2    11-20-2019
	    3   Aquaman     12-21-2018
	    4   Aquaman 2   12-25-2023
	    6   Aquaman 4   11-29-2013

	    Table actor (name and gender are string)
	    id  name            age     gender
	    1   Jason Momoa     43      Male
	    2   Emilia Clarke   36      Female
	    3   Idina Menzel    51      Female
	    4   Kristen Bell    42      Female
	    6   Angelina        26      female

	    Table movie_items
	    movie_id   actor_id
	    1           3
	    2           3
	    1           4
	    2           4
	    3           1
	    3           4

    - In git bash:
        `flask run`
    
    - Access some of API endpoints below (there are example of how to try it on curl).

### Endpoints ###

Endpoints that casting assistant can access
    - GET /movies = get:movies
    - GET /actors  =  get:actors
    - GET /movie-items/movies/<int:id>  = get:movie-items/movies
    - GET /movie-items/actors/<int:id> = get:movie-items/actors

Endpoints that casting director can access
    - GET /movies  = get:movies
    - PATCH /movies/<int:id> = patch:movies
    - GET /actors =  get:actors
    - DELETE /actors/<int:id> = delete:actors
    - POST /actors = post:actors
    - PATCH /actors<int:id> = patch:actors
    - GET /movie-items/movies/<int:id> = get:movie-items/movies
    - GET /movie-items/actors/<int:id> = get:movie-items/actors
    - DELETE /movie-items/actors = delete:movie-items/actors

Endpoints that executive producer can access
    - GET /movies  = get:movies
    - DELETE /movies/<int:id> = delete:movies
    - POST /movies = post:movies
    - PATCH /movies/<int:id> = patch:movies
    - GET /actors =  get:actors
    - DELETE /actors/<int:id> = delete:actors
    - POST /actors = post:actors
    - PATCH /actors<int:id> = patch:actors
    - GET /movie-items/movies/<int:id> = get:movie-items/movies
    - GET /movie-items/actors/<int:id> = get:movie-items/actors
    - POST /movie-items = post:movie-items
    - DELETE /movie-items/movies/<int:id> = delete:movie-items/movies
    - DELETE /movie-items/actors/<int:id> = delete:movie-items/actors

### API Resources ###

GET http://localhost:5000/
    - return a json object contains message
    - you can access it through website without providing credentials
    Try in curl:
    curl http://localhost:5000/
    result example:
    {
        "message": "Welcome, dear! Please login first to use our resources"
    }

GET http://localhost:5000/movies
    - Fetch Movies
    - need Authorization (Bearer token) in headers
    - return json object contains list of available movies
    Try in curl:
    curl http://localhost:5000/movies -H 'Authorization: Bearer {token}'
    result example:
    {
        "movies": [
            {
                "id": 1,
                "release_date": "10-10-2016",
                "title": "Moana"
            },
            {
                "id": 2,
                "release_date": "12-14-2022",
                "title": "Avatar 2"
            }
        ],
        "status_code": 200,
        "success": true
    }

GET http://localhost:5000/actors
    - Fetch Actors
    - need Authorization (Bearer token) in headers
    - return json object contains list of available actors
    Try in curl:
    curl http://localhost:5000/actors -H 'Authorization: Bearer {token}'
    result example:
    {
    "actors": [
        {
            "age": 40,
            "gender": "female",
            "id": 1,
            "name": "Lily Rose"
        },
        {
            "age": 40,
            "gender": "female",
            "id": 2,
            "name": "Lily Rose"
        }
    ],
    "status_code": 200,
    "success": true
    }

GET http://localhost:5000/movie-items/movies/{id}
    - Fetch movie's actors
    - need Authorization (Bearer token) in headers
    - return json object contains list of available movie's actors
    Try in curl:
    curl http://localhost:5000/movie-items/movies/1 -H 'Authorization: Bearer {token}'
    result example:
    {
        "movieActors": [
            {
                "age": 40,
                "gender": "female",
                "id": 2,
                "name": "Lily Rose"
            }
        ],
        "movieId": 1,
        "movieTitle": "Moana",
        "status_code": 200,
        "success": true,
        "totalOfMovieActors": 1
    }

GET http://localhost:5000/movie-items/actors/{id}
    - Fetch actor's movies
    - need Authorization (Bearer token) in headers
    - return json object contains list of available actor's movies
    Try in curl:
    curl http://localhost:5000/movie-items/actors/1 -H 'Authorization: Bearer {token}'
    result example:
    {
        "actorMovies": [
            {
                "id": 2,
                "release_date": "12-14-2022",
                "title": "Avatar 2"
            }
        ],
        "actorName": "Lily Rose",
        "id": 1,
        "status_code": 200,
        "success": true,
        "totalOfActorMovies": 1
    }

POST http://localhost:5000/movies
    - Create new movie
    - need Authorization (Bearer token) in headers
    - need new movie's data in headers
    - return json object contains data from created movies
    Try in curl:
    curl -X POST http://localhost:5000/movies -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"title":"Frozen 1", "release_date":"2015"}'
    return example:
    {
        "id": 7,
        "release_date": "2015",
        "status_code": 200,
        "success": true,
        "title": "Frozen 1"
    }

PATCH http://localhost:5000/movies/{id}
    - Update existing movie
    - need Authorization (Bearer token) in headers
    - need movie's data in headers
    - return json object contains list updated movie
    Try in curl:
    curl -X PATCH http://localhost:5000/movies/7 -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"release_date":"12-23-2013"}'
    return example:
    {
        "id": 7,
        "release_date": "12-23-2013",
        "status_code": 200,
        "success": true,
        "title": "Frozen 1"
    }

DELETE http://localhost:5000/movies/7
    - Delete existing movie
    - need Authorization (Bearer token) in headers
    - need movie's data in headers
    - return json object contains deleted movie
    Try in curl:
    curl -X DELETE http://localhost:5000/movies/7 -H 'Authorization: Bearer {token}'
    return example:
    {
        "deletedMovieId": 7,
        "deletedMovieTitle": "Frozen 1",
        "status_code": 200,
        "success": true
    }

POST http://localhost:5000/actors
    - Create new actor
    - need Authorization (Bearer token) in headers
    - need actor's data in headers
    - return json object contains created actor
    Try in curl:
    curl -X POST http://localhost:5000/actors -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"name":"Taylor Swift", "age":32, "gender":"female"}'
    return example:
    {
        "id": 6,
        "name": "Taylor Swift",
        "status_code": 200,
        "success": true
    }

PATCH http://localhost:5000/actors/{id}
    - Update existing actor
    - need Authorization (Bearer token) in headers
    - need actor's data in headers
    - return json object contains updated actor
    Try in curl:
    curl -X PATCH http://localhost:5000/actors/6 -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"gender":""}'
    result example:
    {
        "id": 6,
        "name": "Taylor Swift",
        "status_code": 200,
        "success": true
    }

DELETE http://localhost:5000/actors/{id}
    - delete existing actor
    - need Authorization (Bearer token) in headers
    - need actor's data in headers
    - return json object contains deleted actor
    Try in curl:
    curl -X DELETE http://localhost:5000/actors/7 -H 'Authorization: Bearer {token}'
    return example:
    {
        "id": 6,
        "name": "Taylor Swift",
        "status_code": 200,
        "success": true
    }

POST http://localhost:5000/movie-items
    - create new data in the third table
    - need Authorization (Bearer token) in headers
    - need movie id and actor id in headers
    - return json object contains movie and actor data
    Try in curl:
    curl -X POST http://localhost:5000/movie-items -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"movie_id":1, "actor_id":1}'
    result example:
    {
        "actor_id": 1,
        "actor_name": "Lily Rose",
        "movie_id": 1,
        "movie_title": "Moana",
        "status_code": 200,
        "success": true
    }

DELETE http://localhost:5000/movie-items/actors
    - delete an actor's movie
    - need Authorization (Bearer token) in headers
    - need movie id and actor id in headers
    - return json object contains movie and actor data
    curl -X DELETE http://localhost:5000/movie-items/actors -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"movie_id":1, "actor_id":1}'
    result example:
    {
        "actorId": 1,
        "actorMoviesNow": [
            {
                "id": 2,
                "release_date": "12-14-2022",
                "title": "Avatar 2"
            }
        ],
        "movieId": 1,
        "status_code": 200,
        "success": true,
        "totalActorMoviesNow": 1
    }

DELETE http://localhost:5000/movie-items/movies
    - delete a movie's actor
    - need Authorization (Bearer token) in headers
    - need movie id and actor id in headers
    - return json object contains movie and actor data
    Try in curl:
    curl -X DELETE http://localhost:5000/movie-items/actors -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' --data '{"movie_id":2, "actor_id":2}'
    result example:
    {
        "actorId": 2,
        "movieActorsNow": [
            {
                "age": 40,
                "gender": "female",
                "id": 1,
                "name": "Lily Rose"
            }
        ],
        "movieId": 2,
        "status_code": 200,
        "success": true,
        "totalMovieActorsNow": 1
    }