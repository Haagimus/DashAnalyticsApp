"""adding uid column to resource_usage table

Revision ID: 4d430ae84e6a
Revises: 3cb53d7f889e
Create Date: 2020-03-03 11:36:18.985024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d430ae84e6a'
down_revision = '3cb53d7f889e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource_entries', sa.Column('uid', sa.String(length=50), nullable=False))
    op.alter_column('resource_entries', 'charge_number',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
    op.alter_column('resource_entries', 'function_name',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
    op.alter_column('resource_entries', 'period',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('resource_entries', 'sub_period',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'resource_entries', 'functions', ['function_name'], ['function'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'resource_entries', type_='foreignkey')
    op.alter_column('resource_entries', 'sub_period',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('resource_entries', 'period',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('resource_entries', 'function_name',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
    op.alter_column('resource_entries', 'charge_number',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
    op.drop_column('resource_entries', 'uid')
    # ### end Alembic commands ###
