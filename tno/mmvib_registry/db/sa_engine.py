from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine, orm
from sqlalchemy.engine import URL

from tno.mmvib_registry.settings import EnvSettings
from tno.shared.log import get_logger

logger = get_logger(__name__)

session_factory = orm.sessionmaker()
Session = orm.scoped_session(session_factory)


@contextmanager
def session_scope(bind=None):
    """Provide a transactional scope around a series of operations. Ensures that the session is
    commited and closed. Exceptions raised within the 'with' block using this contextmanager
    should be handled in the with block itself. They will not be caught by the 'except' here."""
    try:
        if bind:
            yield Session(bind=bind)
        yield Session()
        Session.commit()
    except Exception:
        # Only the exceptions raised by session.commit above are caught here
        Session.rollback()
        raise
    finally:
        Session.remove()


def with_session(func):
    """
    Wraps the function in a transaction, any errors thrown in the function
    are intercepted so the tx can be rolled back.
    """

    @wraps(func)
    def wrapped(**kwargs):
        with session_scope() as session:
            try:
                result = func(session=session, **kwargs)
                session.commit()
                return result
            except Exception as exception:
                logger.exception(exception)
                session.rollback()
                raise

    return wrapped


def initialize_db(application_name: str, url: URL | None = None):
    """
    Initialize the database connection by creating the engine and configuring
    the default session maker.
    """
    if url is None:
        url = URL.create(
            "postgresql+psycopg2",
            username=EnvSettings.postgres_user(),
            password=EnvSettings.postgres_password(),
            host=EnvSettings.postgres_host(),
            port=EnvSettings.postgres_port(),
            database=EnvSettings.postgres_db(),
        )

    engine = create_engine(
        url,
        pool_size=20,
        max_overflow=5,
        echo=False,
        connect_args={
            "application_name": application_name,
            "options": "-c lock_timeout=30000 -c statement_timeout=300000",  # 5 minutes
        },
    )

    # Bind the global session to the actual engine.
    Session.configure(bind=engine)

    return engine
