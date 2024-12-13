from .database import Base, engine


def init_db():
    # pylint: disable=import-outside-toplevel
    # pylint: disable=unused-import
    import src.models.case
    import src.models.victim
    import src.models.suspect
    Base.metadata.create_all(bind=engine)
