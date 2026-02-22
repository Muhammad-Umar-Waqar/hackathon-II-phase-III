"""Add messages table

Revision ID: 002_add_messages
Revises: 001_add_conversations
Create Date: 2026-02-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = '002_add_messages'
down_revision = '001_add_conversations'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'])
    )
    op.create_index('ix_messages_conversation_id_created_at', 'messages', ['conversation_id', 'created_at'])
    op.create_index('ix_messages_user_id', 'messages', ['user_id'])
    op.create_index('ix_messages_role', 'messages', ['role'])


def downgrade() -> None:
    op.drop_index('ix_messages_role', table_name='messages')
    op.drop_index('ix_messages_user_id', table_name='messages')
    op.drop_index('ix_messages_conversation_id_created_at', table_name='messages')
    op.drop_table('messages')
