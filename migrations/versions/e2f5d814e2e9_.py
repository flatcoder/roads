"""empty message

Revision ID: e2f5d814e2e9
Revises: 046d1b5b151b
Create Date: 2019-04-11 21:12:29.585542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f5d814e2e9'
down_revision = '046d1b5b151b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_road_name_combo', 'junctions', ['road', 'name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_road_name_combo', 'junctions', type_='unique')
    # ### end Alembic commands ###