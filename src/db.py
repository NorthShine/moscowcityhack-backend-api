import databases
import sqlalchemy as sa
from sqlalchemy_utils import PasswordType

DATABASE_URL = 'sqlite:///./project.db'

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String, unique=True),
    sa.Column('password', PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']),
    )
)
whitelist = sa.Table(
    'whitelist',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('url', sa.String, unique=True),
)
checked_urls = sa.Table(
    'checked_urls',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('url', sa.String),
    sa.Column('is_trusted_url', sa.Boolean),
    sa.Column('is_real_author', sa.Boolean),
    sa.Column('is_real_article', sa.Boolean)
)


engine = sa.create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)
metadata.create_all(engine)
