"""Initial migration

Revision ID: 84cfe1a0101e
Revises: 
Create Date: 2025-03-11 19:06:22.812582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '84cfe1a0101e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('request_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_data', sa.LargeBinary(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_request_history'))
    )
    op.create_index(op.f('ix_request_history_id'), 'request_history', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_request_history_id'), table_name='request_history')
    op.drop_table('request_history')
