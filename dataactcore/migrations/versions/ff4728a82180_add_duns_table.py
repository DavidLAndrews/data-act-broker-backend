"""add duns table

Revision ID: ff4728a82180
Revises: 0bf2ed508f33
Create Date: 2017-07-25 00:12:22.805037

"""

# revision identifiers, used by Alembic.
revision = 'ff4728a82180'
down_revision = '18d9b114c1dc'
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
    op.create_table('duns',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('duns_id', sa.Integer(), nullable=False),
    sa.Column('awardee_or_recipient_uniqu', sa.Text(), nullable=True),
    sa.Column('legal_business_name', sa.Text(), nullable=True),
    sa.Column('activation_date', sa.Date(), nullable=True),
    sa.Column('deactivation_date', sa.Date(), nullable=True),
    sa.Column('expiration_date', sa.Date(), nullable=True),
    sa.Column('last_sam_mod_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('duns_id')
    )
    op.create_index('ix_duns_awardee_or_recipient_uniqu', 'duns', ['awardee_or_recipient_uniqu'], unique=False)
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('duns')
    ### end Alembic commands ###
