"""empty message

Revision ID: fcf76f49d872
Revises: 
Create Date: 2021-03-26 05:56:43.376937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcf76f49d872'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('clientName', sa.String(), nullable=False),
    sa.Column('clientPhone', sa.String(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lessons')
    # ### end Alembic commands ###
