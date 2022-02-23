"""add content column to post table

Revision ID: 0fe8fc89e4cb
Revises: 87b3adb7029e
Create Date: 2022-02-22 17:04:52.014900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fe8fc89e4cb'
down_revision = '87b3adb7029e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
