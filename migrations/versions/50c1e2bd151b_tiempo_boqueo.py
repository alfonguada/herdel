"""tiempo_boqueo

Revision ID: 50c1e2bd151b
Revises: 672e18ccca70
Create Date: 2025-09-30 08:21:08.688122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c1e2bd151b'
down_revision = '672e18ccca70'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bloqueado_hasta', sa.DateTime(), nullable=True))



def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bloqueado_hasta')
