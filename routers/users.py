from fastapi import APIRouter

router= APIRouter(prefix="/api/users")

@router.get("/")
async def login():
    return {"message": "List of users"}

async def logout():
    return {"message": "User logged out"}


async def register():
    return {"message": "User registered successfully"}
