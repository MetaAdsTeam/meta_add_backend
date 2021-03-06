"""nullable

Revision ID: 5ca1d84fd129
Revises: 0c8c410a4a57
Create Date: 2022-02-08 14:25:09.201749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca1d84fd129'
down_revision = '0c8c410a4a57'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('creatives', 'url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('playbacks', 'adspot_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('playbacks', 'timeslot_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('playbacks', 'creative_id',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade():
    op.alter_column('playbacks', 'creative_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('playbacks', 'timeslot_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('playbacks', 'adspot_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('creatives', 'url',
               existing_type=sa.VARCHAR(),
               nullable=False)
