"""zenmoney user last sync

Revision ID: 1241bca1fdbc
Revises: 763d4d81c8bc
Create Date: 2021-10-05 22:38:54.565286

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '1241bca1fdbc'
down_revision = '763d4d81c8bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('zenmoney_last_sync', sa.BigInteger(), nullable=True))


def downgrade():
    op.drop_column('users', 'zenmoney_last_sync')
