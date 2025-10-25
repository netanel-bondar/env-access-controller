# Environment Access Controller

A full-stack application for managing access to QA Publishers and Staging Environments. Built with FastAPI (backend) and React + TypeScript + MUI (frontend).

## Project Structure

```
env-access-controller/
├── backend/               # FastAPI backend
│   ├── main.py           # API endpoints
│   ├── Resource.py       # Base resource class
│   ├── QAPPublisher.py   # QA Publisher resource
│   ├── StagingEnv.py     # Staging environment resource
│   ├── resources_config.py  # Resource configuration
│   └── requirements.txt  # Python dependencies
│
└── frontend/             # React + TypeScript frontend
    ├── src/
    │   ├── components/   # React components
    │   ├── services/     # API service layer
    │   ├── types/        # TypeScript types
    │   ├── App.tsx       # Main app component
    │   └── main.tsx      # Entry point
    └── package.json      # Node dependencies
```

## Features

- **Resource Management**: Take, release, and steal QA Publishers and Staging Environments
- **Real-time Updates**: Auto-refresh every 5 seconds to show latest status
- **User Detection**: Automatically detects system username
- **Material-UI**: Modern, responsive UI with MUI components
- **Toggle Controls**: Easy take/release with switch toggles
- **Steal Functionality**: Take resources from other users when needed

## Setup & Installation

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The backend will be available at: http://localhost:8000
   API documentation: http://localhost:8000/docs

### Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:3000

## Usage

1. Start both the backend and frontend servers (in separate terminals)
2. Open http://localhost:3000 in your browser
3. The app will automatically detect your username
4. View all QA Publishers and Staging Environments
5. Use the toggle switch to take/release resources (only works for your own resources)
6. Click "Steal" button to take resources from other users

## API Endpoints

### General
- `GET /health` - Health check
- `GET /api/whoami` - Get current system username
- `GET /status` - Get all resource statuses

### Publishers
- `GET /publishers` - List all publishers
- `GET /publishers/available` - List available publishers
- `POST /publishers/take/{publisher_id}?user={username}` - Take publisher
- `POST /publishers/release/{publisher_id}` - Release publisher
- `POST /publishers/steal/{publisher_id}?user={username}` - Steal publisher

### Environments
- `GET /environments` - List all environments
- `GET /environments/available` - List available environments
- `POST /environments/take/{env_name}?user={username}` - Take environment
- `POST /environments/release/{env_name}` - Release environment
- `POST /environments/steal/{env_name}?user={username}` - Steal environment

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Python 3.x**

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Material-UI (MUI)** - Component library
- **Axios** - HTTP client

## Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`
