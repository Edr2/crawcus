from sqlalchemy import create_engine
from base import Base
#we need to import this FactoryImage for scheme creation
from factory_image import FactoryImage

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///simple.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
