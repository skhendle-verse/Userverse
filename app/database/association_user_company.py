from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.exc import NoResultFound
from .base_model import BaseModel


class AssociationUserCompany(BaseModel):
    __tablename__ = "association_user_company"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"), primary_key=True)
    user_level = Column(String(255))
    # A user can be associated with multiple companies
    user = relationship("User", back_populates="companies")
    # A company can have multiple users
    company = relationship("Company", back_populates="users")

    @classmethod
    def get_user_by_email(cls, session: Session, email: str) -> dict:
        try:
            agent = session.query(cls).filter_by(email=email).one()
            return agent
        except NoResultFound:
            raise ValueError(f"User with email:{email}, not found.")
