"""create update_updated_at_column function

Revision ID: aae8e0c4fbb5
Revises: 726eb42232d5
Create Date: 2024-10-19 13:00:22.002252

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aae8e0c4fbb5"
down_revision: Union[str, None] = "726eb42232d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.execute(
		"""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated_at = current_timestamp;
        RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
	)


def downgrade() -> None:
	op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")
