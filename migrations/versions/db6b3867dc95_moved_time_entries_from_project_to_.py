"""moved time entries from project to charge number

Revision ID: db6b3867dc95
Revises: 8a0cab1e44af
Create Date: 2020-02-28 15:42:39.628962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db6b3867dc95'
down_revision = '8a0cab1e44af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'registered_users', 'functions', ['function'], ['function'])
    op.add_column('resource_entries', sa.Column('charge_number', sa.String(length=50), nullable=True))
    op.drop_constraint('FK_proj_rsrc', 'resource_entries', type_='foreignkey')
    op.create_foreign_key(None, 'resource_entries', 'charge_numbers', ['charge_number'], ['charge_number'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('resource_entries', 'project_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource_entries', sa.Column('project_name', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'resource_entries', type_='foreignkey')
    op.create_foreign_key('FK_proj_rsrc', 'resource_entries', 'projects', ['project_name'], ['name'])
    op.drop_column('resource_entries', 'charge_number')
    op.drop_constraint(None, 'registered_users', type_='foreignkey')
    # ### end Alembic commands ###
