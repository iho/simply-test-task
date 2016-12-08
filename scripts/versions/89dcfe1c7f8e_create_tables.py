"""create tables

Revision ID: 89dcfe1c7f8e
Revises: 
Create Date: 2016-12-08 18:00:04.843620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89dcfe1c7f8e'
down_revision = None
branch_labels = None
depends_on = None


create_room_table_query = '''
CREATE TABLE IF NOT EXISTS public.room
(
    id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(300),
	theme TEXT
)
'''

create_message_table_query = '''
CREATE TABLE IF NOT EXISTS public.message
(
   id SERIAL PRIMARY KEY,
   username VARCHAR(255),
   room_id INT NOT NULL REFERENCES room(id) ON DELETE CASCADE,
   text TEXT,
   ts TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc')
)'''
def upgrade():
    op.execute(create_room_table_query)
    op.execute(create_message_table_query)


def downgrade():
    op.execute("DROP TABLE message;")
    op.execute("DROP TABLE room;")
