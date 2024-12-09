# app/schemas/license.py
from pydantic import BaseModel, Field
from datetime import date

class LicenseBase(BaseModel):
    key: str = Field(..., description="Унікальний ключ ліцензії")
    expiration_date: date = Field(..., description="Дата закінчення дії ліцензії")
    is_active: bool = True

class LicenseCreate(LicenseBase):
    pass

class LicenseRead(LicenseBase):
    id: int
    
    class Config:
        orm_mode = True