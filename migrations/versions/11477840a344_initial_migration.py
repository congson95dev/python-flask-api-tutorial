"""Initial migration.

Revision ID: 11477840a344
Revises:
Create Date: 2022-06-07 10:34:34.064226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "11477840a344"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=80), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
