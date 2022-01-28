"""content_type

Revision ID: ce39af23ee7a
Revises: fcef64ccfdba
Create Date: 2022-01-28 17:17:21.749301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce39af23ee7a'
down_revision = 'fcef64ccfdba'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('content_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('content_types')
