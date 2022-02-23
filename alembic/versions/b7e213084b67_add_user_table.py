"""add user table

Revision ID: b7e213084b67
Revises: 0fe8fc89e4cb
Create Date: 2022-02-22 17:10:26.527611

"""
from pickle import FALSE
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e213084b67'
down_revision = '0fe8fc89e4cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                        sa.Column('id',sa.Integer(),nullable=FALSE),
                        sa.Column('email',sa.String(),nullable=False),
                        sa.Column('password',sa.String(),nullable=False),
                        sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'),nullable=False),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('email')
                        )
    pass


def downgrade():
    op.drop_table('users')
    pass
