"""removed timeslots.adspot_id

Revision ID: febe27bfff1e
Revises: c7d2bf420110
Create Date: 2022-02-01 14:01:02.767186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'febe27bfff1e'
down_revision = 'c7d2bf420110'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('publishers', 'service_ref',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint('timeslots_adspot_id_fkey', 'timeslots', type_='foreignkey')
    op.drop_column('timeslots', 'adspot_id')


def downgrade():
    op.add_column('timeslots', sa.Column('adspot_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('timeslots_adspot_id_fkey', 'timeslots', 'adspots', ['adspot_id'], ['id'])
    op.alter_column('publishers', 'service_ref',
               existing_type=sa.VARCHAR(),
               nullable=True)
