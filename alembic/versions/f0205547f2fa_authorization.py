"""authorization

Revision ID: f0205547f2fa
Revises: a445c0a5411f
Create Date: 2022-02-03 16:55:06.483114

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0205547f2fa'
down_revision = 'a445c0a5411f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('advertisers', sa.Column('login', sa.String(), nullable=False))
    op.add_column('advertisers', sa.Column(
        'password', sqlalchemy_utils.types.password.PasswordType(max_length=1137), nullable=False))
    op.create_unique_constraint(None, 'advertisers', ['login'])


def downgrade():
    op.drop_constraint(None, 'advertisers', type_='unique')
    op.drop_column('advertisers', 'password')
    op.drop_column('advertisers', 'login')
