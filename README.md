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

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.