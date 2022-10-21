"""Add publish column to table posts

Revision ID: a8afebf865b4
Revises: 5e777bcb0ebd
Create Date: 2022-10-21 17:10:10.974058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8afebf865b4'
down_revision = '5e777bcb0ebd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('publish', sa.Boolean(), nullable=False, server_default='TRUE'))


def downgrade() -> None:
    op.drop_column('posts', 'publish')
