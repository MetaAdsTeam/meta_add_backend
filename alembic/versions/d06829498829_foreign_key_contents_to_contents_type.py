"""foreign key contents to contents_type

Revision ID: d06829498829
Revises: 9dbf008f4608
Create Date: 2022-01-30 15:02:16.504293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd06829498829'
down_revision = '9dbf008f4608'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('ad_places', 'price',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('contents_content_type_id_fkey', 'contents', type_='foreignkey')
    op.create_foreign_key(None, 'contents', 'content_types', ['content_type_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'contents', type_='foreignkey')
    op.create_foreign_key('contents_content_type_id_fkey', 'contents', 'adspot_types', ['content_type_id'], ['id'])
    op.alter_column('ad_places', 'price',
               existing_type=sa.INTEGER(),
               nullable=True)
