# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

If on Windows, use 'set' instead of 'export':

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns:

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET '/questions'

- Fetches all questions with pagination (every 10 questions). It returns a list of questions, categories, current category and total # of questions
- Request Arguments: None
- Returns: 

```
{
  "questions": [
    {
      "answer": "[Answer #5]",
      "category": 4
      "difficulty": 2,
      "id": 5,
      "question": "[Question #5]"
    },
    {
      "answer": "[Answer #9]",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "[Question #9]"
    },
    {
      "answer": "[Answer #7]",
      "category": 3,
      "difficulty": 2,
      "id": 7,
      "question": "[Question #7]"
    },
  ],
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": None,
  "total_questions": 3,
  "success": true
}
```

### DELETE '/questions/<int:id>'

- Deletes a question by question ID. If successful, the response will return the total # of questions remaining, list of all remaining questions with pagination and the ID of the deleted question
- Request Arguments: `id` (i.e. Question ID)

```
{
    "id": 10
  }
}
```

- Returns: 

```
{
  "questions": [
    {
      "answer": "[Answer #5]",
      "category": 4
      "difficulty": 2,
      "id": 5,
      "question": "[Question #5]"
    },
    {
      "answer": "[Answer #9]",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "[Question #9]"
    },
    {
      "answer": "[Answer #7]",
      "category": 3,
      "difficulty": 2,
      "id": 7,
      "question": "[Question #7]"
    },
  ],
  "deleted": 4,
  "total_questions": 3,
  "success": true
}
```

### POST '/questions'

- Performs two functions: 1) To create a new question and 2) To get questions based on a search term 
- For #1 (To create a new question), it requires the question, answer text, category and difficulty score to be submitted. After submission, the new question will be included in the response
- For #2 (To get questions based on a search term), it requires the ***searchTerm*** to be included. When submitted, the code will get questions based on the search term and return any questions for whom the search term 
  is a substring of the question.
- Request Arguments: None

- For #1, returns: 

```
{
  "questions": [
    {
      "answer": "[Answer #5]",
      "category": 4
      "difficulty": 2,
      "id": 5,
      "question": "[Question #5]"
    },
    {
      "answer": "[Answer #9]",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "[Question #9]"
    },
    {
      "answer": "[Answer #7]",
      "category": 3,
      "difficulty": 2,
      "id": 7,
      "question": "[Question #7]"
    },
  ],
  "total_questions": 20,
  "created": 21,
  "success": true
}
```

- For #2, returns: 

```
{
  "questions": [
    {
      "answer": "[Answer #5]",
      "category": 4
      "difficulty": 2,
      "id": 5,
      "question": "[Question #5]"
    },
    {
      "answer": "[Answer #9]",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "[Question #9]"
    },
    {
      "answer": "[Answer #7]",
      "category": 3,
      "difficulty": 2,
      "id": 7,
      "question": "[Question #7]"
    },
  ],
  "total_questions": 20,
  "success": true
}
```

### GET '/categories/<int:id>/questions'

- Get questions based on category. Returns only questions of the category to be shown
- Request Arguments: `id` (i.e. Categories ID)
```
{
    "id": 3
}
```
- Returns: 

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "[Answer #5]",
      "category": 4
      "difficulty": 2,
      "id": 5,
      "question": "[Question #5]"
    },
    {
      "answer": "[Answer #9]",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "[Question #9]"
    },
    {
      "answer": "[Answer #7]",
      "category": 3,
      "difficulty": 2,
      "id": 7,
      "question": "[Question #7]"
    },
  ],
  "total_questions": 20,
  "current_category": Art,
  "success": true
}
```

### POST '/quizzes'

- To get questions to play the quiz. Each question is returned at random.
- Request Arguments: `quiz_category`

```
{
  "quiz_category": {
    "id": 1
  }
}
```

- Returns: 

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "question": {
    "answer": "[Answer]",
    "category": 1,
    "difficulty": 3,
    "id": 15,
    "question": "[Question]"
  },
  "quizCategory": "Science",
  "success": true
}
```

## Errors

### Not Found (404)

```
{
  'success': false,
  'error': 404,
  'message': 'Not found'
}
```

### Unprocessable request (422)

```
{
  'success': false,
  'error': 422,
  'message': 'Unable to process request'
}
```

### Bad Request (400)

```
{
  'success': false,
  'error': 400,
  'message': 'Bad request'
}
```

### Internal server error (500)

```
{
  'success': false,
  'error': 500,
  'message': 'Internal server error'
}
```

### Method Not Allowed (405)

```
{
  'success': false,
  'error': 405,
  'message': 'Method Not Allowed'
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```