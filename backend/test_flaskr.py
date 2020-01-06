import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from flask_cors import CORS


class CategoriesTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:marco@localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # TEST to query all categories; GET
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # TEST to generate 405 error
    def test_get_categories_405(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Method Not Allowed')

class QuestionsTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:marco@localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # TEST to query all questions paginated
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'], True)
        self.assertTrue(len(data['questions']))

    # TEST to generate 404 if page is too high
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource not found')

    # TEST to create new question
    def test_create_new_questions(self):
        data = {
            "question": "test",
            "answer": "test",
            "difficulty": 5,
            "category": 5
        }
        res = self.client().post('/questions', json=data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    # TEST to generate error if submitting a new question w/o data
    def test_post_new_question_400(self):
        data = {
            "question": "",
            "answer": "",
            "difficulty": 1,
            "category": 1
        }
        res = self.client().post('/questions', json=data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)

    # TEST to query questions by category ID
    def test_questions_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(len(data['current_category']))

    # TEST to generate error if querying questions by category ID with a category ID that does not exist
    def test_questions_category_404(self):
        res = self.client().get('/categories/9999999/questions')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    # TEST to delete question by category ID
    '''
    def test_delete_question(self):
        # Delete last record
        last_question = Question.query.all()[-1]
        res = self.client().delete(f'/questions/{last_question.id}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
    '''
    # TEST to generate 404 error during deletion if category ID does not exist
    def test_delete_question_404(self):
        res = self.client().delete('/questions/88')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)


    # TEST to display results from search form
    def test_search_questions(self):
        data = {"searchTerm": "Hanks"}
        res = self.client().post('/questions', json=data)
        data_result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data_result['success'], True)
        self.assertTrue(len(data_result['questions']))
        self.assertTrue(data_result['total_books'] > 0)


    # TEST to generate 405 error (Wrong method used)
    def test_search_questions_405(self):
        data = {"searchTerm": "Hanks"}
        res = self.client().get('/questions', json=data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.get_json()['success'], False)

    # TEST to get questions to play quiz
    def test_get_questions_play(self):
        data = {
            "quiz_category": {
                "id": 3
            },
            "previous_questions": []
        }
        res = self.client().post('/quizzes', json=data)
        data_result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data_result['success'], True)
        self.assertTrue(data_result['quizCategory'] != "")
        self.assertTrue(len(data_result['question']))

    # TEST to generate 405 error when starting questions to play quiz
    def test_get_questions_play_405(self):
        data = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        }
        res = self.client().get('/quizzes', json=data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.get_json()['success'], False)

    # TEST to generate 404 error when starting questions to play quiz
    def test_get_questions_play_400(self):
        data = {
            "quiz_category": {
                "id": None
            },
            "previous_questions": []
        }
        res = self.client().post('/quizzes', json=data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()