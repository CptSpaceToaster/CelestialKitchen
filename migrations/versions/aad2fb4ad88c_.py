"""empty message

Revision ID: aad2fb4ad88c
Revises: 6616332a2bff
Create Date: 2018-12-30 20:54:32.415303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad2fb4ad88c'
down_revision = '6616332a2bff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('initial_ticks', sa.Integer(), nullable=False, default=0))
    op.add_column('user', sa.Column('is_exploring', sa.Boolean(), nullable=False, default=False))
    op.add_column('user', sa.Column('ticks', sa.Integer(), nullable=False, default=0))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'ticks')
    op.drop_column('user', 'is_exploring')
    op.drop_column('user', 'initial_ticks')
    # ### end Alembic commands ###