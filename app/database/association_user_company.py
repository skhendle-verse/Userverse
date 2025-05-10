from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class AssociationUserCompany(BaseModel):
    __tablename__ = "association_user_company"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"), primary_key=True)
    role_name = Column(String(256), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id", "role_name"],
            ["role.company_id", "role.name"],
            ondelete="CASCADE",
        ),
    )

    user = relationship("User", back_populates="companies")
    company = relationship("Company", back_populates="users")
    role = relationship("Role", back_populates="users")
