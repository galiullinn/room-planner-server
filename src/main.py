from fastapi import FastAPI

app = FastAPI(
    title="Room Planner API",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Room Planner API"}
