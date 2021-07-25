from pydantic import BaseModel

class OrmMode(BaseModel):

    class Config:
        orm_mode = True

class UserSchema(OrmMode):
    username: str

class UserCreateSchema(UserSchema):
    password: str

class UserDBSchema(UserSchema):
    id: int
    hashed_password: str
