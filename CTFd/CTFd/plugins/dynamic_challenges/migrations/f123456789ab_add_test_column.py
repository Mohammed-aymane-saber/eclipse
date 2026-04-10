"""Add test column to dynamic_challenges

Revision ID: f123456789ab
Revises: eb68f277ab61
Create Date: 2026-04-10 16:05:00.000000

"""
import sqlalchemy as sa

from CTFd.plugins.migrations import get_columns_for_table

revision = "f123456789ab"
down_revision = "eb68f277ab61"
branch_labels = None
depends_on = None


def upgrade(op=None):
    columns = get_columns_for_table(
        op=op, table_name="dynamic_challenge", names_only=True
    )
    if "test" not in columns:
        op.add_column(
            "dynamic_challenge",
            sa.Column("test", sa.String(length=128), nullable=True),
        )
        conn = op.get_bind()
        url = str(conn.engine.url)
        if url.startswith("postgres"):
            conn.execute(
                "UPDATE dynamic_challenge SET test = '' WHERE test IS NULL"
            )
        else:
            conn.execute(
                "UPDATE dynamic_challenge SET `test` = '' WHERE `test` IS NULL"
            )


def downgrade(op=None):
    columns = get_columns_for_table(
        op=op, table_name="dynamic_challenge", names_only=True
    )
    if "test" in columns:
        op.drop_column("dynamic_challenge", "test")
