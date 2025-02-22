"""Add report updates to products

Revision ID: e3cbc92b0a17
Revises: 3a2b99443dbf
Create Date: 2021-12-04 11:40:21.765342

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e3cbc92b0a17"
down_revision = "3a2b99443dbf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product",
        sa.Column(
            "report_updates", sa.INTEGER(), server_default=sa.text("'1'"), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product", "report_updates")
    # ### end Alembic commands ###
