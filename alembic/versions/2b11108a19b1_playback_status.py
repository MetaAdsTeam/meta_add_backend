"""playback_status

Revision ID: 2b11108a19b1
Revises: aeb776c470c4
Create Date: 2022-01-28 16:47:29.064820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b11108a19b1'
down_revision = 'aeb776c470c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('playback_statuses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('playback_statuses')
