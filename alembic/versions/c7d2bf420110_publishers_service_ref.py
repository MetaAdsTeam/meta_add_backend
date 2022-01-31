"""publishers.service_ref

Revision ID: c7d2bf420110
Revises: dc29f12bad1a
Create Date: 2022-01-31 18:33:06.043144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7d2bf420110'
down_revision = 'dc29f12bad1a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('publishers', sa.Column('service_ref', sa.String()))


def downgrade():
    op.drop_column('publishers', 'service_ref')
