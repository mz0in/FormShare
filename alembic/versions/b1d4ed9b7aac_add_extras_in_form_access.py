"""Add extras in form access

Revision ID: b1d4ed9b7aac
Revises: be94ab1faa43
Create Date: 2020-06-24 10:10:18.026197

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b1d4ed9b7aac"
down_revision = "be94ab1faa43"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("formaccess", sa.Column("extras", sa.UnicodeText(), nullable=True))
    op.add_column("formgrpaccess", sa.Column("extras", sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("formgrpaccess", "extras")
    op.drop_column("formaccess", "extras")
    # ### end Alembic commands ###
