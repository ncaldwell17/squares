"""adding the squares table

Revision ID: 8e6c97d4ae0c
Revises: 
Create Date: 2025-02-20 12:14:32.526760

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '8e6c97d4ae0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE squares (
            id UUID PRIMARY KEY,
            color VARCHAR(255) NOT NULL,
            rotation INTEGER NOT NULL
        )
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE squares
    """)
