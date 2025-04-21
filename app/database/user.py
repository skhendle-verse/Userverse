from sqlalchemy import Column, JSON, String, Integer, DateTime
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.exc import NoResultFound
from .base_model import BaseModel
import datetime


class User(BaseModel):
    __tablename__="user"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)


    # # All the companies agent is linked with
    # company = relationship("CompanyUserAssociation", back_populates="user")
    
    
    @classmethod
    def get_user_by_email(cls, session: Session, email: str) -> dict:
        try:
            agent = session.query(cls).filter_by(
                email=email
            ).one()
            return agent
        except NoResultFound:
            raise ValueError(f"User with email:{email}, not found.")