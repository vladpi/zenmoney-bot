"""zenmoney user token

Revision ID: 74a2870b172e
Revises: 7d03dead2f08
Create Date: 2021-10-05 11:56:00.820991

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '74a2870b172e'
down_revision = '7d03dead2f08'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('zenmoney_token', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('users', 'zenmoney_token')
