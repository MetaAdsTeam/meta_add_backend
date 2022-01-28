"""content

Revision ID: fcef64ccfdba
Revises: 2b11108a19b1
Create Date: 2022-01-28 17:16:06.915593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcef64ccfdba'
down_revision = '2b11108a19b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('contents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('advert_id', sa.Integer(), nullable=False),
    sa.Column('content_type_id', sa.Integer(), nullable=False),
    sa.Column('nft_ref', sa.String(), nullable=False),
    sa.Column('nft_bin', sa.LargeBinary(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('contents')
