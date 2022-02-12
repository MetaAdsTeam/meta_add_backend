"""removed playback_statuses

Revision ID: 7231807a7571
Revises: 3a23474893a8
Create Date: 2022-02-12 22:22:30.405929

"""
from alembic import op
import sqlalchemy as sa
import root.enums as enums

# revision identifiers, used by Alembic.
revision = '7231807a7571'
down_revision = '3a23474893a8'
branch_labels = None
depends_on = None

playbackstatus = sa.Enum(enums.PlaybackStatus, name='playbackstatus')


def upgrade():
    op.drop_constraint('playbacks_status_id_fkey', 'playbacks', type_='foreignkey')
    op.drop_table('playback_statuses')
    playbackstatus.create(op.get_bind())
    op.add_column('playbacks', sa.Column('status', playbackstatus, nullable=True))
    op.drop_column('playbacks', 'status_id')


def downgrade():
    op.add_column('playbacks', sa.Column('status_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('playbacks', 'status')
    playbackstatus.drop(op.get_bind())
    op.create_table('playback_statuses',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='playback_statuses_pkey')
                    )
    op.create_foreign_key('playbacks_status_id_fkey', 'playbacks', 'playback_statuses', ['status_id'], ['id'])
