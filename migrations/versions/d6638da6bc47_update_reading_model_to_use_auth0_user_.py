"""Update Reading model to use auth0_user_id

Revision ID: d6638da6bc47
Revises: 6c4ddeedcb32
Create Date: 2024-07-17 14:26:11.644759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d6638da6bc47"
down_revision = "6c4ddeedcb32"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("readings", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("auth0_user_id", sa.String(length=64), nullable=False)
        )
        batch_op.drop_constraint("readings_user_id_fkey", type_="foreignkey")
        batch_op.create_foreign_key(None, "users", ["auth0_user_id"], ["auth0_user_id"])
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("readings", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False)
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "readings_user_id_fkey", "users", ["user_id"], ["id"]
        )
        batch_op.drop_column("auth0_user_id")

    # ### end Alembic commands ###
