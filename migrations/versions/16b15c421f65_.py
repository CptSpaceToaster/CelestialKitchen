"""empty message

Revision ID: 16b15c421f65
Revises: 9fcd837d9e9a
Create Date: 2019-01-06 19:51:29.175099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16b15c421f65'
down_revision = '9fcd837d9e9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('ticks', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('drop_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drop')
    op.drop_column('user', 'drop_id')
    # ### end Alembic commands ###