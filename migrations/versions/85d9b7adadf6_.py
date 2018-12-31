"""empty message

Revision ID: 85d9b7adadf6
Revises: aad2fb4ad88c
Create Date: 2018-12-30 21:07:27.475615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d9b7adadf6'
down_revision = 'aad2fb4ad88c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('destination', sa.String(), nullable=True))
    op.add_column('user', sa.Column('mention', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'mention')
    op.drop_column('user', 'destination')
    # ### end Alembic commands ###