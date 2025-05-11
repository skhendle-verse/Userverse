from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref, Session
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

    # relationships
    role = relationship("Role", back_populates="users", overlaps="company,users")
    company = relationship("Company", back_populates="users", overlaps="role")
    user = relationship("User", back_populates="companies", overlaps="company,role")

    @classmethod
    def is_user_linked_to_company(
        cls, session: Session, user_id: int, company_id: int, role_name: str = None
    ) -> bool:
        """
        Check if a user is associated with a company, optionally filtered by role.
        """
        query = session.query(cls).filter_by(user_id=user_id, company_id=company_id)
        if role_name:
            query = query.filter_by(role_name=role_name)

        return session.query(query.exists()).scalar()
