"""removed playbacks.play_price

Revision ID: 15afb1722e18
Revises: 7231807a7571
Create Date: 2022-02-14 18:17:13.714614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15afb1722e18'
down_revision = '7231807a7571'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('playbacks', 'play_price')


def downgrade():
    op.add_column('playbacks', sa.Column('play_price', sa.INTEGER(), autoincrement=False, nullable=True))
