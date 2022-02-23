"""foreign-key to post table

Revision ID: 30d7c7492978
Revises: b7e213084b67
Create Date: 2022-02-22 17:24:21.810582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30d7c7492978'
down_revision = 'b7e213084b67'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts",referent_table="users",
    local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
