"""Change file to text

Revision ID: 3a2b99443dbf
Revises: 1ffae93c82d2
Create Date: 2021-11-27 20:51:37.174202

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "3a2b99443dbf"
down_revision = "1ffae93c82d2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "product",
        "output_file",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=120),
        type_=mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    op.alter_column(
        "product",
        "output_file",
        existing_type=mysql.MEDIUMTEXT(collation="utf8mb4_unicode_ci"),
        type_=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=120),
        existing_nullable=True,
    )
