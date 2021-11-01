"""zenmoney user id

Revision ID: b637c6de31f3
Revises: 1241bca1fdbc
Create Date: 2021-11-01 19:33:27.295232

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b637c6de31f3'
down_revision = '1241bca1fdbc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('zenmoney_user_id', sa.BigInteger(), nullable=True))


def downgrade():
    op.drop_column('users', 'zenmoney_user_id')
