"""marking author for course

Revision ID: 628fee213b19
Revises: 0313e49585ed
Create Date: 2022-03-08 04:45:44.703744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '628fee213b19'
down_revision = '0313e49585ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'course', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'author_id')
    # ### end Alembic commands ###
