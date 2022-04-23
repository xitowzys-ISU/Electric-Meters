import sqlalchemy as sa
from config import DB_USERNAME, DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT

engine = sa.create_engine(
    f"mariadb+mariadbconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")
