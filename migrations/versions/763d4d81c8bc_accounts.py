"""accounts

Revision ID: 763d4d81c8bc
Revises: d21bd02931db
Create Date: 2021-10-05 17:08:15.534311

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '763d4d81c8bc'
down_revision = 'd21bd02931db'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'accounts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk__accounts__user_id__users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__accounts')),
    )


def downgrade():
    op.drop_table('accounts')
