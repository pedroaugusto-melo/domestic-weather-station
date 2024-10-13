from sqlmodel import Field, SQLModel

class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)