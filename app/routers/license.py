# app/routers/license.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.license import LicenseCreate, LicenseRead
from app.models.license_model import License, Base
from app.database import get_db

router = APIRouter(
    prefix="/licenses",
    tags=["licenses"]
)

@router.get("/", response_model=list[LicenseRead])
async def list_licenses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(License))
    licenses = result.scalars().all()
    return licenses

@router.post("/", response_model=LicenseRead)
async def create_license(license_data: LicenseCreate, db: AsyncSession = Depends(get_db)):
    new_license = License(**license_data.dict())
    db.add(new_license)
    await db.commit()
    await db.refresh(new_license)
    return new_license