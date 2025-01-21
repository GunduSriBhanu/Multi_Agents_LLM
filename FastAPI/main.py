from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/crew_kick/{start}/{end}")
async def crew_kick(start: int, end: int):
    return {"Hello": "World", "start": start, "end": end}