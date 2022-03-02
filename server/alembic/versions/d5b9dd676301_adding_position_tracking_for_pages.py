"""adding position tracking for pages

Revision ID: d5b9dd676301
Revises: d82f46651413
Create Date: 2022-02-15 16:19:11.618016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b9dd676301'
down_revision = 'd82f46651413'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('position', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'position')
    # ### end Alembic commands ###
