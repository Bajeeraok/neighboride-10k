# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ── User Schemas ───────────────────────
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_driver: bool = False
    is_verified: bool = False
    rating: float = 5.0
    created_at: datetime

    class Config:
        from_attributes = True


# ── Auth / Token ───────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# ── Allowed Domain ─────────────────────
class AllowedDomainBase(BaseModel):
    domain: str = Field(..., description="e.g. wellsfargo.com")
    company_name: Optional[str] = None


class AllowedDomainCreate(AllowedDomainBase):
    pass


class AllowedDomain(AllowedDomainBase):
    id: int
    is_active: bool = True
    added_by_admin: bool = True

    class Config:
        from_attributes = True


# ── Ride Schemas ───────────────────────
class RideBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    available_seats: int = Field(..., ge=1, le=6)
    price_per_seat: float = Field(..., gt=0)


class RideCreate(RideBase):
    pass


class Ride(RideBase):
    id: int
    driver_id: int
    origin_lat: Optional[float]
    origin_lng: Optional[float]
    dest_lat: Optional[float]
    dest_lng: Optional[float]
    status: str = "open"
    surge_multiplier: float = 1.0
    created_at: datetime

    class Config:
        from_attributes = True


# ── Booking Schemas ───────────────────
class BookingBase(BaseModel):
    ride_id: int
    seats_booked: int = Field(..., ge=1)


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int
    passenger_id: int
    status: str = "confirmed"
    created_at: datetime

    class Config:
        from_attributes = True


# ── Review Schemas ─────────────────────
class ReviewBase(BaseModel):
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    reviewer_id: int
    reviewed_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Wallet & Incentives ───────────────
class DriverWalletBase(BaseModel):
    balance: float = 0.0
    total_earned: float = 0.0


class DriverWallet(DriverWalletBase):
    id: int
    driver_id: int

    class Config:
        from_attributes = True


# ── Subscription Plans ─────────────────
class SubscriptionPlanBase(BaseModel):
    name: str
    price_monthly: float
    max_rides_per_month: int = 999


class SubscriptionPlan(SubscriptionPlanBase):
    id: int

    class Config:
        from_attributes = True
