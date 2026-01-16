from pydantic import BaseModel, EmailStr, Field

class OTPRequestIn(BaseModel):
    email: EmailStr

class OTPVerifyIn(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
    role: str = "buyer"  # buyer/seller/admin (admin normalmente solo por DB)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
