import logging
from logging.config import fileConfig
from alembic import context
from flask import current_app

# Interpret the config file for Python logging.
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    """
    Retrieve the SQLAlchemy engine from Flask-Migrate.
    Handles differences between Flask-SQLAlchemy versions.
    """
    try:
        # Works with Flask-SQLAlchemy < 3 and other setups.
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # For Flask-SQLAlchemy >= 3.
        return current_app.extensions['migrate'].db.engine

def get_engine_url():
    """
    Render the engine URL as a string, escaping percent signs for Alembic.
    """
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')

# Update the SQLAlchemy URL in Alembic config to match the Flask app configuration.
config.set_main_option('sqlalchemy.url', get_engine_url())

target_db = current_app.extensions['migrate'].db

def get_metadata():
    """
    Retrieve the SQLAlchemy metadata for autogeneration.
    """
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Run migrations in 'online' mode.
    """
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No schema changes detected; skipping migration generation.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
