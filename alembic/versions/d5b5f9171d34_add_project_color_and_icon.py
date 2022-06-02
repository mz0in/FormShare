"""Add project color and icon

Revision ID: d5b5f9171d34
Revises: 6fd9ba381bc6
Create Date: 2021-07-29 15:26:57.628525

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "d5b5f9171d34"
down_revision = "6fd9ba381bc6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "project",
        sa.Column(
            "project_icon",
            mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
            nullable=True,
        ),
    )
    op.add_column(
        "project", sa.Column("project_hexcolor", sa.Unicode(length=60), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "project_hexcolor")
    op.drop_column("project", "project_icon")
    # ### end Alembic commands ###
