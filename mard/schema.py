from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDb(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)


class RomancistSchema(BaseModel):
    name: str


class RomancistPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class RomancistList(BaseModel):
    romancists: list[RomancistPublic]


class BookSchema(BaseModel):
    title: str
    year: int
    romancist_id: int


class BookPublic(BaseModel):
    id: int
    title: str
    year: int
    romancist_id: int
    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    books: list[BookPublic]
