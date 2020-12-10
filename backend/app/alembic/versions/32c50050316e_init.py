"""Init

Revision ID: 32c50050316e
Revises: 
Create Date: 2020-12-08 22:11:06.972099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32c50050316e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('proj_id', sa.String(length=8), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=True),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('proj_id')
    )
    op.create_index(op.f('ix_project_description'), 'project', ['description'], unique=False)
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)
    op.create_index(op.f('ix_project_name'), 'project', ['name'], unique=False)
    op.create_table('issue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_id', sa.String(length=12), nullable=False),
    sa.Column('summary', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('status', sa.String(length=11), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('proj_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['proj_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('issue_id')
    )
    op.create_index(op.f('ix_issue_description'), 'issue', ['description'], unique=False)
    op.create_index(op.f('ix_issue_id'), 'issue', ['id'], unique=False)
    op.create_index(op.f('ix_issue_status'), 'issue', ['status'], unique=False)
    op.create_index(op.f('ix_issue_summary'), 'issue', ['summary'], unique=False)
    op.create_table('issuesrelations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link_from', sa.Integer(), nullable=False),
    sa.Column('link_to', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['link_from'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['link_to'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_issuesrelations_id'), 'issuesrelations', ['id'], unique=False)
    # ### end Alembic commands ###