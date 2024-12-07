from .database import Base, engine


def init_db():
    # pylint: disable=import-outside-toplevel
    # pylint: disable=unused-import
    import models.case
    import models.victim
    import models.suspect
    Base.metadata.create_all(bind=engine)
