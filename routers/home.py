from fastapi import APIRouter

router= APIRouter(prefix="/api")

@router.get("/home")
async def home():
    return {"message": "Welcome to the Home Page!"}