"""adspot preview, thumbnail

Revision ID: 5889feae9ad7
Revises: f0205547f2fa
Create Date: 2022-02-04 12:23:30.076871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5889feae9ad7'
down_revision = 'f0205547f2fa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('adspots', sa.Column('preview_url', sa.String(), nullable=True))
    op.add_column('adspots', sa.Column('preview_thumb_url', sa.String(), nullable=True))


def downgrade():
    op.drop_column('adspots', 'preview_thumb_url')
    op.drop_column('adspots', 'preview_url')
