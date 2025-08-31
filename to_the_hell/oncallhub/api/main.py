from fastapi import FastAPI

from to_the_hell.oncallhub.api.routers import duties, incidents

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "my best project"}


app.include_router(duties.router)
app.include_router(incidents.router)
