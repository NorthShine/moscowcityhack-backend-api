import databases
import sqlalchemy

DATABASE_URL = 'sqlite:///./project.db'

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('username', sqlalchemy.String, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String),
)
whitelist = sqlalchemy.Table(
    'whitelist',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('url', sqlalchemy.String, unique=True),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)
metadata.create_all(engine)
