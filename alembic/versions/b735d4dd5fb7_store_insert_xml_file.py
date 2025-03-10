"""Store insert XML file

Revision ID: b735d4dd5fb7
Revises: 8ad53c7df321
Create Date: 2020-11-21 17:17:55.609632

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b735d4dd5fb7"
down_revision = "8ad53c7df321"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "odkform", sa.Column("form_insertxmlfile", sa.UnicodeText(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("odkform", "form_insertxmlfile")
    # ### end Alembic commands ###
