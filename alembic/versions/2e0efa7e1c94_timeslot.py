"""timeslot

Revision ID: 2e0efa7e1c94
Revises: 4e30e60c754b
Create Date: 2022-01-28 16:27:59.913612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0efa7e1c94'
down_revision = '4e30e60c754b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('timeslots',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('adspot_id', sa.Integer(), nullable=True),
    sa.Column('from_time', sa.Integer(), nullable=True),
    sa.Column('to_time', sa.Integer(), nullable=True),
    sa.Column('locked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('timeslots')
