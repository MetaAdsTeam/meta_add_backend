"""added creative.blockchain_ref

Revision ID: 3a23474893a8
Revises: 5ca1d84fd129
Create Date: 2022-02-11 11:27:59.194852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a23474893a8'
down_revision = '5ca1d84fd129'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('creatives', sa.Column('blockchain_ref', sa.String(), nullable=True))


def downgrade():
    op.drop_column('creatives', 'blockchain_ref')
