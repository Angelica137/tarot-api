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

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables (database URL, Auth0 credentials, etc.)

4. Initialize the database:
   ```
   flask db upgrade
   ```

5. Run the application:
   ```
   flask run
   ```

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

# Live API URL
The API is accessible at: https://tarot-api-shar.onrender.com

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


# Authentication

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