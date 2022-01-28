"""ForeignKeys: adspot -> publishers.id, adspot_types.id

Revision ID: d149d70dcb4a
Revises: ce39af23ee7a
Create Date: 2022-01-28 17:31:19.052827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd149d70dcb4a'
down_revision = 'ce39af23ee7a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(None, 'adspots', 'publishers', ['publisher_id'], ['id'])
    op.create_foreign_key(None, 'adspots', 'adspot_types', ['adspot_type_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'adspots', type_='foreignkey')
    op.drop_constraint(None, 'adspots', type_='foreignkey')
