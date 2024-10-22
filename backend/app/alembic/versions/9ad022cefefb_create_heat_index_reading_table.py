"""Create heat_index_reading table

Revision ID: 9ad022cefefb
Revises: 29f0496f917c
Create Date: 2024-10-21 13:06:03.618456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ad022cefefb'
down_revision = '29f0496f917c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heat_index_reading',
    sa.Column('sensor_id', sa.Uuid(), nullable=False),
    sa.Column('weather_station_id', sa.Uuid(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('read_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.ForeignKeyConstraint(['weather_station_id'], ['weather_station.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('heat_index_reading')
    # ### end Alembic commands ###