"""getting rid of sections

Revision ID: ed8dd1b47418
Revises: 1ce2b029b2c1
Create Date: 2022-02-05 12:35:45.074263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8dd1b47418'
down_revision = '1ce2b029b2c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('section')
    op.add_column('page', sa.Column('html', sa.String(length=2000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'html')
    op.create_table('section',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('text_html', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.Column('page_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['page.id'], name='section_page_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='section_pkey')
    )
    # ### end Alembic commands ###
