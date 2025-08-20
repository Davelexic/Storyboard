"""create initial tables"""

from sqlmodel import SQLModel
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    SQLModel.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    SQLModel.metadata.drop_all(bind=op.get_bind())
