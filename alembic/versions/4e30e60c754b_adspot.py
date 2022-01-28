"""adspot

Revision ID: 4e30e60c754b
Revises: a4514cd9a264
Create Date: 2022-01-25 17:29:40.075653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e30e60c754b'
down_revision = 'a4514cd9a264'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('adspots',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('adspot_type_id', sa.Integer(), nullable=True),
    sa.Column('ad_metadata', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('adspots')
