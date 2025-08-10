import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).resolve().parent))
from src.api.Hotels import router as hotels_router
app = FastAPI()
app.include_router(hotels_router)



if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
