from http.client import HTTPException
import secrets
from datetime import datetime, timedelta
from unittest.mock import Base

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from streamlit import status

from .crud import is_email_allowed

from .database import get_db
import resend


from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
#from passlib.context import CryptContext
import secrets
import os

from . import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 24 hours

# New: Magic link tokens
class MagicLinkToken(Base):
    __tablename__ = "magic_links"
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)

def create_magic_link(db: Session, email: str):
    #email = email.lower().strip()
    print('email '+email)
    if not is_email_allowed(db, email):
        raise HTTPException(403, "Domain not allowed")
    
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=15)
    db_token = MagicLinkToken(email=email.lower(), token=token, expires_at=expires)
    db.add(db_token)
    db.commit()
    alert('committed')
    # Send email via Resend
    link = f"https://yourapp.com/auth/magic?token={token}"
    resend.Emails.send({
        "from": "Neighboride <no-reply@yourapp.com>",
        "to": email,
        "subject": "Login to Neighboride",
        "html": f"<p>Click to log in: <a href='{link}'>Sign In</a></p><p>Link expires in 15 minutes.</p>"
    })
    return {"message": "Magic link sent"}

    
    
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user