"""accounts transactions count

Revision ID: 3313e89114a9
Revises: f0dc83ee21dd
Create Date: 2022-02-11 00:16:11.679344

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3313e89114a9'
down_revision = 'f0dc83ee21dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'accounts',
        sa.Column(
            'transactions_count',
            sa.Integer(),
            server_default='0',
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column('accounts', 'transactions_count')
