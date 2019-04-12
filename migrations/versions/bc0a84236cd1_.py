"""empty message

Revision ID: bc0a84236cd1
Revises: dd211bf2dbbc
Create Date: 2019-04-11 20:34:22.266971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc0a84236cd1'
down_revision = 'dd211bf2dbbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('traffic_counts', sa.Column('total_vehicles', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('traffic_counts', 'total_vehicles')
    # ### end Alembic commands ###