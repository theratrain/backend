# Training Platform API

A FastAPI-based backend for a training platform that manages users, sessions, and analysis data.

## Project Structure

```
training_platform/
├── app/
│ ├── api/ # API endpoints
│ ├── core/ # Core configurations
│ ├── db/ # Database sessions and configs
│ ├── models/ # SQLAlchemy models
│ └── schemas/ # Pydantic schemas
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd training_platform
```

2. Create a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```


## Configuration

The application uses a SQLite database by default. The database file (`training.db`) will be automatically created in the root directory when you first run the application.

You can modify the configuration in `app/core/config.py` if needed.

## Running the Application

1. Start the server:

```bash
uvicorn app.main:app --reload
```

2. The API will be available at:
- API: `http://localhost:8000`
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get specific user
