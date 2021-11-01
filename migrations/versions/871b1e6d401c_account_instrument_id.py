"""account instrument id

Revision ID: 871b1e6d401c
Revises: b637c6de31f3
Create Date: 2021-11-01 19:53:05.517121

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '871b1e6d401c'
down_revision = 'b637c6de31f3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('accounts', sa.Column('instrument_id', sa.BigInteger(), nullable=True))
    op.execute('UPDATE accounts SET instrument_id = -1')
    op.alter_column('accounts', 'instrument_id', nullable=False)


def downgrade():
    op.drop_column('accounts', 'instrument_id')
