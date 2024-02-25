"""first week models

Revision ID: 3c8a9e008d67
Revises: 
Create Date: 2024-02-22 10:55:56.724141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '3c8a9e008d67'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agerange',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('MinAge', sa.Integer(), nullable=False),
    sa.Column('MaxAge', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('number_of_people', sa.Integer(), nullable=False),
    sa.Column('referred_organization', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('next_renewal_date', sa.Date(), nullable=False),
    sa.Column('derecognition_state', sa.Enum('ACTIVE', 'SUSPENDED', name='derecognitionstatus'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('registration_date', sa.Date(), nullable=False),
    sa.Column('dossier_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('alias', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('first_surname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('second_surname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('sex', sa.Enum('MALE', 'FEMALE', name='sex'), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dni', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('contact_phone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('first_appointment_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('familyagerangelink',
    sa.Column('family_id', sa.Integer(), nullable=False),
    sa.Column('age_range_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['age_range_id'], ['agerange.id'], ),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('family_id', 'age_range_id')
    )
    op.create_table('familyobservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('observation_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patientobservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('observation_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patientobservation')
    op.drop_table('familyobservation')
    op.drop_table('familyagerangelink')
    op.drop_table('user')
    op.drop_table('patient')
    op.drop_table('family')
    op.drop_table('agerange')
    # ### end Alembic commands ###