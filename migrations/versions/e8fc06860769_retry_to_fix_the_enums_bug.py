"""Retry to fix the enums bug

Revision ID: e8fc06860769
Revises: 
Create Date: 2022-02-11 09:59:35.092742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8fc06860769'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
                    sa.Column('city_id', sa.Integer(), nullable=False),
                    sa.Column('city_name', sa.String(
                        length=64), nullable=True),
                    sa.Column('region', sa.Enum('Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
                                                'Noord-Holland', 'Overijssel', 'Utrecht', 'Zuid-Holland', 'Zeeland', name='regions'), nullable=True),
                    sa.PrimaryKeyConstraint('city_id')
                    )
    op.create_table('meta',
                    sa.Column('meta_id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.Enum('Discipline', 'Branch',
                              'Tag', name='types'), nullable=True),
                    sa.Column('meta_string', sa.String(
                        length=120), nullable=True),
                    sa.PrimaryKeyConstraint('meta_id')
                    )
    op.create_table('companies',
                    sa.Column('company_id', sa.Integer(), nullable=False),
                    sa.Column('company_name', sa.String(
                        length=64), nullable=True),
                    sa.Column('logo_image_src', sa.String(
                        length=255), nullable=True),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.Column('website', sa.String(length=255), nullable=True),
                    sa.Column('year', sa.Integer(), nullable=True),
                    sa.Column('company_size', sa.Enum('1-10', '11-50',
                                                      '51-100', 'GT-100', name='sizes'), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ),
                    sa.PrimaryKeyConstraint('company_id')
                    )
    op.create_table('companies_meta',
                    sa.Column('meta_id', sa.Integer(), nullable=False),
                    sa.Column('company_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['company_id'], ['companies.company_id'], ),
                    sa.ForeignKeyConstraint(['meta_id'], ['meta.meta_id'], ),
                    sa.PrimaryKeyConstraint('meta_id', 'company_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('companies_meta')
    op.drop_table('companies')
    op.drop_table('meta')
    op.drop_table('cities')
    # ### end Alembic commands ###
