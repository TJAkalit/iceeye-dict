"""empty message

Revision ID: 3e8c05906e53
Revises: b6be6832c6e0
Create Date: 2023-01-27 15:59:31.634181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e8c05906e53'
down_revision = 'b6be6832c6e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('physical_machine', sa.Column('cpu_multiply', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('physical_machine', 'cpu_multiply')
    # ### end Alembic commands ###
