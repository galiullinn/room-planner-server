from fastapi import FastAPI

app = FastAPI(
    title="Room Planner API",
)


@app.get("/")
async def root() -> dict:
    return {"message": "Interior Planner API"}
