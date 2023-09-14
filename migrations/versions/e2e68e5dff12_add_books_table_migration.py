"""add books table migration

Revision ID: e2e68e5dff12
Revises: 11477840a344
Create Date: 2023-01-31 15:59:46.203171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e2e68e5dff12"
down_revision = "11477840a344"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("author", sa.String(length=80), nullable=False),
        sa.Column("pages_num", sa.Integer(), nullable=False),
        sa.Column("review", sa.Text(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("author"),
        sa.UniqueConstraint("title"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("books")
    # ### end Alembic commands ###
