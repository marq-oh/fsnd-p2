import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)


  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    #categories = Category.query.all()
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    formatted_categories = [c.get("type") for c in formatted_categories]

    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
      #'total': len(Category.query.all())
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_paginated_questions():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    formatted_categories = [c.get("type") for c in formatted_categories]
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'current_category': formatted_categories,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter(Question.id == id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    search = body.get('searchTerm', None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_books': len(Question.query.all())
        })
      else:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })

    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:id>/questions')
  def get_categories_questions(id):
    category_id = id + 1
    category_type = Category.query.with_entities(Category.type).filter(Category.id == category_id).all()
    category_type = category_type[0][0]

    question_data = Question.query.filter(Question.category == category_id).all()
    question_list = [question.format() for question in question_data]

    if len(question_list) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': question_list,
      'total_questions': len(question_list),
      'current_category': category_type
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_questions_to_play():
    body = request.get_json()
    quiz_category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions', None)

    category_type = quiz_category.get("type")

    category_id = Category.query.with_entities(Category.id).filter(Category.type == category_type).all()
    category_id = category_id[0][0]

    questions_list = Question.query.filter(Question.category == category_id).all()
    formatted_questions_list = [question.format() for question in questions_list]
    formatted_questions_list = [q.get("question") for q in formatted_questions_list]
    previous_questions = previous_questions.insert(0, random.choice(formatted_questions_list))

    return jsonify({
      'success': True,
      'quiz_category': quiz_category,
      'previous_questions': previous_questions
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }), 422

  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(500)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method Not Allowed"
    }), 405

  return app