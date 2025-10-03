from fastapi import FastAPI

from to_the_hell.oncallhub.api.routers import auth, duties, incidents

app = FastAPI(
    title="OnCall Hub",
    description="DevOps team duty management system",
    version="0.1.0",
)


@app.get("/")
async def welcome() -> dict[str, str]:
    """Root endpoint of the application"""
    return {"message": "my best project"}


app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(duties.router, prefix="/duties", tags=["duties"])
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
