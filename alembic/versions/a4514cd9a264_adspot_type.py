"""adspot_type

Revision ID: a4514cd9a264
Revises: ebe1ba8fe2a5
Create Date: 2022-01-25 15:21:14.656907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4514cd9a264'
down_revision = 'ebe1ba8fe2a5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('adspot_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('adspot_types')
