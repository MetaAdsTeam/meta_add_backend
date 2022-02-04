"""timeslot datetime

Revision ID: 1e3951596653
Revises: 5889feae9ad7
Create Date: 2022-02-04 20:50:38.665405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e3951596653'
down_revision = '5889feae9ad7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'timeslots',
        'from_time',
        type_=sa.DateTime(False),
        postgresql_using='to_timestamp(from_time)'
    )
    op.alter_column(
        'timeslots',
        'to_time',
        type_=sa.DateTime(False),
        postgresql_using='to_timestamp(to_time)'
    )


def downgrade():
    op.alter_column(
        'timeslots',
        'from_time',
        type_=sa.Integer,
        postgresql_using='cast(extract(epoch from from_time) as integer)'
    )
    op.alter_column(
        'timeslots',
        'to_time',
        type_=sa.Integer,
        postgresql_using='cast(extract(epoch from to_time) as integer)'
    )
