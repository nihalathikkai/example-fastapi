"""Add foreign-key to table posts

Revision ID: d13f1941d718
Revises: a8afebf865b4
Create Date: 2022-10-21 17:27:56.297508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd13f1941d718'
down_revision = 'a8afebf865b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_owner_id_fkey', 
                          source_table='posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], 
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_owner_id_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
