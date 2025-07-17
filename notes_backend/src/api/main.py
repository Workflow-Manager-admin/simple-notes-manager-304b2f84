from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from starlette.responses import JSONResponse

from .routers import notes

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = FastAPI(
    title="Notes Management FastAPI Application",
    description="A simple FastAPI backend for managing notes with full CRUD endpoints.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Health check endpoint"},
        {"name": "Notes", "description": "Operations with notes (CRUD)"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health Check", description="Basic health check endpoint.")
# PUBLIC_INTERFACE
def health_check():
    """Returns a simple JSON confirming the service is running."""
    return {"message": "Healthy"}


app.include_router(notes.router)

# Customized validation error handler (optional, for more user-friendly errors)
@app.exception_handler(ValueError)
def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )
