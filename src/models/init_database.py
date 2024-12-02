from .database import Base, engine


def init_db():
    # pylint: disable=import-outside-toplevel
    # pylint: disable=unused-import
    import src.models.todo
    Base.metadata.create_all(bind=engine)
