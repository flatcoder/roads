"""empty message

Revision ID: e4c8175b5355
Revises: eee38c2a81f9
Create Date: 2019-05-09 19:56:17.915411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4c8175b5355'
down_revision = 'eee38c2a81f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('traffic_counts', 'total_all')
    op.drop_column('traffic_counts', 'total_hgv')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('traffic_counts', sa.Column('total_hgv', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('traffic_counts', sa.Column('total_all', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
