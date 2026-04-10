"""Add author and difficulty columns to challenges table

Revision ID: c1d2e3f4a5b6
Revises: ebd8b864a529
Create Date: 2026-04-10 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c1d2e3f4a5b6"
down_revision = "ebd8b864a529"
branch_labels = None
depends_on = None


def upgrade():
    # Use try/except to handle MariaDB/MySQL that might already have these columns
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    existing_columns = [c["name"] for c in inspector.get_columns("challenges")]

    if "author" not in existing_columns:
        op.add_column(
            "challenges",
            sa.Column("author", sa.String(length=128), nullable=True),
        )
    if "difficulty" not in existing_columns:
        op.add_column(
            "challenges",
            sa.Column(
                "difficulty",
                sa.String(length=32),
                nullable=True,
                server_default="medium",
            ),
        )


def downgrade():
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    existing_columns = [c["name"] for c in inspector.get_columns("challenges")]

    if "difficulty" in existing_columns:
        op.drop_column("challenges", "difficulty")
    if "author" in existing_columns:
        op.drop_column("challenges", "author")
