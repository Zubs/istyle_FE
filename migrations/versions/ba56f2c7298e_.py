"""empty message

Revision ID: ba56f2c7298e
Revises: 
Create Date: 2020-11-11 09:01:13.325881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba56f2c7298e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=80), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('is_seller', sa.Boolean(), nullable=True),
    sa.Column('author', sa.Boolean(), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('company', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
