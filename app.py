import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, weCommit
from auth.auth import AuthError, requires_auth, get_token_auth_header

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def welcome():
        return jsonify({
            'message': 'Welcome, dear! Please login first to use our resources'
        })

    # get all movie
    # casting assistant
    # casting director
    # executive producer
    # get:movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        allMovies = Movie.query.all()
        movies = [mv.format() for mv in allMovies]
        return jsonify({
            'movies': movies,
            'success': True,
            'status_code': 200
        })

    # delete movies
    # executive producer
    # delete:movies
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        getMovie = Movie.query.get_or_404(id)
        formattedMovie = getMovie.format()
        movieId = formattedMovie.get('id')
        movieTitle = formattedMovie.get('title')
        getMovie.actors = []
        weCommit(getMovie)
        getMovie.delete()

        return jsonify({
            'deletedMovieId': movieId,
            'deletedMovieTitle': movieTitle,
            'status_code': 200,
            'success': True
        })

    # post movies
    # executive producer
    # post:movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movie(jwt):
        newMovie = request.get_json()
        newMovieTitle = newMovie.get('title', None)
        newMovieReleaseDate = newMovie.get('release_date', None)

        try:
            movie = Movie(newMovieTitle, newMovieReleaseDate)
            movie.insert()

            return jsonify({
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date,
                'status_code': 200,
                'success': True
            })
        except:
            abort(400)
    
    # patch movies
    # casting director
    # executive producer
    # patch:movies
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie = request.get_json()
        updatedMovie = Movie.query.get_or_404(id)

        movieTitle = movie.get('title', None)
        if movieTitle != None:
            updatedMovie.title = movieTitle
        
        movieReleaseDate = movie.get('release_date', None)
        if movieReleaseDate != None:
            updatedMovie.release_date = movieReleaseDate
        
        try:
            updatedMovie.update()
            return jsonify({
                'id': id,
                'title': updatedMovie.title,
                'release_date': updatedMovie.release_date,
                'success': True,
                'status_code': 200
            })
        except:
            abort(400)

    # get all actors
    # casting assistant
    # casting director
    # executive producer
    # get:actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'actors': formatted_actors,
            'success': True,
            'status_code': 200
        })

    # delete actors
    # casting director
    # executive producer
    # delete:actors
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        getActor = Actor.query.get_or_404(id)
        actorName = getActor.name
        getActor.movies = []
        weCommit(getActor)
        getActor.delete()
        
        return ({
            'id': id,
            'name': actorName,
            'status_code': 200,
            'success': True
        })


    # post actors
    # casting director
    # executive producer
    # post:actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actor(jwt):
        newActor = request.get_json()
        newActorName =  newActor.get('name', None)
        newActorAge = newActor.get('age', None)
        newActorGender = newActor.get('gender', None)

        try:
            actor = Actor(newActorName, newActorAge, newActorGender)
            actor.insert()

            return jsonify({
                'id': actor.id,
                'name': actor.name,
                'status_code': 200,
                'success': True
            })
        except:
            abort(400)

    # patch actors
    # casting director
    # executive producer
    # patch:actors
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor = request.get_json()
        updatedActor = Actor.query.get_or_404(id)
        
        actorName = actor.get('name', None)
        if actorName != None:
            updatedActor.name = actorName
        
        actorAge = actor.get('age', None)
        if actorAge != None:
            updatedActor.age = actorAge

        actorGender = actor.get('gender', None)
        if actorGender != None:
            updatedActor.gender = actorGender
        
        try:
            updatedActor.update()
            return jsonify({
                'id': id,
                'name': updatedActor.name,
                'status_code': 200,
                'success': True
            })

        except:
            abort(400)
        
    # get list of all actors of a movie
    # casting assistant
    # casting director
    # executive producer
    # get:movie-items/movies
    @app.route('/movie-items/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movie-items/movies')
    def get_all_actors_movie(jwt, id):
        movie = Movie.query.get_or_404(id)
        actors = movie.actors
        formattedActor = [actor.format() for actor in actors]
        return jsonify({
            'movieId': id,
            'movieTitle': movie.title,
            'movieActors': formattedActor,
            'totalOfMovieActors': len(formattedActor),
            'status_code': 200,
            'success': True
        })

    # get list of all movie of an actor
    # casting assistant
    # casting director
    # executive producer
    # get:movie-items/actors
    @app.route('/movie-items/actors/<int:id>', methods=['GET'])
    @requires_auth('get:movie-items/actors')
    def get_all_movie_actors(jwt, id):
        actor = Actor.query.get_or_404(id)
        movies = actor.movies
        formattedMovies = [movie.format() for movie in movies]
        return jsonify({
            'id': id,
            'actorName': actor.name,
            'actorMovies': formattedMovies,
            'totalOfActorMovies': len(movies),
            'status_code': 200,
            'success': True
        })

    # insert to movie items
    # executive producer
    # post:movie-items
    @app.route('/movie-items', methods=['POST'])
    @requires_auth('post:movie-items')
    def insert_third_table(jwt):
        ids = request.get_json()
        movie_id = ids.get('movie_id', None)
        actor_id = ids.get('actor_id', None)
        movie = Movie.query.get_or_404(movie_id)
        actor = Actor.query.get_or_404(actor_id)
        try:
            movie.actors.append(actor)
            weCommit(movie)
            return jsonify({
                'movie_id': movie_id,
                'movie_title': movie.title,
                'actor_id': actor_id,
                'actor_name': actor.name,
                'status_code': 200,
                'success': True
            })
        except:
            abort(400)

    # delete movie's actor items
    # executive producer
    # delete:movie-items/movies
    @app.route('/movie-items/movies', methods=['DELETE'])
    @requires_auth('delete:movie-items/movies')
    def delete_movie_movie_items(jwt):
        movieItems = request.get_json()
        movie_id = movieItems.get('movie_id', None)
        actor_id = movieItems.get('actor_id', None)
        
        movie = Movie.query.get_or_404(movie_id)
        actor = Actor.query.get_or_404(actor_id)

        movie.actors.remove(actor)
        weCommit(movie)
        movieActors = movie.actors
        formattedMovieActors = [actor.format() for actor in movieActors]

        return jsonify({
            'movieId': movie_id,
            'actorId': actor_id,
            'movieActorsNow': formattedMovieActors,
            'totalMovieActorsNow': len(formattedMovieActors),
            'status_code': 200,
            'success': True
        })

    # delete actor's movie items
    # casting director
    # executive producer
    # delete:movie-items/actors
    @app.route('/movie-items/actors', methods=['DELETE'])
    @requires_auth('delete:movie-items/actors')
    def delete_actor_movie_items(jwt):
        movieItems = request.get_json()
        movie_id = movieItems.get('movie_id', None)
        actor_id = movieItems.get('actor_id', None)
        
        movie = Movie.query.get_or_404(movie_id)
        actor = Actor.query.get_or_404(actor_id)

        actor.movies.remove(movie)
        weCommit(actor)
        actorMovies = actor.movies
        formattedActorMovies = [movie.format() for movie in actorMovies]

        return jsonify({
            'actorId': actor_id,
            'movieId': movie_id,
            'actorMoviesNow': formattedActorMovies,
            'totalActorMoviesNow': len(formattedActorMovies),
            'status_code': 200,
            'success': True
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status_code': 404,
            'message': 'resource not found',
            'success': False
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'status_code': 400,
            'message': 'bad request',
            'success': False
        })

    @app.errorhandler(403)
    def forbidden_access(error):
        return jsonify({
            'status_code': 403,
            'message': 'forbidden access',
            'success': False
        })

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'status_code': 405,
            'message': 'method not allowed',
            'success': False
        })

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'status_code': 422,
            'message': 'unprocessable entity',
            'success': False
        })
    return app

app = create_app()

if __name__=="__main__":
    app.run()