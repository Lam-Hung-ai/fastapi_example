"""add foreign key to post table

Revision ID: e6d8dbaba937
Revises: d59975fb58ed
Create Date: 2024-08-24 14:18:29.082782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6d8dbaba937'
down_revision: Union[str, None] = 'd59975fb58ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
