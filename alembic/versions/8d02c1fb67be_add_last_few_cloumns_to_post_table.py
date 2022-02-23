"""add last few cloumns to post table

Revision ID: 8d02c1fb67be
Revises: 30d7c7492978
Create Date: 2022-02-22 17:29:08.670059

"""
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d02c1fb67be'
down_revision = '30d7c7492978'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published',sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
