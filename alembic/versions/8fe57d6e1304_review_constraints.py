"""review constraints

Revision ID: 8fe57d6e1304
Revises: 81e60cacccb2
Create Date: 2022-02-17 18:13:42.013615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fe57d6e1304'
down_revision = '81e60cacccb2'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('adspots', 'publisher_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('adspots', 'spot_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('adspots_stats', 'spot_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('creatives', 'advert_id',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade():
    op.alter_column('creatives', 'advert_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('adspots_stats', 'spot_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('adspots', 'spot_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('adspots', 'publisher_id',
               existing_type=sa.INTEGER(),
               nullable=True)
