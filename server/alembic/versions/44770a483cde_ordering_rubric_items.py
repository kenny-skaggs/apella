"""ordering rubric items

Revision ID: 44770a483cde
Revises: cb7f7f84b88b
Create Date: 2022-03-27 16:34:33.840378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44770a483cde'
down_revision = 'cb7f7f84b88b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rubric_item', sa.Column('position', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rubric_item', 'position')
    # ### end Alembic commands ###
