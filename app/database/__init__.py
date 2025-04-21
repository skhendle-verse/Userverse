from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    def __init__(self, configs: dict) -> None:
        self._base = Base
        self.configs = configs

        from .user import User

        self.engine = self._configure_engine()
        self._base.metadata.create_all(bind=self.engine)
        self._session = sessionmaker()
        self._session.configure(bind=self.engine)

    def _configure_engine(self):
        url = self.configs["main_database_url"]
        # print(f"Database URL: {url}")
        if not database_exists(url):
            create_database(url)

        return create_engine(url, pool_pre_ping=True, echo=False)

    def session_object(self):
        return self._session()