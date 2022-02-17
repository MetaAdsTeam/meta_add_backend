"""adspot default

Revision ID: c299bf41a74f
Revises: 8fe57d6e1304
Create Date: 2022-02-17 18:30:43.937733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c299bf41a74f'
down_revision = '8fe57d6e1304'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('adspots', sa.Column('default_media', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('adspots', 'default_media')
    # ### end Alembic commands ###
