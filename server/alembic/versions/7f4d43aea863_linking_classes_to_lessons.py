"""linking classes to lessons

Revision ID: 7f4d43aea863
Revises: 0f10d1e89649
Create Date: 2022-05-20 11:40:18.421397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f4d43aea863'
down_revision = '0f10d1e89649'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_visible', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lesson_class')
    # ### end Alembic commands ###
