"""bloqueo ip

Revision ID: 730361bd2ebb
Revises: 21375db5a1ee
Create Date: 2025-10-30 11:41:58.992056
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '730361bd2ebb'
down_revision = '21375db5a1ee'
branch_labels = None
depends_on = None


def upgrade():
    # Solo añadimos las columnas nuevas
    with op.batch_alter_table('empresa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ip_empresa', sa.String(length=45), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bloquear_por_ip', sa.Boolean(), nullable=True))


def downgrade():
    # Revertir los cambios si se baja la migración
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bloquear_por_ip')

    with op.batch_alter_table('empresa', schema=None) as batch_op:
        batch_op.drop_column('ip_empresa')
