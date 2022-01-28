"""advertiser

Revision ID: aeb776c470c4
Revises: 961df91a870c
Create Date: 2022-01-28 16:41:05.245510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeb776c470c4'
down_revision = '961df91a870c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('advertisers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('advertiser')
