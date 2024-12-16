from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.views import router as router_auth
from src.realty.views import router as router_realty
from src.user.views import router as router_user

app = FastAPI()

app.include_router(router_realty, prefix="/realtys")
app.include_router(router_auth, prefix="/auth/jwt")
app.include_router(router_user, prefix="/users")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://frontend:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-total-count"],
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
