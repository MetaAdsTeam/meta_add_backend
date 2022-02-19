"""added creatives.moderated

Revision ID: c1442cd73b8a
Revises: c299bf41a74f
Create Date: 2022-02-19 18:48:18.993823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1442cd73b8a'
down_revision = 'c299bf41a74f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('creatives', sa.Column('moderated', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('creatives', 'moderated')
