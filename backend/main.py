from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import processor
from app.api.v1 import health
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Set log levels for application loggers
logging.getLogger("app").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app = FastAPI(
    title="Incident Report Backend",
    version="0.1.0",
    description="Incident Report Backend for AskEmma take home",
)

app.include_router(processor.router)
app.include_router(health.router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

