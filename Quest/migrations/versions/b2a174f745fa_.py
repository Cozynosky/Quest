"""empty message

Revision ID: b2a174f745fa
Revises: b72a40d819f4
Create Date: 2021-12-10 14:34:52.294529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2a174f745fa'
down_revision = 'b72a40d819f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('table_reservations', sa.Column('first_name', sa.String(length=250), nullable=False))
    op.add_column('table_reservations', sa.Column('last_name', sa.String(length=250), nullable=False))
    op.add_column('table_reservations', sa.Column('phone', sa.String(length=9), nullable=False))
    op.add_column('table_reservations', sa.Column('message', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('table_reservations', 'message')
    op.drop_column('table_reservations', 'phone')
    op.drop_column('table_reservations', 'last_name')
    op.drop_column('table_reservations', 'first_name')
    # ### end Alembic commands ###
