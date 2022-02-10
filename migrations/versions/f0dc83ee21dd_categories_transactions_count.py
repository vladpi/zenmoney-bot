"""categories transactions count

Revision ID: f0dc83ee21dd
Revises: 871b1e6d401c
Create Date: 2022-02-10 23:20:57.261268

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f0dc83ee21dd'
down_revision = '871b1e6d401c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'categories',
        sa.Column(
            'transactions_count',
            sa.Integer(),
            server_default='0',
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column('categories', 'transactions_count')
