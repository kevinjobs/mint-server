"""initdb

Revision ID: b3e6814df96e
Revises: 
Create Date: 2024-01-07 22:35:59.787482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3e6814df96e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('origin', sa.String(), nullable=False),
    sa.Column('filepath', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(), nullable=True),
    sa.Column('updateAt', sa.Integer(), nullable=True),
    sa.Column('createAt', sa.Integer(), nullable=True),
    sa.Column('deleteAt', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('posts',
    sa.Column('createAt', sa.Integer(), nullable=True),
    sa.Column('publishAt', sa.Integer(), nullable=True),
    sa.Column('updateAt', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('excerpt', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('exif', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(), nullable=True),
    sa.Column('deleteAt', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('nickname', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('birthday', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('motto', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.Column('invitation', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(), nullable=True),
    sa.Column('updateAt', sa.Integer(), nullable=True),
    sa.Column('createAt', sa.Integer(), nullable=True),
    sa.Column('deleteAt', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('posts')
    op.drop_table('files')
    # ### end Alembic commands ###
