from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker, declarative_base
from app.configs import ConfigLoader

Base = declarative_base()

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._base = Base
        # load configs
        loader = ConfigLoader()
        configs = loader.get_config()
        self.configs = configs

        from .user import User

        self.engine = self._configure_engine()
        self._base.metadata.create_all(bind=self.engine)
        self._session = sessionmaker()
        self._session.configure(bind=self.engine)

    def _configure_engine(self):
        url = self.configs["database_url"]
        if not database_exists(url):
            create_database(url)

        return create_engine(url, pool_pre_ping=True, echo=False)

    def session_object(self):
        return self._session()
