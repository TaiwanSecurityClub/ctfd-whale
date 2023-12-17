"""add WhaleConfig WhaleRedirectTemplate DynamicDockerChallenge WhaleContainer

Revision ID: ad7c31bc8fdf
Revises: 
Create Date: 2023-12-17 23:24:17.040989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'ad7c31bc8fdf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(op=None):
    op.create_table(
        "whale_config",
        sa.Column("key", sa.String(length=128), nullable=False),
        sa.Column("value", sa.Text),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "whale_container",
        sa.Column("id", sa.Integer, nullable=False, autoincrement=True),
        sa.Column("user_id", sa.Integer),
        sa.Column("challenge_id", sa.Integer),
        sa.Column("start_time", sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column("renew_count", sa.Integer, nullable=False, default=0),
        sa.Column("status", sa.Integer, default=1),
        sa.Column("uuid", sa.String(256)),
        sa.Column("port", sa.Integer, nullable=True, default=0),
        sa.Column("flag", sa.String(128), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["challenge_id"], ["challenges.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "whale_redirect_template",
        sa.Column("key", sa.String(length=20), nullable=False),
        sa.Column("frp_template", sa.Text),
        sa.Column("access_template", sa.Text),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "dynamic_docker_challenge",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("memory_limit", sa.Text, default="128m"),
        sa.Column("cpu_limit", sa.Float, default=0.5),
        sa.Column("dynamic_score", sa.Integer, default=0),
        sa.Column("docker_image", sa.Text, default=0),
        sa.Column("redirect_type", sa.Text, default=0),
        sa.Column("redirect_port", sa.Integer, default=0),
        sa.ForeignKeyConstraint(["id"], ["dynamic_challenge.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade(op=None) -> None:
    op.drop_table("whale_config")
    op.drop_table("whale_container")
    op.drop_table("whale_redirect_template")
    op.drop_table("dynamic_docker_challenge")

