from fastapi import FastAPI
from routers import home, users
from db.models import Base,engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(users.router)

from sqladmin import Admin
from db.admin import UserAdmin, ProfileAdmin, ChannelAdmin, APICredentialsAdmin

admin = Admin(app, engine)

# Register admin models
admin.add_view(UserAdmin)
admin.add_view(ProfileAdmin)
admin.add_view(ChannelAdmin)
admin.add_view(APICredentialsAdmin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)