from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str | None = None
    email: str | None = None
    address: str | None = None
    phone: str | None = None

class Organizations(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Roles(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str

class Permissions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    permission: str

########class Users_to_Orgs(SQLModel, table=True):
    
