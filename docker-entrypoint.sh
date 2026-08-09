#!/bin/sh

uv run alembic upgrade head

exec uv run faststream run service.main:app