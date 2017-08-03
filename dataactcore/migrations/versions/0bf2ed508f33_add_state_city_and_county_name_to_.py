"""Add state, city, and county name to PublishedAwardFinancialAssistance table

Revision ID: 0bf2ed508f33
Revises: 2c2b9b1ff0e5
Create Date: 2017-07-21 13:05:06.714431

"""

# revision identifiers, used by Alembic.
revision = '0bf2ed508f33'
down_revision = '2c2b9b1ff0e5'
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
    op.add_column('published_award_financial_assistance', sa.Column('place_of_perform_county_na', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('place_of_perform_state_nam', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('place_of_performance_city', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('published_award_financial_assistance', 'place_of_performance_city')
    op.drop_column('published_award_financial_assistance', 'place_of_perform_state_nam')
    op.drop_column('published_award_financial_assistance', 'place_of_perform_county_na')
    ### end Alembic commands ###

