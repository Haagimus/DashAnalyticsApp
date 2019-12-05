"""adding relationship to resources <> programs

Revision ID: 3cee229d951e
Revises: ff11d28c68dc
Create Date: 2019-12-04 15:39:42.638310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cee229d951e'
down_revision = 'ff11d28c68dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('programs', sa.Column('entries', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'programs', 'resource_entries', ['entries'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'programs', type_='foreignkey')
    op.drop_column('programs', 'entries')
    # ### end Alembic commands ###
