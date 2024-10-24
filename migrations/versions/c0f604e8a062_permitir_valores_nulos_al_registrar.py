"""Permitir valores nulos al registrar

Revision ID: c0f604e8a062
Revises: 
Create Date: 2024-10-22 11:00:24.955033

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c0f604e8a062'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classalimentos', schema=None) as batch_op:
        batch_op.alter_column('porcion',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.Float(),
               existing_nullable=False)

    with op.batch_alter_table('classusuarios', schema=None) as batch_op:
        batch_op.alter_column('verificado',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Integer(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classusuarios', schema=None) as batch_op:
        batch_op.alter_column('verificado',
               existing_type=sa.Integer(),
               type_=mysql.TINYINT(display_width=1),
               nullable=False)

    with op.batch_alter_table('classalimentos', schema=None) as batch_op:
        batch_op.alter_column('porcion',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###
