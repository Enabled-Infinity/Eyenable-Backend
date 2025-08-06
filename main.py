from fastapi import FastAPI
from routers import home, users
from db.models import Base,engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(users.router)

from sqladmin import Admin
admin = Admin(app, engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)