"""1_to_1 user-teacher added.

Revision ID: f3560e7b1837
Revises: bf16022bfff9
Create Date: 2022-02-02 12:08:50.038549

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f3560e7b1837'
down_revision = 'bf16022bfff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('card_id', sa.String(length=64), nullable=True),
    sa.Column('qualification', sa.String(length=256), nullable=False),
    sa.Column('working_since', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('card_id')
    )
    op.create_index(op.f('ix_teachers_id'), 'teachers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_teachers_id'), table_name='teachers')
    op.drop_table('teachers')
    # ### end Alembic commands ###
