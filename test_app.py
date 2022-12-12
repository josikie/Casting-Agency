import os
from unicodedata import category
import unittest
import json
from urllib import request
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, weCommit, Movie, Actor
from dotenv import load_dotenv
from auth.auth import AuthError, requires_auth, get_token_auth_header

DB_URL_TEST = os.environ.get('DATABASE_URL_TEST')
CREDENTIALS_EXECUTIVE = os.environ.get('CREDENTIALS_EXECUTIVE')
CREDENTIALS_DIRECTOR = os.environ.get('CREDENTIALS_DIRECTOR')
CREDENTIALS_ASSISTANT = os.environ.get('CREDENTIALS_ASSISTANT')


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "testdb"
        self.database_path = DB_URL_TEST

        with self.app.app_context():
            setup_db(self.app, self.database_path)
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    
    def tearDown(self):
        pass

    
    def test_welcome_resource(self):
        req = self.client().get('/')
        data = json.loads(req.data)

        self.assertEqual(data['message'], 'Welcome, dear! Please login first to use our resources')

    
    # test for assistant
    def test_get_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(CREDENTIALS_ASSISTANT)
        }
        req = self.client().get('/movies', headers=headers)
        data = json.loads(req.data)

        self.assertEqual(data['status_code'], 200)
    

    # test for assistant
    def test_404_get_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(CREDENTIALS_ASSISTANT)
        }
        req = self.client().get('/movies/1', headers=headers)
        data = json.loads(req.data)

        self.assertEqual(data['status_code'], 405)


    # test for executive
    def test_post_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().post('/movies', headers=headers, json={"title":"Aquaman 5", "release_date":"11-29-2013"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)

    # test for executive
    def test_400_post_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().post('/movies', headers=headers, json={"itle":"Queen''s Gambit", "release_date":"10-23-2020"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 400)

    
    # test for executive
    def test_patch_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().patch('/movies/3', headers=headers, json={"release_date":"11-20-2019"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)
    

    # test for executive
    def test_405_patch_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().patch('/movies', headers=headers, json={"release_date":"11-20-2019"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 405)

    
    # test for executive
    def test_delete_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/movies/6', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)

    
    # test for executive
    def test_404_delete_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/movies/120', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)


    # test for executive
    def test_get_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().get('/actors', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_405_get_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().get('/actors/12', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 405)


    # test for director
    def test_post_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_DIRECTOR)
        }
        req = self.client().post('/actors', headers=headers, json={"name":"Angelina", "age":26, "gender":"female"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for director
    def test_400_post_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_DIRECTOR)
        }
        req = self.client().post('/actors', headers=headers, json={"nme":"Irfan Gunawan", "age":26, "gender":"female"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 400)


    # test for executive
    def test_patch_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().patch('/actors/3', headers=headers, json={"name":"Railey", "age":28, "gender":"female"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_404_patch_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().patch('/actors/200', headers=headers, json={"name":"Railey", "age":28, "gender":"female"})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)


    # test for executive
    def test_delete_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/actors/6', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_404_delete_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/actors/8002', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)


    # test for executive
    def test_get_movie_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().get('/movie-items/movies/1', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_404_get_movie_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().get('/movie-items/movies/1231', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)

    
    # test for executive
    def test_get_actor_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().get('/movie-items/actors/3', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_404_get_actor_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().get('/movie-items/actors/690', headers=headers)
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)

    
    # test for executive
    def test_post_movie_items(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().post('/movie-items', headers=headers, json={"movie_id":3, "actor_id":3})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_404_post_movie_items(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().post('/movie-items/334', headers=headers, json={"movie_id":3, "actor_id":3})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)


    # test for executive
    def test_delete_movie_items_movie_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/movie-items/movies', headers=headers, json={"movie_id":3, "actor_id":4})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)

    # test for executive
    def test_404_delete_movie_items_movie_actors(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/movie-items3dr/movies', headers=headers, json={"movie_id":3, "actor_id":4})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 404)

    
    # test for executive
    def test_delete_movie_items_actor_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/movie-items/actors', headers=headers, json={"movie_id":3, "actor_id":1})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 200)


    # test for executive
    def test_405_delete_movie_items_actor_movies(self):
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(CREDENTIALS_EXECUTIVE)
        }
        req = self.client().delete('/movie-items/actors/34', headers=headers, json={"movie_id":3, "actor_id":1})
        data =json.loads(req.data)

        self.assertEqual(data['status_code'], 405)

if __name__=="__main__":
    unittest.main()