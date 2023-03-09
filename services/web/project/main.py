from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, session
from .media import routes as routes_medias
from .tweets import routes as routes_tweets
from .users import routes as routes_users

api_router = APIRouter()
api_router.include_router(routes_tweets.router)
api_router.include_router(routes_users.router)
api_router.include_router(routes_medias.router)

app = FastAPI()
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test1():
    return {"id": 1, "name": "sasa"}


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()
