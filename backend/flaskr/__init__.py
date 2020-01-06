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

    # First, query to get all categories
    # Then, filter to only store category type because that's all that's needed
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    formatted_categories = [c.get("type") for c in formatted_categories]

    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
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

    # Get full list of categories and format appropriately for jsonify
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    # Get all questions and then pass to paginate_questions() to format for jsonify
    # and set up pagination
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    # Define arrays for category data
    category_ids = []
    category_types = []

    # Populate arrays with actual values
    for cat in formatted_categories:
      category_ids.append(cat['id'])
      category_types.append(cat['type'])

    # Combine arrays to create dictionary with the required data and format
    categories_dict = dict(zip(category_ids, category_types))


    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories_dict,
      'current_category': None,
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
      # Query to get question by ID
      question = Question.query.filter(Question.id == id).one_or_none()

      if question is None:
        abort(404)

      # Execute delete transaction
      question.delete()
      selection = Question.query.order_by(Question.id).all()

      # Ensure questions are displayed with pagination
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

    # Get data that was submitted to endpoint
    body = request.get_json()

    for value in body.values():
      if not value:
        abort(400)

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    new_category = int(new_category) + 1
    search = body.get('searchTerm', None)

    try:
      # Check if 'search form' was used
      if search:

        # Query according to search term
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_books': len(Question.query.all())
        })

      # If 'search form' was not used
      else:
        # Prepare INSERT transaction
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        # Display latest data with pagination
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
    # Get category data based on ID
    category_id = id
    category_data = Category.query.filter(Category.id == category_id).all()
    category_list = [category.format() for category in category_data]

    # Get question data based on selected category
    question_data = Question.query.filter(Question.category == category_id).all()
    question_list = [question.format() for question in question_data]

    if len(question_list) == 0 or (category_list) == 0:
      abort(404)

    # Define arrays for category data
    category_ids = []
    category_types = []

    # Populate arrays with actual values
    for cat in category_list:
      category_ids.append(cat['id'])
      category_types.append(cat['type'])

    # Combine arrays to create dictionary with the required data and format
    categories_dict = dict(zip(category_ids, category_types))

    return jsonify({
      'success': True,
      'questions': question_list,
      'categories': category_list,
      'total_questions': len(question_list),
      'current_category': categories_dict[category_id]
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

    # Get JSON data submitted to endpoint
    body = request.get_json()

    if not body:
      abort(400)

    # Set up variables from submitted JSON data
    quiz_category = body.get('quiz_category', None)
    quiz_category_type = quiz_category.get('type')
    quiz_category_id = quiz_category.get('id')
    quiz_category_id = int(quiz_category_id)
    previous_questions = body.get('previous_questions', None)

    # Get questions
    if quiz_category_type == 'click':
      cat_id = 0
      questions_list = Question.query.order_by(Question.id).all()
      formatted_questions_list = [question.format() for question in questions_list]
      random_q = random.choice(formatted_questions_list)

      # Loop to check for previous questions
      counter = 1
      random_q = {}

      if len(previous_questions) > 0:
        for q in formatted_questions_list:
          if q['id'] not in previous_questions:
            random_q = q
            break
          elif counter == len(formatted_questions_list):
            random_q = random.choice(formatted_questions_list)
            break
          counter += 1
      else:
        random_q = random.choice(formatted_questions_list)

    else:
      cat_id = quiz_category_id + 1
      questions_list = Question.query.filter(Question.category == cat_id).all()
      formatted_questions_list = [question.format() for question in questions_list]

      # Loop to check for previous questions
      counter = 1
      random_q = {}

      if len(previous_questions) > 0:
        for q in formatted_questions_list:
          if q['id'] not in previous_questions:
            random_q = q
            break
          elif counter == len(formatted_questions_list):
            random_q = random.choice(formatted_questions_list)
            break
          counter += 1
      else:
        random_q = random.choice(formatted_questions_list)

    return jsonify({
      'success': True,
      'quizCategory': 'ALL' if quiz_category_type == 'click' else quiz_category_type,
      'previous_questions': previous_questions,
      'question': random_q
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