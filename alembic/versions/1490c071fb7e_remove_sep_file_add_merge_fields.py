"""Remove sep_file. Add merge fields

Revision ID: 1490c071fb7e
Revises: 27849ecf5d0b
Create Date: 2019-09-04 08:38:51.156743

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "1490c071fb7e"
down_revision = "27849ecf5d0b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "odkform",
        sa.Column(
            "form_abletomerge",
            sa.INTEGER(),
            server_default=sa.text("'-1'"),
            nullable=True,
        ),
    )
    op.add_column(
        "odkform", sa.Column("form_mergetask", sa.Unicode(length=64), nullable=True)
    )
    op.drop_column("odkform", "form_sepfile")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("odkform", sa.Column("form_sepfile", mysql.TEXT(), nullable=True))
    op.drop_column("odkform", "form_mergetask")
    op.drop_column("odkform", "form_abletomerge")
    # ### end Alembic commands ###
