"""AdPlace added price field

Revision ID: 9dbf008f4608
Revises: da51784bba7c
Create Date: 2022-01-30 00:31:36.324141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dbf008f4608'
down_revision = 'da51784bba7c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ad_places', sa.Column('price', sa.Integer(), nullable=False, default=0))


def downgrade():
    op.drop_column('ad_places', 'price')
