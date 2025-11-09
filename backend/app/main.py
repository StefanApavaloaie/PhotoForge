from fastapi import FastAPI
from .routers import images


app = FastAPI()
@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(images.router)