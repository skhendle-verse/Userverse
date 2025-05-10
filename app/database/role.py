from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from .base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "role"

    company_id = Column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), primary_key=True
    )
    name = Column(String(256), primary_key=True)
    description = Column(String(256), nullable=True)

    company = relationship("Company", back_populates="roles", overlaps="users")
    users = relationship(
        "AssociationUserCompany", back_populates="role", overlaps="company,users"
    )

    @classmethod
    def update_role(
        cls,
        session,
        company_id: int,
        name: str,
        new_name: str = None,
        new_description: str = None,
    ) -> dict:
        """
        Update a role's name and/or description using the composite key (company_id, name).
        """
        try:
            role = session.query(cls).filter_by(company_id=company_id, name=name).one()

            if new_name:
                role.name = new_name
            if new_description:
                role.description = new_description

            session.commit()
            return cls.to_dict(role)

        except NoResultFound:
            raise ValueError(
                f"Role with company_id={company_id} and name='{name}' not found."
            )
