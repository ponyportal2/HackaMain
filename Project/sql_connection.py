from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import atexit

engine = create_engine("sqlite:///metanit.db", echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
print(engine)
Base = declarative_base()
# conn.execute(text("BEGIN CONCURRENT; COMMIT;"))

def exit_sql():
    print('Saving database, commit')
    conn.commit()

atexit.register(exit_sql)