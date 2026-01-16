from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway")

# ✅ CORS CORRECTO (ESTO ES CLAVE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=False,                  # importante
    allow_methods=["*"],                      # incluye OPTIONS
    allow_headers=["*"],                      # Authorization, Content-Type
)

# importar routers
from app.routes.proxy import router as proxy_router
from app.routes.admin_users_proxy import router as admin_router
from app.routes.auth_proxy import router as auth_router

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(proxy_router)
