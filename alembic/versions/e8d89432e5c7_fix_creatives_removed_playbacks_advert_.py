"""fix creatives, removed playbacks.advert_id

Revision ID: e8d89432e5c7
Revises: 9b0c66f1025a
Create Date: 2022-01-30 23:52:19.894205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8d89432e5c7'
down_revision = '9b0c66f1025a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('creatives', sa.Column('creative_type_id', sa.Integer(), nullable=True))
    op.alter_column('creatives', 'advert_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('creatives_content_type_id_fkey', 'creatives', type_='foreignkey')
    op.create_foreign_key(None, 'creatives', 'advertisers', ['advert_id'], ['id'])
    op.create_foreign_key(None, 'creatives', 'creative_types', ['creative_type_id'], ['id'])
    op.drop_column('creatives', 'content_type_id')
    op.add_column('playbacks', sa.Column('creative_id', sa.Integer(), nullable=True))
    op.drop_constraint('playbacks_advert_id_fkey', 'playbacks', type_='foreignkey')
    op.drop_constraint('playbacks_content_id_fkey', 'playbacks', type_='foreignkey')
    op.create_foreign_key(None, 'playbacks', 'creatives', ['creative_id'], ['id'])
    op.drop_column('playbacks', 'content_id')
    op.drop_column('playbacks', 'advert_id')


def downgrade():
    op.add_column('playbacks', sa.Column('advert_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('playbacks', sa.Column('content_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'playbacks', type_='foreignkey')
    op.create_foreign_key('playbacks_content_id_fkey', 'playbacks', 'creatives', ['content_id'], ['id'])
    op.create_foreign_key('playbacks_advert_id_fkey', 'playbacks', 'advertisers', ['advert_id'], ['id'])
    op.drop_column('playbacks', 'creative_id')
    op.add_column('creatives', sa.Column('content_type_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'creatives', type_='foreignkey')
    op.drop_constraint(None, 'creatives', type_='foreignkey')
    op.create_foreign_key('creatives_content_type_id_fkey', 'creatives', 'creative_types', ['content_type_id'], ['id'])
    op.alter_column('creatives', 'advert_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('creatives', 'creative_type_id')
