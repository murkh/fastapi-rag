# FastAPI RAG Application

A robust FastAPI-based Retrieval-Augmented Generation (RAG) application that combines document storage, vector embeddings, and OpenAI's language models to provide intelligent document querying capabilities.

## Features

- Document processing and chunking
- Vector embeddings generation using OpenAI
- PostgreSQL with pgvector for vector similarity search
- Streaming responses for real-time AI interactions
- Asynchronous API design
- Structured logging system
- Environment-based configuration

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with pgvector extension
- **ORM**: SQLAlchemy with async support
- **Vector Embeddings**: OpenAI
- **Language Model**: OpenAI GPT
- **Dependencies Management**: Poetry

## Prerequisites

- Python 3.11 or higher
- PostgreSQL with pgvector extension installed
- OpenAI API key
- Poetry for dependency management

## Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/fastapi-rag.git
cd fastapi-rag
```

2. Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/rag"
OPENAI_API_KEY="your-openai-api-key"
```

3. Install dependencies:

```bash
poetry install
```

4. Set up the PostgreSQL database:
   - Create a database named 'rag'
   - Enable the pgvector extension

## Running the Application

1. Activate the poetry environment:

```bash
poetry shell
```

2. Start the FastAPI server:

```bash
uvicorn src.app.main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Document Management

- **POST** `/v1/rag/documents`
  - Upload and process documents
  - Generates embeddings and stores in the vector database

### Query Interface

- **POST** `/v1/rag/query`
  - Query the RAG system with streaming response
  - Parameters:
    - `question`: The query text
    - `top_k`: Number of most relevant chunks to retrieve (default: 3)

## Project Structure

```
src/
├── app/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration management
│   │   ├── db/          # Database setup and models
│   │   ├── logger.py    # Logging configuration
│   │   ├── middleware.py # Request/Response middleware
│   │   └── setup.py     # Application setup
│   ├── models/          # Data models
│   └── services/        # Business logic
```

## Development

The project uses Poetry for dependency management. To add new dependencies:

```bash
poetry add package-name
```

## Logging

Logs are stored in the `src/app/logs` directory:

- `app.log`: General application logs
- `error.log`: Error-specific logs

## Error Handling

The application includes comprehensive error handling and logging through middleware. All requests are logged with timing information and error tracking.
