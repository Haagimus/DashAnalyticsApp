"""changed resource usage pd and sub pd to optional columns

Revision ID: 8a0cab1e44af
Revises: 276ee2b15b38
Create Date: 2020-02-28 07:32:10.193844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a0cab1e44af'
down_revision = '276ee2b15b38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('resource_entries', 'period',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('resource_entries', 'sub_period',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('resource_entries', 'sub_period',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('resource_entries', 'period',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
