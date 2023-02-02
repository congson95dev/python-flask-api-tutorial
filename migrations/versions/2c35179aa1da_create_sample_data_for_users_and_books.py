"""create sample data for users and books

Revision ID: 2c35179aa1da
Revises: 73ed3f7bede2
Create Date: 2023-02-02 15:38:22.313786

"""

from alembic import op
from sqlalchemy import column, table, String, Integer
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = '2c35179aa1da'
down_revision = 'd7ac43aff94d'
branch_labels = None
depends_on = None

password = generate_password_hash('123456')

USERS_DATA = f"""
(1,'email1@gmail.com','user1','{password}'),
(2,'email2@gmail.com','user2','{password}'),
(3,'email3@gmail.com','user3','{password}'),
(4,'email4@gmail.com','user4','{password}'),
(5,'email5@gmail.com','user5','{password}')
"""

BOOKS_DATA = (
    ('book 1', 1, 100, 'good', 4),
    ('book 2', 2, 200, 'bad', 3),
    ('book 3', 3, 300, 'ok', 5),
    ('book 4', 4, 400, 'good', 2),
    ('book 5', 5, 500, 'great', 1)
)


# There's 2 ways to add sample data to the db throught migration
# First way, use op.execute to run direct sql command
# With this way, it can be update or ignore if there's duplicated records
# Second way, use bulk_insert of alembic to insert multiple records
# But with this 2nd way, it can't be update or ignore if there's duplicated records
# If there's duplicated records, the command `flask db upgrade` will throw error
def upgrade():
    # Insert users data using op.execute
    op.execute(
        f"""
                INSERT INTO users
                VALUES {USERS_DATA}
                ON CONFLICT DO NOTHING;

                SELECT setval('users_id_seq', (SELECT MAX(id) from users), true);
            """
    )

    # Insert books data using bulk_insert
    books = table(
        "books",
        column("title", String),
        column("author_id", Integer),
        column("pages_num", Integer),
        column("review", String),
        column("created_by", Integer),
    )
    op.bulk_insert(
        books,
        [
            {
                "title": record[0],
                "author_id": record[1],
                "pages_num": record[2],
                "review": record[3],
                "created_by": record[4]
            }
            for record in BOOKS_DATA
        ],
    )


def downgrade():
    pass
