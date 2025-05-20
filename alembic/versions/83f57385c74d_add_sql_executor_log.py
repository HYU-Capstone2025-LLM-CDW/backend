"""add sql_executor_log

Revision ID: 83f57385c74d
Revises: dfbe45e8ec1c
Create Date: 2025-05-19 17:49:26.663331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83f57385c74d'
down_revision: Union[str, None] = 'dfbe45e8ec1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sql_executor_log',
        sa.Column('log_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sql', sa.Text, nullable=True),
        sa.Column('sql_validation_reason', sa.Text, nullable=True),
        sa.Column('pre_sql_filter_complete_timestamp', sa.DateTime, nullable=True),
        sa.Column('post_sql_filter_complete_timestamp', sa.DateTime, nullable=True),
        sa.Column('sql_execution_status', sa.String(50), nullable=True),
        sa.Column('sql_error_message', sa.Text, nullable=True),
        sa.Column('result_row_count', sa.Integer, nullable=True),
        sa.Column('sql_execution_start_timestamp', sa.DateTime, nullable=True),
        sa.Column('sql_execution_end_timestamp', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('sql_executor_log')
