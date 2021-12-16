"""adjusted models for 'cascade'

Revision ID: 6ed6b534e71f
Revises: d66f5633eb9c
Create Date: 2021-12-16 11:39:56.982676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ed6b534e71f'
down_revision = 'd66f5633eb9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('deficiency_client_client_id_fkey', 'deficiency_client', type_='foreignkey')
    op.create_foreign_key(None, 'deficiency_client', 'clients', ['client_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('disease_client_client_id_fkey', 'disease_client', type_='foreignkey')
    op.create_foreign_key(None, 'disease_client', 'clients', ['client_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('surgery_client_client_id_fkey', 'surgery_client', type_='foreignkey')
    op.create_foreign_key(None, 'surgery_client', 'clients', ['client_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'surgery_client', type_='foreignkey')
    op.create_foreign_key('surgery_client_client_id_fkey', 'surgery_client', 'clients', ['client_id'], ['id'])
    op.drop_constraint(None, 'disease_client', type_='foreignkey')
    op.create_foreign_key('disease_client_client_id_fkey', 'disease_client', 'clients', ['client_id'], ['id'])
    op.drop_constraint(None, 'deficiency_client', type_='foreignkey')
    op.create_foreign_key('deficiency_client_client_id_fkey', 'deficiency_client', 'clients', ['client_id'], ['id'])
    # ### end Alembic commands ###
