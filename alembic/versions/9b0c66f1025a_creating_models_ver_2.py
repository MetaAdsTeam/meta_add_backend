"""creating models ver. #2

Revision ID: 9b0c66f1025a
Revises: dbb698a6db0b
Create Date: 2022-01-30 16:19:35.047104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b0c66f1025a'
down_revision = 'dbb698a6db0b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('adspot_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advertisers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('wallet_ref', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('creative_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playback_statuses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publishers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('wallet_ref', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('adspots',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('spot_type_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('spot_metadata', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.ForeignKeyConstraint(['spot_type_id'], ['adspot_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('creatives',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('advert_id', sa.Integer(), nullable=False),
    sa.Column('content_type_id', sa.Integer(), nullable=True),
    sa.Column('nft_ref', sa.String(), nullable=False),
    sa.Column('nft_bin', sa.LargeBinary(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['content_type_id'], ['creative_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timeslots',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('adspot_id', sa.Integer(), nullable=True),
    sa.Column('from_time', sa.Integer(), nullable=False),
    sa.Column('to_time', sa.Integer(), nullable=False),
    sa.Column('locked', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['adspot_id'], ['adspots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playbacks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('adspot_id', sa.Integer(), nullable=True),
    sa.Column('timeslot_id', sa.Integer(), nullable=True),
    sa.Column('advert_id', sa.Integer(), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('smart_contract', sa.String(), nullable=True),
    sa.Column('play_price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adspot_id'], ['adspots.id'], ),
    sa.ForeignKeyConstraint(['advert_id'], ['advertisers.id'], ),
    sa.ForeignKeyConstraint(['content_id'], ['creatives.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['playback_statuses.id'], ),
    sa.ForeignKeyConstraint(['timeslot_id'], ['timeslots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('playbacks')
    op.drop_table('timeslots')
    op.drop_table('creatives')
    op.drop_table('adspots')
    op.drop_table('publishers')
    op.drop_table('playback_statuses')
    op.drop_table('creative_types')
    op.drop_table('advertisers')
    op.drop_table('adspot_types')
