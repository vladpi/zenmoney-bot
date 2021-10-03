"""users

Revision ID: 7d03dead2f08
Revises:
Create Date: 2021-10-03 14:50:50.790962

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7d03dead2f08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.Text(), nullable=True),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
    )


def downgrade():
    op.drop_table('users')
