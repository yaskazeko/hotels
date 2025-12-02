import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from src.init import redis_manager

sys.path.append(str(Path(__file__).resolve().parent))
from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.images import router as images_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(images_router)


if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
