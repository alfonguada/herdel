"""compleata2025-2

Revision ID: c1bbbaa88980
Revises: 9de22436ee03
Create Date: 2025-12-18 16:21:00.923660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1bbbaa88980'
down_revision = '9de22436ee03'
branch_labels = None
depends_on = None


def upgrade():
    # --- tablas nuevas ---
    op.create_table(
        'baja',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_baja_user'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'qr',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('imagen', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('centro_trabajo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['user.id'], name='fk_qr_user'
        ),
        sa.ForeignKeyConstraint(
            ['centro_trabajo_id'], ['centro_trabajo.id'], name='fk_qr_centro_trabajo'
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'solicitud_cambio_horario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('registro_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=10), nullable=True),
        sa.Column('nueva_fecha_hora', sa.DateTime(), nullable=False),
        sa.Column('motivo', sa.Text(), nullable=False),
        sa.Column('estado', sa.String(length=10), nullable=True),
        sa.Column('token', sa.String(length=100), nullable=False),
        sa.Column('fecha_solicitud', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['registro_id'], ['registro.id'], name='fk_solicitud_registro'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token', name='uq_solicitud_token')
    )

    # --- cambios en tablas existentes ---
    with op.batch_alter_table('contrato', schema=None) as batch_op:
        batch_op.alter_column(
            'archivo',
            existing_type=sa.BLOB(),
            type_=sa.String(length=255),
            existing_nullable=False
        )

    with op.batch_alter_table('empresa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('logo_favicon', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('logo_login', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('logo_menu', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('ip_empresa', sa.String(length=45), nullable=True))

    with op.batch_alter_table('festivo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('año', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('empresa_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            'fk_festivo_empresa',
            'empresa',
            ['empresa_id'],
            ['id']
        )

    with op.batch_alter_table('nomina', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ruta', sa.String(length=255), nullable=True))
        batch_op.drop_column('archivo')

    with op.batch_alter_table('registro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('aprobado_modificacion', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('centro_trabajo_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_registro_centro_trabajo',
            'centro_trabajo',
            ['centro_trabajo_id'],
            ['id']
        )

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bloqueos_temporales', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('empresa_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('vacaciones', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('registros_horarios', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('ausencias', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('bloquear_por_ip', sa.Boolean(), nullable=True))
        batch_op.create_foreign_key(
            'fk_user_empresa',
            'empresa',
            ['empresa_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_empresa', type_='foreignkey')
        batch_op.drop_column('bloquear_por_ip')
        batch_op.drop_column('ausencias')
        batch_op.drop_column('registros_horarios')
        batch_op.drop_column('vacaciones')
        batch_op.drop_column('empresa_id')
        batch_op.drop_column('bloqueos_temporales')

    with op.batch_alter_table('registro', schema=None) as batch_op:
        batch_op.drop_constraint('fk_registro_centro_trabajo', type_='foreignkey')
        batch_op.drop_column('centro_trabajo_id')
        batch_op.drop_column('aprobado_modificacion')

    with op.batch_alter_table('nomina', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archivo', sa.BLOB(), nullable=False))
        batch_op.drop_column('ruta')

    with op.batch_alter_table('festivo', schema=None) as batch_op:
        batch_op.drop_constraint('fk_festivo_empresa', type_='foreignkey')
        batch_op.drop_column('empresa_id')
        batch_op.drop_column('año')

    with op.batch_alter_table('empresa', schema=None) as batch_op:
        batch_op.drop_column('ip_empresa')
        batch_op.drop_column('logo_menu')
        batch_op.drop_column('logo_login')
        batch_op.drop_column('logo_favicon')

    with op.batch_alter_table('contrato', schema=None) as batch_op:
        batch_op.alter_column(
            'archivo',
            existing_type=sa.String(length=255),
            type_=sa.BLOB(),
            existing_nullable=False
        )

    op.drop_table('solicitud_cambio_horario')
    op.drop_table('qr')
    op.drop_table('baja')
