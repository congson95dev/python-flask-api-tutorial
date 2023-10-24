"""update role column in user table

Revision ID: 62d0399b49a9
Revises: 3f50e2318328
Create Date: 2023-10-23 17:03:46.192592

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column

# revision identifiers, used by Alembic.
revision = "62d0399b49a9"
down_revision = "3f50e2318328"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("role", sa.Integer(), nullable=True))
    role = table("users", column("role"))
    op.execute(role.update().values(role=1))
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Integer(),
        nullable=False,
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "role")
    # ### end Alembic commands ###
