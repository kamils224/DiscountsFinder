"""empty message

Revision ID: 8deeab97496a
Revises: 
Create Date: 2021-04-12 09:30:40.434855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8deeab97496a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop_website',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('website', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shop_website')
    # ### end Alembic commands ###
