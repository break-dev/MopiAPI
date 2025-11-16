from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#
from core.settings import settings
from src.presentation.filter_exception import filter_exception
from src.presentation.routes import router

# fastapi dev app/main.py
#
# cd app
# fastapi dev main.py

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Registrar el filtro global de excepciones
filter_exception(app)


# --- Middlewares ---

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
)


# Middleware para corregir esquema HTTPS si viene tras proxy
@app.middleware("http")
async def https_scheme(request: Request, call_next):
    x_forwarded_proto = request.headers.get("X-Forwarded-Proto")
    if x_forwarded_proto and x_forwarded_proto.lower() == "https":
        request.scope["scheme"] = "https"
    response: Response = await call_next(request)
    return response


# --- Endpoints ---

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
