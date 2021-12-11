"""changed professional rating table

Revision ID: a7b29220527a
Revises: 9506b09c14b8
Create Date: 2021-12-10 16:19:48.587521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b29220527a'
down_revision = '9506b09c14b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('professional_rating', 'rating',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('professional_rating', 'rating',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###