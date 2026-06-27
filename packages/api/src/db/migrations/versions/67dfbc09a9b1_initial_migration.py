"""Initial migration

Revision ID: 67dfbc09a9b1
Revises:
Create Date: 2025-02-14 10:00:00.000000

"""
from typing import Sequence, Optional

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67dfbc09a9b1'
down_revision: Optional[str] = None
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('contact', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_name'), 'customers', ['name'], unique=False)

    op.create_table(
        'materials',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('spec', sa.String(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_materials_name'), 'materials', ['name'], unique=False)

    op.create_table(
        'drafts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer_name_raw', sa.String(), nullable=False),
        sa.Column('matched_customer_id', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('DRAFT', 'CONFIRMED', 'SUBMITTED', 'COMPLETED', name='quotationstatus'), nullable=False),
        sa.Column('matching_score', sa.Float(), nullable=False),
        sa.Column('needs_confirmation', sa.Boolean(), nullable=False),
        sa.Column('raw_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['matched_customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'draft_items',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('draft_id', sa.String(), nullable=False),
        sa.Column('material_name_raw', sa.String(), nullable=False),
        sa.Column('matched_material_id', sa.String(), nullable=True),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=True),
        sa.Column('matching_score', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['draft_id'], ['drafts.id'], ),
        sa.ForeignKeyConstraint(['matched_material_id'], ['materials.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('draft_items')
    op.drop_table('drafts')
    op.drop_table('materials')
    op.drop_table('customers')
    sa.Enum(name='quotationstatus').drop(op.get_bind())
