"""Add parent duns and parent legal business name to DUNS table

Revision ID: 6973101b6853
Revises: ee7bff1d660c
Create Date: 2018-03-28 10:31:51.687556

"""

# revision identifiers, used by Alembic.
revision = '6973101b6853'
down_revision = 'ee7bff1d660c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('duns', sa.Column('ultimate_parent_legal_enti', sa.Text(), nullable=True))
    op.add_column('duns', sa.Column('ultimate_parent_unique_ide', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('duns', 'ultimate_parent_unique_ide')
    op.drop_column('duns', 'ultimate_parent_legal_enti')
    ### end Alembic commands ###

