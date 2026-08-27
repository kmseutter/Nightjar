from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
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

class UserOrganizationLink(SQLModel, table=True):
    __tablename__ = "users_to_orgs"
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    org_id: int | None = Field(default=None, foreign_key="organizations.id", primary_key=True)