from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from shop.errors import AppError
from shop.routes import orders

app = FastAPI(title="Orders service")
app.include_router(orders.router)


@app.exception_handler(AppError)
def handle_app_error(_request: Request, error: AppError) -> JSONResponse:
    return JSONResponse(status_code=error.status_code, content={"error": error.message})
