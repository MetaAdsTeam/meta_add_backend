"""playback

Revision ID: 961df91a870c
Revises: 2e0efa7e1c94
Create Date: 2022-01-28 16:35:49.501717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '961df91a870c'
down_revision = '2e0efa7e1c94'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('playbacks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('adspot_id', sa.Integer(), nullable=True),
    sa.Column('timeslot_id', sa.Integer(), nullable=True),
    sa.Column('advert_id', sa.Integer(), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('smart_contract', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('playbacks')
