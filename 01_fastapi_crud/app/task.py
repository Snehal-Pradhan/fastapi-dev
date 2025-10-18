from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from app.routers import tasks
from app.exceptions import CSVError


app = FastAPI()

@app.exception_handler(CSVError)
async def csv_exception_handler(request: Request, exc: CSVError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "CSV file error", "details": exc.message},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "An unexpected error occurred",
            "error": str(exc),
            "path": str(request.url)
        },
    )

app.include_router(tasks.router)
