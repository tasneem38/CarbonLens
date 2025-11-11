from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("name", sa.String),
    )
    op.create_table(
        "footprint_runs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("electricity_kwh", sa.Float),
        sa.Column("car_km", sa.Float),
        sa.Column("bus_km", sa.Float),
        sa.Column("diet", sa.String),
        sa.Column("total_kg", sa.Float),
        sa.Column("energy_kg", sa.Float),
        sa.Column("travel_kg", sa.Float),
        sa.Column("food_kg", sa.Float),
        sa.Column("score", sa.Integer),
    )

def downgrade():
    op.drop_table("footprint_runs")
    op.drop_table("users")
