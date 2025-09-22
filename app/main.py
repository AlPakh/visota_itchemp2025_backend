from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RoadLab API")

# Разрешим фронтенду ходить к API (при необходимости ужесточи список origin'ов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # замени на список доменов фронтенда в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "FastAPI on Render works!"}
