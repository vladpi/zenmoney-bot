import sqlalchemy as sa

from core.db import metadata

accounts = sa.Table(
    'accounts',
    metadata,
    sa.Column('id', sa.String, primary_key=True),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('instrument_id', sa.BigInteger, nullable=False),
    sa.Column('title', sa.Text, nullable=False),
    sa.Column('transactions_count', sa.Integer, nullable=False, server_default='0'),
)
