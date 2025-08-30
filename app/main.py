"""FastAPI Professional Application."""

import time
import zoneinfo
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.db.db import lifespan
from app.api.deps import get_current_user
from app.api.responses import APIResponse
from app.api.exceptions import APIException
from app.models import Invoice
from .routers import customers, transactions, plans

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A professional FastAPI application with PostgreSQL",
    lifespan=lifespan,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(
    customers.router, 
    prefix=settings.api_v1_prefix,
    tags=["customers"]
)
app.include_router(
    transactions.router, 
    prefix=settings.api_v1_prefix,
    tags=["transactions"]
)
app.include_router(
    plans.router, 
    prefix=settings.api_v1_prefix,
    tags=["plans"]
)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": getattr(exc, 'error_code', None)
        }
    )


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    """Log request processing time."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.url} - Process Time: {process_time:.4f} seconds")
    return response


@app.get("/", response_model=APIResponse[dict])
async def root(current_user: Annotated[str, Depends(get_current_user)]):
    """Root endpoint with authentication."""
    return APIResponse(
        message=f"Welcome to {settings.app_name}",
        data={
            "user": current_user,
            "version": settings.app_version,
            "docs": "/docs"
        }
    )


@app.get("/health", response_model=APIResponse[dict])
async def health_check():
    """Health check endpoint."""
    return APIResponse(
        message="Application is healthy",
        data={
            "status": "healthy",
            "version": settings.app_version,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Country timezone mapping
COUNTRY_TIMEZONES = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City", 
    "AR": "America/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}", response_model=APIResponse[dict])
async def get_time_by_iso_code(iso_code: str):
    """Get current time for a country by ISO code."""
    iso = iso_code.upper()
    timezone_str = COUNTRY_TIMEZONES.get(iso)
    
    if not timezone_str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timezone not found for country code: {iso}"
        )
    
    try:
        tz = zoneinfo.ZoneInfo(timezone_str)
        current_time = datetime.now(tz)
        
        return APIResponse(
            message=f"Current time for {iso}",
            data={
                "country_code": iso,
                "timezone": timezone_str,
                "time": current_time.isoformat(),
                "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            }
        )
    except Exception as e:
        logger.error(f"Error getting time for {iso}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving time information"
        )


@app.post("/invoices", response_model=APIResponse[Invoice])
async def create_invoice(
    invoice_data: Invoice,
    current_user: Annotated[str, Depends(get_current_user)]
):
    """Create an invoice (authenticated endpoint)."""
    logger.info(f"Invoice created by user: {current_user}")
    return APIResponse(
        message="Invoice created successfully",
        data=invoice_data
    )