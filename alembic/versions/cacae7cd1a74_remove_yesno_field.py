"""Remove yesNo field

Revision ID: cacae7cd1a74
Revises: f02babf9a725
Create Date: 2019-08-31 23:36:29.321871

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "cacae7cd1a74"
down_revision = "f02babf9a725"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("odkform", "form_yesno")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "odkform", sa.Column("form_yesno", mysql.VARCHAR(length=120), nullable=True)
    )
    # ### end Alembic commands ###
