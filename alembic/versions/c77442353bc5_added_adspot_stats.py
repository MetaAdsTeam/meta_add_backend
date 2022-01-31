"""added adspot_stats

Revision ID: c77442353bc5
Revises: e8d89432e5c7
Create Date: 2022-01-31 12:16:47.445353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c77442353bc5'
down_revision = 'e8d89432e5c7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('adspots_stats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spot_id', sa.Integer(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('views_amount', sa.Integer(), nullable=True),
    sa.Column('average_time', sa.Integer(), nullable=True),
    sa.Column('max_traffic', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spot_id'], ['adspots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('adspots_stats')
