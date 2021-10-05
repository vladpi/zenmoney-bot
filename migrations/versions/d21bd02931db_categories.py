"""categories

Revision ID: d21bd02931db
Revises: 74a2870b172e
Create Date: 2021-10-05 16:43:29.902807

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd21bd02931db'
down_revision = '74a2870b172e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('is_income', sa.Boolean(), nullable=False),
        sa.Column('is_outcome', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk__categories__user_id__users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__categories')),
    )


def downgrade():
    op.drop_table('categories')
