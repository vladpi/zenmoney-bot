import sqlalchemy as sa

from core.db import metadata

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('username', sa.Text, nullable=True),
    sa.Column('first_name', sa.Text, nullable=True),
    sa.Column('last_name', sa.Text, nullable=True),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    sa.Column('zenmoney_token', sa.Text, nullable=True),
    sa.Column('zenmoney_last_sync', sa.BigInteger, nullable=True),
    sa.Column('zenmoney_user_id', sa.BigInteger, nullable=True),
    sa.Column(
        'default_outcome_account_id',
        sa.ForeignKey(
            'accounts.id',
            ondelete='SET NULL',
        ),
        nullable=True,
    ),
)
