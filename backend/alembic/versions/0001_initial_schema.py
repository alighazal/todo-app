from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "project_members",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(length=50), nullable=False, server_default=sa.text("'editor'")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("user_id", "project_id", name="uq_project_members_user_project"),
    )

    todo_status = postgresql.ENUM(
        "todo",
        "in_progress",
        "done",
        "archived",
        name="todo_status",
        create_type=False,
    )
    #todo_status.create(op.get_bind(), checkfirst=True)

    todo_priority = postgresql.ENUM(
        "1",
        "2",
        "3",
        name="todo_priority",
        create_type=False,
    )
    #todo_priority.create(op.get_bind(), checkfirst=True)

    op.execute(
    """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'todo_status') THEN
            CREATE TYPE todo_status AS ENUM ('todo', 'in_progress', 'done', 'archived');
        END IF;

        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'todo_priority') THEN
            CREATE TYPE todo_priority AS ENUM ('1', '2', '3');
        END IF;
    END
    $$;
    """
    )


    op.create_table(
        "todos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", todo_status, nullable=False, server_default="todo"),
        sa.Column("priority", todo_priority, nullable=False, server_default="2"),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index(
        "ix_todos_project_position",
        "todos",
        ["project_id", "position"],
    )


def downgrade() -> None:
    op.drop_index("ix_todos_project_position", table_name="todos")
    op.drop_table("todos")

    todo_status = postgresql.ENUM(
        "todo",
        "in_progress",
        "done",
        "archived",
        name="todo_status",
    )
    todo_priority = postgresql.ENUM(
        "1",
        "2",
        "3",
        name="todo_priority",
    )
    todo_priority.drop(op.get_bind(), checkfirst=True)
    todo_status.drop(op.get_bind(), checkfirst=True)

    op.drop_table("project_members")
    op.drop_table("projects")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

