"""empty message

Revision ID: 35cbc5774a9b
Revises: 49cc9a3f5a85
Create Date: 2022-12-06 22:16:30.136990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35cbc5774a9b'
down_revision = '49cc9a3f5a85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie_items', schema=None) as batch_op:
        batch_op.drop_constraint('movie_items_actor_id_key', type_='unique')
        batch_op.drop_constraint('movie_items_movie_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie_items', schema=None) as batch_op:
        batch_op.create_unique_constraint('movie_items_movie_id_key', ['movie_id'])
        batch_op.create_unique_constraint('movie_items_actor_id_key', ['actor_id'])

    # ### end Alembic commands ###
