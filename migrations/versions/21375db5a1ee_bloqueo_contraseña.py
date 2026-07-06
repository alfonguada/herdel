"""bloqueo contraseña

Revision ID: 21375db5a1ee
Revises: 50c1e2bd151b
Create Date: 2025-10-20 07:59:34.969891

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '21375db5a1ee'
down_revision = '50c1e2bd151b'
branch_labels = None
depends_on = None


def upgrade():
    # Solo añadimos el nuevo campo, no tocamos la tabla QR existente
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bloqueos_temporales', sa.Integer(), nullable=True))


def downgrade():
    # Solo eliminamos el campo si hacemos rollback
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bloqueos_temporales')