"""adding month to resource usage table

Revision ID: 78433d3fab89
Revises: 4d430ae84e6a
Create Date: 2020-03-05 07:36:52.812482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78433d3fab89'
down_revision = '4d430ae84e6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource_entries', sa.Column('month', sa.String(length=6), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resource_entries', 'month')
    # ### end Alembic commands ###
