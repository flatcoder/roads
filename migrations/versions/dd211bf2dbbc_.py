"""empty message

Revision ID: dd211bf2dbbc
Revises: acb3601a294c
Create Date: 2019-04-11 15:34:17.029634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd211bf2dbbc'
down_revision = 'acb3601a294c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('traffic_counts_cp_key', 'traffic_counts', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('traffic_counts_cp_key', 'traffic_counts', ['cp'])
    # ### end Alembic commands ###