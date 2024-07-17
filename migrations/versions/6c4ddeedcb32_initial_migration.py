"""initial migration

Revision ID: 6c4ddeedcb32
Revises: 
Create Date: 2024-07-17 10:11:55.881836

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6c4ddeedcb32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('number', sa.String(length=10), nullable=False),
    sa.Column('arcana', sa.String(length=200), nullable=False),
    sa.Column('suit', sa.String(length=200), nullable=False),
    sa.Column('img', sa.String(length=200), nullable=False),
    sa.Column('fortune_telling', sa.Text(), nullable=True),
    sa.Column('keywords', sa.Text(), nullable=True),
    sa.Column('meanings', sa.Text(), nullable=True),
    sa.Column('archetype', sa.String(length=200), nullable=True),
    sa.Column('hebrew_alphabet', sa.String(length=200), nullable=True),
    sa.Column('numerology', sa.String(length=200), nullable=True),
    sa.Column('elemental', sa.String(length=200), nullable=True),
    sa.Column('mythical_spiritual', sa.Text(), nullable=True),
    sa.Column('astrology', sa.String(length=200), nullable=True),
    sa.Column('affirmation', sa.String(length=200), nullable=True),
    sa.Column('questions_to_ask', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spread_layouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('layout_description', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auth0_user_id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('auth0_user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('readings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('spread_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spreads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('number_of_cards', sa.Integer(), nullable=False),
    sa.Column('layout_id', sa.Integer(), nullable=False),
    sa.Column('position_meanings', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['layout_id'], ['spread_layouts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spread_cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('position_name', sa.String(length=256), nullable=False),
    sa.Column('position_interpretation', sa.String(length=256), nullable=False),
    sa.Column('spread_id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['spread_id'], ['spreads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spread_cards')
    op.drop_table('spreads')
    op.drop_table('readings')
    op.drop_table('users')
    op.drop_table('spread_layouts')
    op.drop_table('cards')
    # ### end Alembic commands ###