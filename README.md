# Tarot Reading API

A RESTful API for tarot card readings, built with Flask and deployed on Render.

## Features

- Authentication with Auth0
- Role-based access control
- Search for tarot cards by ID
- Get tarot readings based on different spreads
- Save, retrieve, and delete readings
- Edit the question for the reading
- View user's reading history

## Technologies Used

- Flask
- PostgreSQL
- SQLAlchemy
- Postman (for API testing)
- Auth0 (for authentication)
- Render (for deployment)

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/tarot-reading-api.git
cd tarot-reading-api
```

2. Set up a virtual environment:
```
python3 -m venv venv
```

3. Activate the virtual environment:

- On macOS and Linux:
```
source venv/bin/activate
```

- On Windows:
```
Copyvenv\Scripts\activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Set up your environment variables (database URL, Auth0 credentials, etc.). Refer to [auth_config.sh](/Users/Angelica/Documents/Coding/Udacity/full-stack-nanodegree/tarot-api/auth_config.sh).

6. Initialize the database:
```
flask db upgrade
```

7. Run the application:
```
FLASK_APP=run.py FLASK_ENV=development flask run
```

8. To deactivate the virtual environment when you're done:
```
deactivate
```

Make sure you have Python 3.7 or later installed on your system before starting the installation process.

## API Documentation

### Authentication

- `GET /auth/login`: Initiates the login process
- `GET /auth/callback`: Handles the Auth0 callback after login
- `GET /auth/logout`: Logs out the user

### Cards

- `GET /cards/<int:card_id>`: Retrieve a specific tarot card by ID

### Spreads

- `GET /spreads/<int:spread_id>`: Get information about a specific spread
- `POST /spreads/<int:spread_id>`: Perform a tarot reading using the specified spread

### Readings

- `GET /readings/`: Retrieve all readings for the authenticated user
- `GET /readings/<int:id>`: Retrieve a specific reading by ID
- `PATCH /readings/<int:reading_id>/question`: Update the question for a specific reading
- `DELETE /readings/<int:reading_id>`: Delete a specific reading

## Usage Examples

Here are some example API calls using curl:

1. Retrieve a card:
   ```
   curl -X GET "http://your-api-url/cards/1" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

2. Perform a reading:
   ```
   curl -X POST "http://your-api-url/spreads/1" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"question": "What does my future hold?"}'
   ```

3. Retrieve all readings:
   ```
   curl -X GET "http://your-api-url/readings/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## Live API URL
The API is accessible at: https://tarot-api-shar.onrender.com

To try the endpoints in the live version you can use the accounts
- free_user@oracle.com
- premium_user@oracle.com

**password:** test_oracle123

## Endpoints
Here are the main endpoints of the API:

Get a specific card:
GET https://tarot-api-shar.onrender.com/api/cards/<card_id>
Perform a reading:
POST https://tarot-api-shar.onrender.com/api/spreads/<spread_id>
Retrieve all readings:
GET https://tarot-api-shar.onrender.com/api/readings/
Get a specific reading:
GET https://tarot-api-shar.onrender.com/api/readings/<reading_id>
Update a reading's question:
PATCH https://tarot-api-shar.onrender.com/api/readings/<reading_id>/question
Delete a reading:
DELETE https://tarot-api-shar.onrender.com/api/readings/<reading_id>


## Authentication

### Please refer to [auth_config.sh](/Users/Angelica/Documents/Coding/Udacity/full-stack-nanodegree/tarot-api/auth_config.sh) for tokens or go through signin flow.

This API uses Auth0 for authentication. To access protected endpoints, you need to include a valid JWT token in the Authorization header:
CopyAuthorization: Bearer YOUR_ACCESS_TOKEN
Usage Examples
Here are some example API calls using curl:

Retrieve a card:
Copycurl -X GET "https://tarot-api-shar.onrender.com/api/cards/1" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Perform a reading:
Copycurl -X POST "https://tarot-api-shar.onrender.com/api/spreads/1" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"question": "What does my future hold?"}'

Retrieve all readings:
Copycurl -X GET "https://tarot-api-shar.onrender.com/api/readings/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"


Replace YOUR_ACCESS_TOKEN with a valid access token obtained through the authentication process.

## Running Tests
To run the tests for this project, follow these steps:

1. Ensure you have activated your virtual environment (if you haven't already):
```
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

2. Install test dependencies (if you haven't already):
```
pip install -r requirements-dev.txt
```

3. Set up your test environment variables:
```
export FLASK_ENV=testing  # On macOS/Linux
set FLASK_ENV=testing     # On Windows
```

4. Run the tests using pytest:
```
pytest
```

5. To run tests with coverage report:
```
pytest --cov=app --cov-report=term-missing
```

6. To run a specific test file:
```
pytest tests/path_to_test_file.py
```

7. To run a specific test function:
```
pytest tests/path_to_test_file.py::test_function_name
```

Note: Make sure you're in the root directory of the project when running these commands.
