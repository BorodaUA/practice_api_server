"""deleated_at field added to User model.

Revision ID: 1f03e8554806
Revises: a65f918ff3a0
Create Date: 2022-01-26 08:41:14.529343

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1f03e8554806'
down_revision = 'a65f918ff3a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'deleted_at')
    # ### end Alembic commands ###
