"""cleanup database state and remove userpreferences table

Revision ID: 0004_cleanup_database
Revises: 0003_enhance_models
Create Date: 2025-01-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '0004_cleanup_database'
down_revision = '0003_enhance_models'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Clean up database state and remove unused userpreferences table."""
    
    # Check if userpreferences table exists and drop it if it does
    # This table was created in 0003 but we're not using it anymore
    # We're using embedded JSON preferences in the user table instead
    
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    
    # Check if userpreferences table exists
    if 'userpreferences' in inspector.get_table_names():
        # Drop the userpreferences table and its indexes
        try:
            op.drop_index('ix_userpreferences_user_id', table_name='userpreferences')
        except:
            pass  # Index might not exist
        
        op.drop_table('userpreferences')
    
    # Ensure user table has the preferences column (JSON)
    # This should already exist but let's make sure
    user_columns = [col['name'] for col in inspector.get_columns('user')]
    if 'preferences' not in user_columns:
        op.add_column('user', sa.Column('preferences', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Recreate userpreferences table if needed for rollback."""
    
    # Recreate the userpreferences table
    op.create_table(
        'userpreferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('font_size', sa.Integer(), nullable=False, server_default='16'),
        sa.Column('brightness', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('adaptive_brightness', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('effects_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('effect_intensity', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('effects_config', sa.JSON(), nullable=True),
        sa.Column('high_contrast', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reduce_motion', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('screen_reader_friendly', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('auto_save_progress', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('sync_preferences', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index
    op.create_index('ix_userpreferences_user_id', 'userpreferences', ['user_id'], unique=False)
    
    # Remove preferences column from user table if it exists
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    user_columns = [col['name'] for col in inspector.get_columns('user')]
    if 'preferences' in user_columns:
        op.drop_column('user', 'preferences')
