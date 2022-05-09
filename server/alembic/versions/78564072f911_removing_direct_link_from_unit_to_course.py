"""removing direct link from unit to course

Revision ID: 78564072f911
Revises: b5ebd10bcdb9
Create Date: 2022-05-04 16:15:53.058647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78564072f911'
down_revision = 'b5ebd10bcdb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unit_course_id_fkey', 'unit', type_='foreignkey')
    op.drop_column('unit', 'course_id')
    op.drop_column('unit', 'position')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit', sa.Column('position', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('unit', sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('unit_course_id_fkey', 'unit', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###
