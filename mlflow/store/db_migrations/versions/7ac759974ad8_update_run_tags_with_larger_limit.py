"""Update run tags with larger limit

Revision ID: 7ac759974ad8
Revises: df50e92ffc5e
Create Date: 2019-07-30 16:36:54.256382

"""
from alembic import op
import sqlalchemy as sa
from mlflow.store.tracking.dbmodels.initial_models import SqlTag, SqlParam


# revision identifiers, used by Alembic.
revision = '7ac759974ad8'
down_revision = 'df50e92ffc5e'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    SqlTag.__table__.create(bind = bind.engine, checkfirst = True)
    # Not sure when to table params was introduced, but putting it here.
    SqlParam.__table__.create(bind = bind.engine, checkfirst = True)

    # Use batch mode so that we can run "ALTER TABLE" statements against SQLite
    # databases (see more info at https://alembic.sqlalchemy.org/en/latest/
    # batch.html#running-batch-migrations-for-sqlite-and-other-databases)
    # We specify existing_type, existing_nullable, existing_server_default
    # because MySQL alter column statements require a full column description.
    with op.batch_alter_table("tags") as batch_op:
        batch_op.alter_column("value",
                              existing_type=sa.String(250),
                              type_=sa.String(5000),
                              existing_nullable=True,
                              existing_server_default=None)


def downgrade():
    pass
