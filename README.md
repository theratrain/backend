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