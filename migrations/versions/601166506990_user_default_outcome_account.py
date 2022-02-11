"""user default outcome account

Revision ID: 601166506990
Revises: 3313e89114a9
Create Date: 2022-02-11 21:49:39.678200

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '601166506990'
down_revision = '3313e89114a9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('default_outcome_account_id', sa.String(), nullable=True))
    op.create_foreign_key(
        op.f('fk__users__default_outcome_account_id__accounts'),
        'users',
        'accounts',
        ['default_outcome_account_id'],
        ['id'],
        ondelete='SET NULL',
    )


def downgrade():
    op.drop_constraint(
        op.f('fk__users__default_outcome_account_id__accounts'), 'users', type_='foreignkey'
    )
    op.drop_column('users', 'default_outcome_account_id')
