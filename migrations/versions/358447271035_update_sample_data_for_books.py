"""update sample data for books

Revision ID: 358447271035
Revises: 2e2801a8582b
Create Date: 2023-02-03 10:05:59.560249

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "358447271035"
down_revision = "2e2801a8582b"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""
            UPDATE books
            SET updated_date = '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            updated_by = 1;
        """
    )
    pass


def downgrade():
    pass
