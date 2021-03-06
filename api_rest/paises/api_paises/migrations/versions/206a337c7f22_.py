"""empty message

Revision ID: 206a337c7f22
Revises: 
Create Date: 2020-02-21 23:31:40.797307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '206a337c7f22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paises',
    sa.Column('codigo', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=32), nullable=False),
    sa.Column('sigla', sa.String(length=3), nullable=False),
    sa.Column('dataInicio', sa.Date(), nullable=False),
    sa.Column('dataFim', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('codigo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paises')
    # ### end Alembic commands ###
