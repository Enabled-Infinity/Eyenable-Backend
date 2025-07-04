from fastapi import FastAPI
from routers import home
import uvicorn
app= FastAPI()

app.include_router(home.router)



if __name__ == "__main__":
    uvicorn.run(app)