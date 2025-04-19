from pydantic import BaseModel, Field, field_validator


class UserRegister(BaseModel):
    first_name: str = Field(..., json_schema_extra={"example": "John"})
    last_name: str = Field(..., json_schema_extra={"example": "Doe"})
    username: str = Field(..., json_schema_extra={"example": "johndoe"})
    password: str = Field(..., json_schema_extra={"example": "mypassword"})
    role: str = Field("user", json_schema_extra={"example": "user"})

    @field_validator("first_name")
    def first_name_must_be_valid(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("First name cannot be empty")
        if not value[0].isupper():
            raise ValueError("First name must start with an uppercase letter")
        if not value.isalpha():
            raise ValueError("First name must contain only alphabetic characters")
        return value

    @field_validator("last_name")
    def last_name_must_be_valid(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Last name cannot be empty")
        if not value[0].isupper():
            raise ValueError("Last name must start with an uppercase letter")
        if not value.isalpha():
            raise ValueError("Last name must contain only alphabetic characters")
        return value

    @field_validator("username")
    def username_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value

    @field_validator("password")
    def password_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password cannot be empty")
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value

    @field_validator("role")
    def role_must_be_valid(cls, value: str) -> str:
        allowed_roles = {"user", "admin", "read_only"}
        if value not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return value


class UserLogin(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "johndoe"})
    password: str = Field(..., json_schema_extra={"example": "mypassword"})

    @field_validator("username")
    def username_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value

    @field_validator("password")
    def password_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password cannot be empty")
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class ConfigDict:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
