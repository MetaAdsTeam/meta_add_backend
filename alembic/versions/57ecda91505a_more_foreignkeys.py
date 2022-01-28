"""more ForeignKeys

Revision ID: 57ecda91505a
Revises: d149d70dcb4a
Create Date: 2022-01-28 18:51:58.754727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57ecda91505a'
down_revision = 'd149d70dcb4a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('advertisers', sa.Column('wallet_ref', sa.String(), nullable=False))
    op.alter_column('contents', 'content_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'contents', 'adspot_types', ['content_type_id'], ['id'])
    op.create_foreign_key(None, 'playbacks', 'adspots', ['adspot_id'], ['id'])
    op.create_foreign_key(None, 'playbacks', 'timeslots', ['timeslot_id'], ['id'])
    op.create_foreign_key(None, 'playbacks', 'contents', ['content_id'], ['id'])
    op.create_foreign_key(None, 'playbacks', 'advertisers', ['advert_id'], ['id'])
    op.create_foreign_key(None, 'playbacks', 'playback_statuses', ['status_id'], ['id'])
    op.add_column('publishers', sa.Column('wallet_ref', sa.String(), nullable=False))
    op.alter_column('timeslots', 'from_time',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('timeslots', 'to_time',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('timeslots', 'locked',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.create_foreign_key(None, 'timeslots', 'adspots', ['adspot_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'timeslots', type_='foreignkey')
    op.alter_column('timeslots', 'locked',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('timeslots', 'to_time',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('timeslots', 'from_time',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('publishers', 'wallet_ref')
    op.drop_constraint(None, 'playbacks', type_='foreignkey')
    op.drop_constraint(None, 'playbacks', type_='foreignkey')
    op.drop_constraint(None, 'playbacks', type_='foreignkey')
    op.drop_constraint(None, 'playbacks', type_='foreignkey')
    op.drop_constraint(None, 'playbacks', type_='foreignkey')
    op.drop_constraint(None, 'contents', type_='foreignkey')
    op.alter_column('contents', 'content_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('advertisers', 'wallet_ref')
