"""Tasks Dispatcher misc

Revision ID: 0c8c410a4a57
Revises: 1e3951596653
Create Date: 2022-02-04 22:45:35.986342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c8c410a4a57'
down_revision = '1e3951596653'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('adspot_types', 'publish_url')
    op.add_column('adspots', sa.Column('publish_url', sa.String(), nullable=False))
    op.add_column('adspots', sa.Column('stop_url', sa.String(), nullable=False))
    op.add_column('adspots', sa.Column('delay_before_publish', sa.Float(), server_default='0', nullable=False))
    op.add_column('playbacks', sa.Column('taken_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('playbacks', 'taken_at')
    op.drop_column('adspots', 'delay_before_publish')
    op.drop_column('adspots', 'stop_url')
    op.drop_column('adspots', 'publish_url')
    op.add_column('adspot_types', sa.Column('publish_url', sa.VARCHAR(), server_default=sa.text("''::character varying"), autoincrement=False, nullable=False))
