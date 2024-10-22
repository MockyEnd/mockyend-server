"""create operation table

Revision ID: f724db7c341f
Revises: aae8e0c4fbb5
Create Date: 2024-10-19 14:21:06.723211

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f724db7c341f"
down_revision: Union[str, None] = "aae8e0c4fbb5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.execute(
		"""
        CREATE TYPE method_type AS ENUM (
            'GET',
            'HEAD',
            'POST',
            'PUT',
            'PATCH',
            'DELETE'
        );
        """
	)

	op.execute(
		"""
        CREATE TYPE data_type AS ENUM (
            'STR',
            'CLASS',
            'INT',
            'BOOL',
            'DICT',
            'LIST'
        );
        """
	)

	op.execute(
		"""
        CREATE TABLE operation (
            id SERIAL PRIMARY KEY,
            uuid uuid DEFAULT uuid_generate_v4(),
            created_at timestamp with time zone DEFAULT current_timestamp,
            updated_at timestamp with time zone,
            name VARCHAR(40) NOT NULL,
            summary VARCHAR(100) NOT NULL,
            description VARCHAR(255) NOT NULL,
            method method_type NOT NULL,
            path VARCHAR(100) NOT NULL,
            response_type data_type,
            response_content jsonb
        );
        """
	)

	op.execute(
		"""
        CREATE TRIGGER update_operation_updated_at BEFORE UPDATE
        ON operation FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
        """
	)

	op.execute(
		"""
        CREATE UNIQUE INDEX idx_operation_uuid ON  operation (uuid);
        """
	)


def downgrade() -> None:
	op.execute("DROP TRIGGER IF EXISTS update_operation_updated_at ON operation;")
	op.execute("DROP TABLE operation;")
	op.execute("DROP TYPE IF EXISTS method_type;")
	op.execute("DROP TYPE IF EXISTS data_type;")
	op.execute("DROP INDEX IF EXISTS idx_operation_uuid;")
