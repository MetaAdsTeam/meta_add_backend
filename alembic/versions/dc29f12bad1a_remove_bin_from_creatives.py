"""remove bin from creatives

Revision ID: dc29f12bad1a
Revises: c77442353bc5
Create Date: 2022-01-31 15:47:27.690011

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dc29f12bad1a'
down_revision = 'c77442353bc5'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('creatives', 'nft_bin')


def downgrade():
    op.add_column('creatives', sa.Column('nft_bin', postgresql.BYTEA(), autoincrement=False, nullable=False))
