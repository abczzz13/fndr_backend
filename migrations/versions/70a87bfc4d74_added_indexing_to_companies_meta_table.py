"""Added indexing to companies_meta Table

Revision ID: 70a87bfc4d74
Revises: e8fc06860769
Create Date: 2022-02-15 15:45:40.330775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70a87bfc4d74'
down_revision = 'e8fc06860769'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_companies_meta_company_id'), 'companies_meta', ['company_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_companies_meta_company_id'), table_name='companies_meta')
    # ### end Alembic commands ###
