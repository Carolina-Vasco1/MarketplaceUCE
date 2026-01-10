from libs.db.postgres import make_engine, make_session_factory
from ..core.config import settings

engine = make_engine(settings.POSTGRES_URL)
SessionLocal = make_session_factory(engine)
