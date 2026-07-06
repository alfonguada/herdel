"""qrs2

Revision ID: 22c7dfe6a2d4
Revises: 933aa63f56de
Create Date: 2025-05-15 12:13:52.228803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22c7dfe6a2d4'
down_revision = '933aa63f56de'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('registro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('centro_trabajo_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_registro_centro_trabajo_id',
            'centro_trabajo',
            ['centro_trabajo_id'],
            ['id']
        )

def downgrade():
    with op.batch_alter_table('registro', schema=None) as batch_op:
        batch_op.drop_constraint('fk_registro_centro_trabajo_id', type_='foreignkey')
        batch_op.drop_column('centro_trabajo_id')


    # ### end Alembic commands ###
