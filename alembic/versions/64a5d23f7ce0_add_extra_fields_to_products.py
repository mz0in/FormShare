"""Add extra fields to products

Revision ID: 64a5d23f7ce0
Revises: b9a8461b1c66
Create Date: 2019-03-28 19:46:39.740554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64a5d23f7ce0'
down_revision = 'b9a8461b1c66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('date_published', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('downloads', sa.INTEGER(), server_default=sa.text("'0'"), nullable=True))
    op.add_column('product', sa.Column('last_download', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'last_download')
    op.drop_column('product', 'downloads')
    op.drop_column('product', 'date_published')
    # ### end Alembic commands ###
