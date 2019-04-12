"""empty message

Revision ID: eee38c2a81f9
Revises: 1929bfab19a6
Create Date: 2019-04-12 19:22:42.319422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eee38c2a81f9'
down_revision = '1929bfab19a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('links', sa.Column('cp', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'links', ['cp'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'links', type_='unique')
    op.drop_column('links', 'cp')
    # ### end Alembic commands ###