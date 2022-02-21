import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

#SQLALCHEMY_DATABASE_URL = "sql ite:///./database.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@35.199.104.124:3306/fletit"

#engine = _sql.create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#)

engine = _sql.create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()