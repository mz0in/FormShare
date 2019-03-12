"""Remove columns for external files

Revision ID: 7ceb8ade2231
Revises: 1681ed03029c
Create Date: 2019-03-11 17:19:26.365249

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7ceb8ade2231'
down_revision = '1681ed03029c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mediafile', 'file_lstdwnld')
    op.drop_column('mediafile', 'file_url')
    op.drop_column('mediafile', 'file_dwnlderror')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mediafile', sa.Column('file_dwnlderror', mysql.INTEGER(display_width=11), server_default=sa.text("'0'"), autoincrement=False, nullable=True))
    op.add_column('mediafile', sa.Column('file_url', mysql.TEXT(), nullable=True))
    op.add_column('mediafile', sa.Column('file_lstdwnld', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
