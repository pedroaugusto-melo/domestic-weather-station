"""Create sensor table

Revision ID: 5ecfcf9e9a66
Revises: 1a31ce608336
Create Date: 2024-10-14 09:35:35.795709

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5ecfcf9e9a66'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor',
    sa.Column('manufacturer', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('component_reference', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('datasheet_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('part_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('measuremnts_types', sa.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sensor_part_number'), 'sensor', ['part_number'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sensor_part_number'), table_name='sensor')
    op.drop_table('sensor')
    # ### end Alembic commands ###
