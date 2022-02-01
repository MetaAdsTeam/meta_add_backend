"""publish_url, path

Revision ID: 8722a94ae8d1
Revises: febe27bfff1e
Create Date: 2022-02-01 18:04:12.256985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8722a94ae8d1'
down_revision = 'febe27bfff1e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('adspot_types', sa.Column('publish_url', sa.String(), nullable=False, server_default=''))
    op.add_column('creatives', sa.Column('path', sa.String(), nullable=False, server_default=''))


def downgrade():
    op.drop_column('creatives', 'path')
    op.drop_column('adspot_types', 'publish_url')
