from sqladmin import ModelView
from db.models import User, Profile, Channel, APICredentials


class UserAdmin(ModelView, model=User):
    pass


class ProfileAdmin(ModelView, model=Profile):
    pass


class ChannelAdmin(ModelView, model=Channel):
    pass


class APICredentialsAdmin(ModelView, model=APICredentials):
    pass