"""enhance book and user models with additional fields"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0003_enhance_models"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to book table
    op.add_column("book", sa.Column("author", sa.String(), nullable=True))
    op.add_column("book", sa.Column("language", sa.String(), nullable=True))
    op.add_column("book", sa.Column("identifier", sa.String(), nullable=True))
    op.add_column("book", sa.Column("file_size", sa.Integer(), nullable=True))
    op.add_column("book", sa.Column("file_path", sa.String(), nullable=True))
    op.add_column("book", sa.Column("processing_status", sa.String(), nullable=False, server_default="pending"))
    op.add_column("book", sa.Column("processing_error", sa.String(), nullable=True))
    op.add_column("book", sa.Column("theme", sa.String(), nullable=True))
    op.add_column("book", sa.Column("total_chapters", sa.Integer(), nullable=True))
    op.add_column("book", sa.Column("total_effects", sa.Integer(), nullable=True))
    op.add_column("book", sa.Column("effect_density", sa.Float(), nullable=True))
    op.add_column("book", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("book", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.add_column("book", sa.Column("processed_at", sa.DateTime(), nullable=True))
    op.add_column("book", sa.Column("book_metadata", postgresql.JSONB(), nullable=True))
    
    # Add new columns to user table
    op.add_column("user", sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"))
    op.add_column("user", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("user", sa.Column("updated_at", sa.DateTime(), nullable=True))
    
    # Create user_preferences table
    op.create_table(
        "userpreferences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("font_size", sa.Integer(), nullable=False, server_default="16"),
        sa.Column("brightness", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("adaptive_brightness", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("effects_enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("effect_intensity", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("effects_config", postgresql.JSONB(), nullable=True),
        sa.Column("high_contrast", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("reduce_motion", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("screen_reader_friendly", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("auto_save_progress", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("sync_preferences", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    
    # Create indexes
    op.create_index(op.f("ix_book_author"), "book", ["author"], unique=False)
    op.create_index(op.f("ix_book_identifier"), "book", ["identifier"], unique=False)
    op.create_index(op.f("ix_userpreferences_user_id"), "userpreferences", ["user_id"], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f("ix_userpreferences_user_id"), table_name="userpreferences")
    op.drop_index(op.f("ix_book_identifier"), table_name="book")
    op.drop_index(op.f("ix_book_author"), table_name="book")
    
    # Drop user_preferences table
    op.drop_table("userpreferences")
    
    # Drop columns from user table
    op.drop_column("user", "updated_at")
    op.drop_column("user", "created_at")
    op.drop_column("user", "is_active")
    
    # Drop columns from book table
    op.drop_column("book", "book_metadata")
    op.drop_column("book", "processed_at")
    op.drop_column("book", "updated_at")
    op.drop_column("book", "created_at")
    op.drop_column("book", "effect_density")
    op.drop_column("book", "total_effects")
    op.drop_column("book", "total_chapters")
    op.drop_column("book", "theme")
    op.drop_column("book", "processing_error")
    op.drop_column("book", "processing_status")
    op.drop_column("book", "file_path")
    op.drop_column("book", "file_size")
    op.drop_column("book", "identifier")
    op.drop_column("book", "language")
    op.drop_column("book", "author")
