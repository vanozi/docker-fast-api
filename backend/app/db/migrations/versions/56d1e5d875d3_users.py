"""users
Revision ID: 56d1e5d875d3
Revises: 3e3594012902
Create Date: 2021-06-30 15:40:47.616791

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic
revision = '56d1e5d875d3'
down_revision = '3e3594012902'
branch_labels = None
depends_on = None

def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False, index=True),
        sa.Column("confirmation", UUID, nullable=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, default=False),
    )

def upgrade() -> None:
    create_users_table()


def downgrade() -> None:
    op.drop_table("users")
