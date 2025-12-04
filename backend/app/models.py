from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String)
    hashed_password = Column(String)
    is_driver = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=5.0)
    expo_push_token = Column(String) # For mobile alerts

    #subscription = relationship("UserSubscription")
    rides_offered = relationship("Ride", back_populates="driver")
    bookings = relationship("Booking", back_populates="passenger")
    #reviews_given = relationship("Review", foreign_keys="Review.reviewer_id")
    #reviews_received = relationship("Review", foreign_keys="Review.reviewed_id")
    #wallet = relationship("DriverWallet")

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String)
    price_monthly = Column(Float)
    max_rides_per_month = Column(Integer, default=5)
    priority_matching = Column(Boolean, default=False)

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"))
    stripe_subscription_id = Column(String)
    status = Column(String, default="active")
    current_period_end = Column(DateTime)

class Ride(Base):
    __tablename__ = "rides"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    origin = Column(String)
    destination = Column(String)
    #origin_lat = Column(Float)
    #origin_lng = Column(Float)
    #dest_lat = Column(Float)
    #dest_lng = Column(Float)
    #departure_time = Column(DateTime)
    #available_seats = Column(Integer)
    #price_per_seat = Column(Float)
    #status = Column(String, default="open")
    #stripe_payment_intent = Column(String)
    #surge_multiplier = Column(Float, default=1.0)

    driver = relationship("User", back_populates="rides_offered")
    bookings = relationship("Booking", back_populates="ride")

class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ride_id = Column(Integer, ForeignKey("rides.id"))
    passenger_id = Column(Integer, ForeignKey("users.id"))
    seats_booked = Column(Integer)
    status = Column(String, default="pending")

    ride = relationship("Ride", back_populates="bookings")
    passenger = relationship("User", back_populates="bookings")

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    reviewed_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(Text)

class DriverWallet(Base):
    __tablename__ = "driver_wallets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Float, default=0.0)
    total_earned = Column(Float, default=0.0)

class Referral(Base):
    __tablename__ = "referrals"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_id = Column(Integer, ForeignKey("users.id"))
    credit_given = Column(Boolean, default=False)

class DriverIncentive(Base):
    __tablename__ = "driver_incentives"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    amount = Column(Float)
    date = Column(DateTime)
    claimed = Column(Boolean, default=False)

# Add this new model
class AllowedDomain(Base):
    __tablename__ = "allowed_domains"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    domain = Column(String, unique=True, index=True) # e.g., "wellsfargo.com"
    company_name = Column(String) # "Wells Fargo"
    is_active = Column(Boolean, default=True)
    added_by_admin = Column(Boolean, default=True)
