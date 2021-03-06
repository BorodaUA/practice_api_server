"""CourseStudentAssociation course and student unique constaint

Revision ID: 0a3173329d84
Revises: 512905603c1c
Create Date: 2022-02-10 07:56:24.816701

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0a3173329d84'
down_revision = '512905603c1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_course_student_uc', 'course_student_association', ['course_id', 'student_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_course_student_uc', 'course_student_association', type_='unique')
    # ### end Alembic commands ###
