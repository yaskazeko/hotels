import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).resolve().parent))
from src.api.auth import router as auth_router
from src.api.Hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)


if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
