"""create roles table
Revision ID: eee69d619ee5
Revises: 56d1e5d875d3
Create Date: 2021-07-06 21:09:58.949452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'eee69d619ee5'
down_revision = '56d1e5d875d3'
branch_labels = None
depends_on = None

def create_roles_table() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("role", sa.String, nullable=False, index=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    )

def upgrade() -> None:
    create_roles_table()

def downgrade() -> None:
    pass
