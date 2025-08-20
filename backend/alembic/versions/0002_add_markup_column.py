"""add markup column to book table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_add_markup_column"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("book", sa.Column("markup", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("book", "markup")
